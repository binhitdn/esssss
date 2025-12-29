import asyncio
import logging

import aiohttp
import discord
from discord.ext import commands

from meta import LionBot, conf, sharding, appname, shard_talk
from meta.app import shardname
from meta.logger import log_context, log_action_stack, setup_main_logger
from meta.context import ctx_bot
from meta.monitor import ComponentMonitor, StatusLevel, ComponentStatus

from data import Database

from babel.translator import LeoBabel, ctx_translator

from constants import DATA_VERSION


for name in conf.config.options('LOGGING_LEVELS', no_defaults=True):
    logging.getLogger(name).setLevel(conf.logging_levels[name])


logging_queue = setup_main_logger()


logger = logging.getLogger(__name__)

db = Database(conf.data['args'])


async def _data_monitor() -> ComponentStatus:
    """
    Component monitor callback for the database.
    """
    data = {
        'stats': str(db.pool.get_stats())
    }
    if not db.pool._opened:
        level = StatusLevel.WAITING
        info = "(WAITING) Database Pool is not opened."
    elif db.pool._closed:
        level = StatusLevel.ERRORED
        info = "(ERROR) Database Pool is closed."
    else:
        level = StatusLevel.OKAY
        info = "(OK) Database Pool statistics: {stats}"
    return ComponentStatus(level, info, info, data)


async def main():
    log_action_stack.set(("Initialising",))
    logger.info("Initialising StudyLion")

    intents = discord.Intents.all()
    intents.members = True
    intents.message_content = True
    intents.presences = False

    async with db.open():
        version = await db.version()
        if version.version != DATA_VERSION:
            error = f"Data model version is {version}, required version is {DATA_VERSION}! Please migrate."
            logger.critical(error)
            raise RuntimeError(error)

        translator = LeoBabel()
        ctx_translator.set(translator)

        async with aiohttp.ClientSession() as session:
            async with LionBot(
                command_prefix='!leo!',
                intents=intents,
                appname=appname,
                shardname=shardname,
                db=db,
                config=conf,
                initial_extensions=[
                    'utils', 'core',
                    # 'analytics',  # Disabled for private bot - requires IPC
                    'modules',
                    'babel',
                    # 'tracking.voice', 'tracking.text',  # Disabled for private bot - requires sysadmin
                ],
                web_client=session,
                app_ipc=shard_talk,
                testing_guilds=conf.bot.getintlist('admin_guilds'),
                shard_id=sharding.shard_number,
                shard_count=sharding.shard_count,
                help_command=None,
                proxy=conf.bot.get('proxy', None),
                translator=translator,
                chunk_guilds_at_startup=False,
            ) as lionbot:
                ctx_bot.set(lionbot)
                lionbot.system_monitor.add_component(
                    ComponentMonitor('Database', _data_monitor)
                )
                
                # Register server restriction handler for private bot
                async def guild_join_listener(guild):
                    await on_guild_join_handler(lionbot, guild)
                
                lionbot.add_listener(guild_join_listener, name='on_guild_join')
                
                try:
                    log_context.set(f"APP: {appname}")
                    logger.info("StudyLion initialised, starting!", extra={'action': 'Starting'})
                    await lionbot.start(conf.bot['TOKEN'])
                except asyncio.CancelledError:
                    log_context.set(f"APP: {appname}")
                    logger.info("StudyLion closed, shutting down.", extra={'action': "Shutting Down"}, exc_info=True)


async def on_guild_join_handler(bot: LionBot, guild: discord.Guild):
    """
    Handler for guild join events - ensures bot only operates on allowed server.
    For private bot deployment serving only server ID: 1434581250798125068
    """
    import os
    allowed_server_id = int(os.environ.get('STUDYLION_SINGLE_SERVER', '1434581250798125068'))
    
    if guild.id != allowed_server_id:
        logger.warning(
            f"Bot joined unauthorized server <gid: {guild.id}> ({guild.name}). "
            f"Leaving immediately. Only server {allowed_server_id} is allowed."
        )
        try:
            await guild.leave()
            logger.info(f"Successfully left unauthorized server <gid: {guild.id}>")
        except Exception as e:
            logger.error(f"Failed to leave unauthorized server <gid: {guild.id}>: {e}", exc_info=True)
    else:
        logger.info(f"Bot joined authorized server <gid: {guild.id}> ({guild.name})")



def _main():
    from signal import SIGINT, SIGTERM

    loop = asyncio.get_event_loop()
    main_task = asyncio.ensure_future(main())
    for signal in [SIGINT, SIGTERM]:
        loop.add_signal_handler(signal, main_task.cancel)
    try:
        loop.run_until_complete(main_task)
    finally:
        loop.close()
        logging.shutdown()


if __name__ == '__main__':
    _main()
