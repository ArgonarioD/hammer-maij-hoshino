import traceback
from io import StringIO

from aiocqhttp import ActionFailed
from hoshino.typing import CQEvent
from nonebot import NoneBot


def format_local_date_time(time, full_datetime: bool = False) -> str:
    if len(time) < 6:
        time.append(0)
    if full_datetime:
        return f'{time[0]}年{time[1]}月{time[2]}日 {time[3]}:{time[4]:02}:{time[5]:02}'
    else:
        return f'{(24 if time[3] <= 4 else 0) + time[3]}:{time[4]:02}:{time[5]:02}'


# 来自开源库nonebot-plugin-hammer-core，仓库地址https://github.com/ArgonarioD/nonebot-plugin-hammer-core，有用的话欢迎点个Star QwQ
async def get_qq_nickname_with_group(
        bot: NoneBot,
        user_id: int,
        current_group_id: int,
        target_group_id: int = None,
        pattern: str = '{nickname}{qq_id}{target_group}',
        target_group_pattern: str = ' @{target_group_name}'
) -> str:
    if target_group_id is None:
        target_group_id = current_group_id

    try:
        info = await bot.get_group_member_info(group_id=current_group_id, user_id=user_id)
        # if the same group
        if len(info['card'].strip()) == 0:
            nickname = info['nickname']
        else:
            nickname = info['card'].strip()
        return pattern.replace('{target_group}', '').replace('{nickname}', nickname).replace('{qq_id}', f'({user_id})')
    except ActionFailed as exc:
        if exc.retcode == 100:
            # if not the same group
            info = await bot.get_stranger_info(user_id=user_id)
            return await __stranger_convert(bot, info['nickname'], target_group_id, pattern, target_group_pattern)
        else:
            traceback.print_exc()


async def __stranger_convert(
        bot: NoneBot,
        nickname: str,
        target_group_id: int,
        pattern: str,
        target_group_pattern: str
) -> str:
    group_info = await bot.get_group_info(group_id=target_group_id)
    return pattern.replace('{nickname}', nickname) \
        .replace('{qq_id}', '') \
        .replace('{target_group}', target_group_pattern.replace('{target_group_name}', group_info['group_name']))


async def build_announcement_str(
        bot: NoneBot,
        event: CQEvent,
        announcement
) -> str:
    return f'''公告ID：{announcement["announcementId"]}
{announcement["announcementContent"]}
By {await get_qq_nickname_with_group(bot, announcement["uploaderId"], event.group_id, announcement["uploaderGroupId"])} {format_local_date_time(announcement["createTime"], True)} 将于{format_local_date_time(announcement["expireTime"], True)}过期'''.strip()

async def build_announcement_list_str(
        bot: NoneBot,
        event: CQEvent,
        announcements
) -> str:
    if len(announcements) == 0:
        return ''
    else:
        result = StringIO()
        result.write(f'该地点有{len(announcements)}条公告。\n')
        for announcement in announcements:
            result.write(await build_announcement_str(bot, event, announcement))
            result.write('\n')
        return result.getvalue()