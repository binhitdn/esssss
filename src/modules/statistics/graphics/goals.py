from datetime import timedelta
from psycopg.sql import SQL

from data import NULL
from meta import LionBot
from gui.cards import WeeklyGoalCard, MonthlyGoalCard
from gui.base import CardMode
# Tracking modules đã bị xóa
# from tracking.text.data import TextTrackerData
# Schedule module đã bị xóa
# from modules.schedule.lib import time_to_slotid

from .. import logger
from ..data import StatsData
from ..lib import extract_weekid, extract_monthid, apply_week_offset, apply_month_offset


async def get_goals_card(
    bot: LionBot, userid: int, guildid: int, offset: int, weekly: bool, mode: CardMode
):
    data: StatsData = bot.get_cog('StatsCog').data

    lion = await bot.core.lions.fetch_member(guildid or 0, userid)
    luser = lion.luser
    if guildid:
        user = await lion.fetch_member()
    else:
        user = await bot.fetch_user(userid)

    today = lion.today

    # Calculate periodid and select the correct model
    if weekly:
        goal_model = data.WeeklyGoals
        tasks_model = data.WeeklyTasks
        start = today - timedelta(days=today.weekday())
        start, end = apply_week_offset(start, offset), apply_week_offset(start, offset - 1)
        periodid = extract_weekid(start)
        key = {'guildid': guildid or 0, 'userid': userid, 'weekid': periodid}
    else:
        goal_model = data.MonthlyGoals
        tasks_model = data.MonthlyTasks
        start = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        start, end = apply_month_offset(start, offset), apply_month_offset(start, offset - 1)
        periodid = extract_monthid(start)
        key = {'guildid': guildid or 0, 'userid': userid, 'monthid': periodid}

    # Extract goals and tasks
    # TODO: Major data model fixy fixy here
    if guildid:
        goals = await goal_model.fetch_or_create(*key.values())
    else:
        goals = await goal_model.fetch(*key.values())
        if not goals:
            from collections import defaultdict
            goals = defaultdict(lambda: 0)

    task_rows = await tasks_model.fetch_where(**key)
    tasks = [(i, row.content, bool(row.completed)) for i, row in enumerate(task_rows)]

    # Tasklist module đã bị xóa - disable task completion tracking
    tasks_completed = 0

    # Set and compute correct middle goal column
    if mode in (CardMode.VOICE, CardMode.STUDY):
        model = data.VoiceSessionStats
        middle_completed = int((await model.study_times_between(guildid or None, userid, start, end))[0] // 3600)
        middle_goal = goals['study_goal']
    elif mode is CardMode.TEXT:
        # Tracking module đã bị xóa - disable text tracking
        middle_goal = goals.get('message_goal', 0)
        middle_completed = 0

    # Schedule module đã bị xóa - disable attendance tracking
    attendance = None

    # Get member profile
    if user:
        username = (user.display_name, user.discriminator)
        avatar = user.avatar.key if user.avatar else user.default_avatar.key
    else:
        username = (lion.data.display_name, '#????')
        avatar = luser.data.avatar_hash

    # Getch badges
    badges = await data.ProfileTag.fetch_tags(guildid, userid)

    card_cls = WeeklyGoalCard if weekly else MonthlyGoalCard

    skin = await bot.get_cog('CustomSkinCog').get_skinargs_for(
        guildid, userid, card_cls.card_id
    )

    card = card_cls(
        name=username[0],
        discrim=username[1],
        avatar=(userid, avatar),
        badges=badges,
        tasks_done=tasks_completed,
        tasks_goal=goals['task_goal'],
        studied_hours=middle_completed,
        studied_goal=middle_goal,
        attendance=attendance,
        goals=tasks,
        date=today,
        skin=skin | {'mode': mode}
    )
    return card
