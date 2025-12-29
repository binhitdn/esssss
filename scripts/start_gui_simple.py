#!/usr/bin/env python3
"""
Simple GUI server startup script that doesn't import bot dependencies.
"""
import sys
import os
import asyncio
import logging
import multiprocessing
import pickle
import time
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

# Import only what we need for GUI
from gui.routes import routes
from gui.utils import RequestState, short_uuid

# Simple config reading
def read_config():
    """Read GUI config without importing full meta module"""
    config_path = Path("config/gui.conf")
    config = {}
    
    if config_path.exists():
        with open(config_path) as f:
            current_section = None
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                if line.startswith('[') and line.endswith(']'):
                    current_section = line[1:-1]
                    continue
                if '=' in line and current_section == 'GUI':
                    key, value = line.split('=', 1)
                    config[key.strip()] = value.strip()
    
    # Defaults
    config.setdefault('socket_path', 'gui.sock')
    config.setdefault('process_count', '4')
    
    return config

config = read_config()
PATH = config['socket_path']
MAX_PROC = int(config['process_count'])

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

executor: ProcessPoolExecutor = None

async def handle_request(reader, writer):
    """Handle GUI rendering request"""
    try:
        data = await reader.read()
        route, args, kwargs = pickle.loads(data)
        rqid = short_uuid()

        logger.info(f"Handling request: {route}")

        if route in routes:
            try:
                start = time.time()
                data, error = await routes[route](runner, args, kwargs)
                if error is None:
                    state = RequestState.SUCCESS
                else:
                    state = RequestState.RENDER_ERROR
            except Exception as e:
                logger.error(f"Error in route {route}: {e}")
                data, error = b'', repr(e)
                state = RequestState.SYSTEM_ERROR

            dur = time.time() - start
            payload = {
                'rqid': rqid,
                'state': state.value,
                'data': data,
                'length': len(data),
                'error': error,
                'duration': dur
            }
            logger.info(f"Request {route} completed in {dur:.3f}s")
        else:
            logger.warning(f"Unknown route: {route}")
            payload = {
                'rqid': rqid,
                'state': int(RequestState.UNKNOWN_ROUTE),
            }

        response = pickle.dumps(payload)
        writer.write(response)
        writer.write_eof()

        try:
            await writer.drain()
        except ConnectionResetError:
            logger.info("Request was cancelled")
    except Exception as e:
        logger.error(f"Error handling request: {e}")
    finally:
        if not writer.is_closing():
            writer.close()
            try:
                await writer.wait_closed()
            except:
                pass

def _execute(method, args, kwargs):
    """Execute method in process pool"""
    try:
        result = method(*args, **kwargs)
        error = None
    except Exception as e:
        logger.error(f"Error in worker: {e}")
        result = b''
        error = repr(e)
    return result, error

async def runner(method, args, kwargs):
    """Run method in executor"""
    return await asyncio.get_event_loop().run_in_executor(
        executor, _execute, method, args, kwargs
    )

def worker_init():
    """Initialize worker process"""
    logger.info(f"Worker {multiprocessing.current_process().name} started")

async def main():
    """Main GUI server"""
    global executor
    
    logger.info("Starting GUI server...")
    
    # Clean up old socket
    socket_path = Path(PATH)
    if socket_path.exists():
        socket_path.unlink()
    
    # Start process pool
    executor = ProcessPoolExecutor(MAX_PROC, initializer=worker_init)
    
    try:
        # Start server
        server = await asyncio.start_unix_server(handle_request, PATH)
        logger.info(f"GUI server listening on: {PATH}")
        
        async with server:
            await server.serve_forever()
    except KeyboardInterrupt:
        logger.info("Shutting down GUI server...")
    finally:
        if executor:
            executor.shutdown(wait=True)
        if socket_path.exists():
            socket_path.unlink()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass