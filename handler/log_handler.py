import traceback

from aiocqhttp import ActionFailed
from nonebot import NoneBot
from hoshino.typing import CQEvent

from ..maij import sv
from .handle_utils import get_group_location, do_request, end_line
from ..const import *
from ..utils import format_local_date_time
from ..http.http_client import client
from ..http.http_utils import get_json_data_from_response


@sv.on_suffix('有谁')
async def handle_maij_log(bot: NoneBot, event: CQEvent):
    location = get_group_location(event.group_id)
    place_name = event.message.extract_plain_text().strip()

    ###########
    async def do():
        response = client.get(url=f'{API_URL}/place/{location}/{place_name}/log')
        data = get_json_data_from_response(response)
        if data['total'] == 0:
            await bot.send(event, f"{data['placeName']}目前还没有人排过卡", at_sender=True)
            return
        result_list = [
            ' - {} 在{}{}{}张卡，卡数变为{}'.format(
                await get_qq_nickname_with_group(bot, r['qqId'], event.group_id, r['qqGroupId']),
                format_local_date_time(r['createTime']),
                '添加' if r['operateCount'] > 0 else '移除',
                abs(r['operateCount']),
                r['afterCount']
            ) for r in data['records']
        ]

        await bot.send(event, f"""{data['placeName']}的卡数变更记录如下
{end_line.join(result_list)}""", at_sender=True)

    ###########

    await do_request(bot, event, place_name, do)


# 来自开源库nonebot-plugin-hammer-core，仓库地址https://github.com/ArgonarioD/nonebot-plugin-hammer-core，有用的话欢迎点个Star QwQ
async def get_qq_nickname_with_group(
        bot: NoneBot,
        user_id: int,
        current_group_id: int,
        target_group_id: int = None,
        pattern: str = '{nickname}{qq_id}{target_group}',
        target_group_pattern: str = '(来自群“{target_group_name}”)'
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
