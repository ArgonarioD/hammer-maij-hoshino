import re

from nonebot import NoneBot
from hoshino.typing import CQEvent

from ..maij import sv
from .handle_utils import get_group_location, do_request, end_line
from ..const import *
from ..utils import format_local_date_time, get_qq_nickname_with_group, build_announcement_list_str
from ..http.http_client import client
from ..http.http_utils import get_json_data_from_response

re_log = re.compile(r'(.+?)都?有谁$')

@sv.on_rex(re_log)
async def handle_maij_log(bot: NoneBot, event: CQEvent):
    location = get_group_location(event.group_id)
    msg = event.message.extract_plain_text().strip()
    match_result = re_log.match(msg)
    place_name = match_result[1].strip()

    ###########
    async def do():
        response = client.get(url=f'{API_URL}/place/{location}/{place_name}/log')
        data = get_json_data_from_response(response)
        if data['total'] == 0:
            result = f"{data['placeName']}目前还没有人排过卡"
        else:
            result_list = [
                ' - {} 在{}{}{}张卡，卡数变为{}'.format(
                    await get_qq_nickname_with_group(bot, r['qqId'], event.group_id, r['qqGroupId']),
                    format_local_date_time(r['createTime']),
                    '添加' if r['operateCount'] > 0 else '移除',
                    abs(r['operateCount']),
                    r['afterCount']
                ) for r in data['records']
            ]
            result = f"{data['placeName']}的卡数变更记录如下：\n{end_line.join(result_list)}".strip()

        await bot.send(event, f"{result}\n\n{await build_announcement_list_str(bot, event, data['announcements'])}".strip(), at_sender=True)

    ###########

    await do_request(bot, event, place_name, do)
