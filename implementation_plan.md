# Implementation Plan - API Reliability

To ensure the bot works even when the network is unstable (e.g. temporary API downtime), I will add retry logic to the data fetching function.

## Proposed Changes

### [Bot Logic]
#### [MODIFY] [leaderboard_only_bot.py](file:///Users/binh/StudyLion/leaderboard_only_bot.py)
- In `fetch_leaderboard_data`:
    - Wrap the API call in a retry loop (5 attempts).
    - Add exponential backoff (wait 2s, 4s, 8s...) between retries.
    - Add specific timeout for the API request (e.g. 10s) to avoid hanging forever.

## Verification Plan
- Manual verification: The user can observe logs if the API is down, seeing "Retry attempt 1...", "Retry attempt 2...".
