
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
    
    # Migration: Add new columns if they don't exist
    try:
        c.execute("ALTER TABLE user_stats ADD COLUMN display_name TEXT")
    except sqlite3.OperationalError:
        pass 
    
    try:
        c.execute("ALTER TABLE user_stats ADD COLUMN avatar_hash TEXT")
    except sqlite3.OperationalError:
        pass

    conn.commit()
    conn.close()

init_db()

# --- Tracking Logic ---
class VoiceTrackerBot(discord.Client):
# ... (rest of class init) ...

# ... (inside background_updater) ...
                # 1. Calculate deltas in memory
                for user_id, session in list(self.active_sessions.items()):
                    delta = now - session['last_update']
                    if delta > 0:
                        # Try to get Member object for guild-specific info
                        try:
                            channel = self.get_channel(session['channel'])
                            if channel and channel.guild:
                                member = channel.guild.get_member(user_id)
                            else:
                                member = self.get_user(user_id)
                        except:
                            member = self.get_user(user_id)
                            
                        username = member.name if member else "Unknown"
                        display_name = member.display_name if member else username
                        
                        # Get Avatar Hash
                        avatar_hash = None
                        if member:
                            if hasattr(member, 'avatar') and member.avatar:
                                avatar_hash = member.avatar.key
                            elif hasattr(member, 'display_avatar') and member.display_avatar:
                                avatar_hash = member.display_avatar.key
                        
                        updates.append({
                            'user_id': user_id,
                            'username': username,
                            'display_name': display_name,
                            'avatar_hash': avatar_hash,
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
                                    INSERT INTO user_stats (user_id, username, display_name, avatar_hash, total_study_seconds, total_cam_seconds, total_stream_seconds)
                                    VALUES (?, ?, ?, ?, 0, 0, 0)
                                ''', (u['user_id'], u['username'], u['display_name'], u['avatar_hash']))
                            
                            # Update total
                            c.execute('''
                                UPDATE user_stats 
                                SET username = ?, display_name = ?, avatar_hash = ?, total_study_seconds = total_study_seconds + ?, last_updated = CURRENT_TIMESTAMP 
                                WHERE user_id = ?
                            ''', (u['username'], u['display_name'], u['avatar_hash'], u['delta'], u['user_id']))
                            
                            # Update cam
                            if u['cam']:
                                c.execute('UPDATE user_stats SET total_cam_seconds = total_cam_seconds + ? WHERE user_id = ?', (u['delta'], u['user_id']))
                            
                            # Update stream
                            if u['stream']:
                                c.execute('UPDATE user_stats SET total_stream_seconds = total_stream_seconds + ? WHERE user_id = ?', (u['delta'], u['user_id']))
                        
                        conn.commit()
                        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        users_updated = ", ".join([u['username'] for u in updates])
                        print(f"[{timestamp}] 💾 Saved data for {len(updates)} users: {users_updated}")
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
                INSERT INTO user_stats (user_id, username, display_name, avatar_hash, total_study_seconds, total_cam_seconds, total_stream_seconds)
                VALUES (?, ?, ?, ?, 0, 0, 0)
            ''', (user_id, username, username, None))
        
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
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

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

        # 2. Determine New State and LOG CHANGES
        if after.channel is None:
            # User left voice
            if user_id in self.active_sessions:
                del self.active_sessions[user_id]
                print(f"[{timestamp}] 👋 {member.name} left voice channel.")
        else:
            # User joined or changed state (cam/stream)
            action = "joined"
            details = []
            
            if user_id in self.active_sessions:
                action = "updated"
            
            if after.self_video != before.self_video:
                status = "ON" if after.self_video else "OFF"
                details.append(f"Cam {status}")
            
            if after.self_stream != before.self_stream:
                status = "ON" if after.self_stream else "OFF"
                details.append(f"Share {status}")
            
            if not details and action == "joined":
                details.append("Voice Only")
                
            if details or action == "joined":
                print(f"[{timestamp}] 🎙️ {member.name} {action}: {', '.join(details)}")

            self.active_sessions[user_id] = {
                'last_update': now,
                'cam': after.self_video,
                'stream': after.self_stream,
                'channel': after.channel.id
            }

    # --- API Handlers ---
    def get_avatar_url(self, user_id, avatar_hash):
        if avatar_hash:
            return f"https://cdn.discordapp.com/avatars/{user_id}/{avatar_hash}.png?size=256"
        return None # Or default avatar url

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
                response_data = {
                    'user_id': data['user_id'],
                    'username': data['username'],
                    'displayName': data.get('display_name', data['username']),
                    'avatarUrl': self.get_avatar_url(data['user_id'], data.get('avatar_hash')),
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
                    'displayName': r.get('display_name', r['username']),
                    'avatarUrl': self.get_avatar_url(r['user_id'], r.get('avatar_hash')),
                    'totalTime': int(r['total_study_seconds'] * 1000),
                    'camTime': int(r['total_cam_seconds'] * 1000), 
                    'shareTime': int(r['total_stream_seconds'] * 1000)
                })
            return web.json_response(data)
        except Exception as e:
            return web.json_response({'error': str(e)}, status=500)

if __name__ == '__main__':
    client = VoiceTrackerBot()
    client.run(TOKEN)
