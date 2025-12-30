# Implementation Plan - Optimize Leaderboard Image Reliability

The goal is to ensure the leaderboard image is sent reliably even on weak VPS instances where rendering might take longer than the default timeouts.

## User Review Required
> [!IMPORTANT]
> I will be increasing the default timeouts significantly (from 30s to 300s) to accommodate slow rendering.
> I will also add retry logic for the image rendering process.

## Proposed Changes

### [GUI Client]
#### [MODIFY] [client.py](file:///Users/binh/StudyLion/src/gui/client.py)
- Increase `connection_timeout` from 30 to 120 seconds.
- Increase `request_expiry` from 30 to 300 seconds.
- Log a warning if rendering takes longer than 60 seconds.

### [Bot Logic]
#### [MODIFY] [leaderboard_only_bot.py](file:///Users/binh/StudyLion/leaderboard_only_bot.py)
- In `render_leaderboard_image`:
    - Add acceptable `timeout=300` to `gui_client.request` call.
    - Implement a retry loop (3 attempts) for the rendering request.
    - Catch `asyncio.TimeoutError` specifically and log it.
- In `upscale` section:
    - Add a fallback: if `LANCZOS` (high quality) fails or takes too long (though we can't easily measure inside synchronization), we might consider `BICUBIC` or just skipping upscale if it fails. For now, just wrapping it in a robust try/except block is good, which is already there, but we can improve logging.

## Verification Plan

### Automated Tests
- I cannot run automated tests for the GUI socket interaction easily without the full environment running.

### Manual Verification
- The user will need to run the bot and observe `pm2 logs`.
- Trigger the command `/bangxephang` and see if it completes even if it takes time.
- I will simulate a "slow" render by observing if the log shows "Rendering request...' and validating it doesn't timeout immediately.
