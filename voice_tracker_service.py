
import discord
import asyncio
import aiohttp
from aiohttp import web
import sqlite3
import configparser
import os
import sys
import time
from datetime import datetime

# --- Configuration ---
CONFIG_FILE = 'config/secrets.conf'
DB_FILE = 'voice_tracker.db'
API_PORT = 3002

def load_token():
    config = configparser.ConfigParser()
    if not os.path.exists(CONFIG_FILE):
        print(f"❌ Config file not found: {CONFIG_FILE}")
        sys.exit(1)
    config.read(CONFIG_FILE)
    try:
        return config['STUDYLION']['token']
    except KeyError:
        print("❌ Token not found in config file")
        sys.exit(1)

TOKEN = load_token()

# --- Database Setup ---
def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS user_stats (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            total_study_seconds INTEGER DEFAULT 0,
            total_cam_seconds INTEGER DEFAULT 0,
            total_stream_seconds INTEGER DEFAULT 0,
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# --- Tracking Logic ---
class VoiceTrackerBot(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        intents.voice_states = True
        intents.members = True # Needed to get usernames
        super().__init__(intents=intents)
        
        # Memory storage for active sessions
        # user_id -> { 'last_update': timestamp, 'cam': bool, 'stream': bool, 'channel': channel_id }
        self.active_sessions = {}
        self.db_conn = sqlite3.connect(DB_FILE) # Keep connection open? Or reopen? sqlite is okay with single thread
        # For thread safety with aiohttp, we should probably close/open per request or use a pool, 
        # but for this scale, open per request is safest/easiest. 
        # Actually this bot class runs in the main event loop.
        self.db_conn.close() 

    def get_db_connection(self):
        conn = sqlite3.connect(DB_FILE)
        conn.row_factory = sqlite3.Row
        return conn

    async def on_ready(self):
        print(f'✅ Voice Tracker Service logged in as {self.user}')
        print('👀 Monitoring voice channels...')
        # Re-scan all channels to catch up state if bot restarted
        for guild in self.guilds:
            for vc in guild.voice_channels:
                for member in vc.members:
                    if not member.bot:
                        self.active_sessions[member.id] = {
                            'last_update': time.time(),
                            'cam': member.voice.self_video,
                            'stream': member.voice.self_stream,
                            'channel': vc.id
                        }
        print(f'📊 Initialized {len(self.active_sessions)} active sessions.')

        # Start API Server
        app = web.Application()
        app.add_routes([
            web.get('/api/stats/{user_id}', self.handle_get_stats),
            web.get('/api/leaderboard', self.handle_get_leaderboard),
            web.get('/', self.handle_root)
        ])
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, '0.0.0.0', API_PORT)
        await site.start()
        print(f'🚀 API Server running on port {API_PORT}')
        
        if not hasattr(self, 'bg_task'):
            # Start background updater only once
            self.bg_task = self.loop.create_task(self.background_updater())

    async def background_updater(self):
        await self.wait_until_ready()
        while not self.is_closed():
            try:
                # print("🔄 Running periodic update...")
                now = time.time()
                updates = []
                
                # 1. Calculate deltas in memory
                for user_id, session in list(self.active_sessions.items()):
                    delta = now - session['last_update']
                    if delta > 0:
                        user = self.get_user(user_id)
                        username = user.name if user else "Unknown"
                        updates.append({
                            'user_id': user_id,
                            'username': username,
                            'delta': delta,
                            'cam': session['cam'],
                            'stream': session['stream']
                        })
                        session['last_update'] = now
                
                # 2. Batch write to DB (Single Transaction)
                if updates:
                    conn = self.get_db_connection()
                    c = conn.cursor()
                    try:
                        c.execute("BEGIN TRANSACTION")
                        
                        for u in updates:
                            # Check exist
                            c.execute('SELECT 1 FROM user_stats WHERE user_id = ?', (u['user_id'],))
                            if not c.fetchone():
                                c.execute('''
                                    INSERT INTO user_stats (user_id, username, total_study_seconds, total_cam_seconds, total_stream_seconds)
                                    VALUES (?, ?, 0, 0, 0)
                                ''', (u['user_id'], u['username']))
                            
                            # Update total
                            c.execute('''
                                UPDATE user_stats 
                                SET username = ?, total_study_seconds = total_study_seconds + ?, last_updated = CURRENT_TIMESTAMP 
                                WHERE user_id = ?
                            ''', (u['username'], u['delta'], u['user_id']))
                            
                            # Update cam
                            if u['cam']:
                                c.execute('UPDATE user_stats SET total_cam_seconds = total_cam_seconds + ? WHERE user_id = ?', (u['delta'], u['user_id']))
                            
                            # Update stream
                            if u['stream']:
                                c.execute('UPDATE user_stats SET total_stream_seconds = total_stream_seconds + ? WHERE user_id = ?', (u['delta'], u['user_id']))
                        
                        conn.commit()
                        # print(f"✅ Batch updated {len(updates)} users.")
                    except Exception as e:
                        print(f"⚠️ Batch update failed: {e}")
                        conn.rollback()
                    finally:
                        conn.close()

            except Exception as e:
                print(f"⚠️ Background update loop error: {e}")
            
            await asyncio.sleep(60) # Update every 60 seconds

    async def save_progress(self, user_id, username, delta, was_cam, was_stream):
        # This function is now only used for single events (leave/join), not the loop.
        # It's fine to keep it separate for immediate event handling.
        if delta <= 0: return
        
        conn = self.get_db_connection()
        c = conn.cursor()
        
        c.execute('SELECT 1 FROM user_stats WHERE user_id = ?', (user_id,))
        if not c.fetchone():
             c.execute('''
                INSERT INTO user_stats (user_id, username, total_study_seconds, total_cam_seconds, total_stream_seconds)
                VALUES (?, ?, 0, 0, 0)
            ''', (user_id, username))
        
        c.execute('UPDATE user_stats SET username = ?, total_study_seconds = total_study_seconds + ?, last_updated = CURRENT_TIMESTAMP WHERE user_id = ?', 
                  (username, delta, user_id))
        
        if was_cam:
            c.execute('UPDATE user_stats SET total_cam_seconds = total_cam_seconds + ? WHERE user_id = ?', (delta, user_id))
        
        if was_stream:
            c.execute('UPDATE user_stats SET total_stream_seconds = total_stream_seconds + ? WHERE user_id = ?', (delta, user_id))
            
        conn.commit()
        conn.close()

    async def on_voice_state_update(self, member, before, after):
        if member.bot: return

        user_id = member.id
        now = time.time()

        # 1. Handle Existing Session (End it or Update it)
        if user_id in self.active_sessions:
            session = self.active_sessions[user_id]
            delta = now - session['last_update']
            
            # Save accumulated time
            await self.save_progress(
                user_id, 
                member.name, 
                delta, 
                session['cam'], 
                session['stream']
            )

        # 2. Determine New State
        if after.channel is None:
            # User left voice
            if user_id in self.active_sessions:
                del self.active_sessions[user_id]
                # print(f"👋 {member.name} left voice.")
        else:
            # User joined or changed state (cam/stream)
            self.active_sessions[user_id] = {
                'last_update': now,
                'cam': after.self_video,
                'stream': after.self_stream,
                'channel': after.channel.id
            }
            # print(f"🎙️ {member.name} update: Cam={after.self_video}, Stream={after.self_stream}")

    # --- API Handlers ---
    async def handle_root(self, request):
        return web.Response(text="StudyLion Voice Tracker API is running.")

    async def handle_get_stats(self, request):
        user_id = request.match_info['user_id']
        try:
            conn = self.get_db_connection()
            c = conn.cursor()
            c.execute('SELECT * FROM user_stats WHERE user_id = ?', (user_id,))
            row = c.fetchone()
            conn.close()
            
            if row:
                data = dict(row)
                # Convert seconds to milliseconds as requested
                response_data = {
                    'user_id': data['user_id'],
                    'username': data['username'],
                    'totalTime': int(data['total_study_seconds'] * 1000),
                    'camTime': int(data['total_cam_seconds'] * 1000),
                    'shareTime': int(data['total_stream_seconds'] * 1000),
                    'last_updated': data['last_updated']
                }
                return web.json_response(response_data)
            else:
                return web.json_response({'error': 'User not found'}, status=404)
        except Exception as e:
            return web.json_response({'error': str(e)}, status=500)

    async def handle_get_leaderboard(self, request):
        try:
            conn = self.get_db_connection()
            c = conn.cursor()
            limit = request.query.get('limit', 10)
            c.execute('SELECT * FROM user_stats ORDER BY total_study_seconds DESC LIMIT ?', (limit,))
            rows = c.fetchall()
            conn.close()
            
            data = []
            for row in rows:
                r = dict(row)
                data.append({
                    'user_id': r['user_id'],
                    'username': r['username'],
                    'totalTime': int(r['total_study_seconds'] * 1000), # ms
                    'camTime': int(r['total_cam_seconds'] * 1000),     # ms
                    'shareTime': int(r['total_stream_seconds'] * 1000) # ms
                })
            return web.json_response(data)
        except Exception as e:
            return web.json_response({'error': str(e)}, status=500)

if __name__ == '__main__':
    client = VoiceTrackerBot()
    client.run(TOKEN)
