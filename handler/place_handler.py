import re
from re import IGNORECASE

from nonebot import NoneBot
from hoshino.typing import CQEvent
from .handle_utils import get_group_location, do_request, get_place_list_str
from ..const import *
from ..maij import sv
from ..http.http_client import client
from ..http.http_utils import get_json_data_from_response
from ..utils import format_local_date_time, build_announcement_list_str

re_maij = re.compile(r'(.+?)(j|jr|几|有?(几|多少)[人卡])$', flags=IGNORECASE)
re_put_maij = re.compile(r'(.+?)( ?([+-] ?[1-9][0-9]*卡)|(\+\+|--))$')
re_set_maij = re.compile(r'(.+?)( ?= ?(0|([1-9][0-9]*))卡)$')


# 查询机厅几卡
@sv.on_rex(re_maij)
async def handle_maij(
        bot: NoneBot,
        event: CQEvent,
):
    location = get_group_location(event.group_id)
    msg = event.message.extract_plain_text().strip()
    match_result = re_maij.match(msg)
    place_name = match_result[1].strip()

    ##########
    async def do():
        response = client.get(url=f'{API_URL}/place/{location}/{place_name}')
        data = get_json_data_from_response(response)
        if not data['updated']:
            result = f'查询到{data["placeName"]}的卡数今天还没有被更新过。'
        else:
            result = f"查询到{data['placeName']}的当前卡数为{data['cardCount']}\n上次更新时间为{format_local_date_time(data['updateTime'])}"

        await bot.send(event, f'{result.strip()}\n\n{await build_announcement_list_str(bot, event, data["announcements"])}'.strip(),
                       at_sender=True)

    ##########

    await do_request(bot, event, place_name, do)


# 机厅卡数更新
@sv.on_rex(re_put_maij)
async def handle_put_maij(
        bot: NoneBot,
        event: CQEvent,
):
    location = get_group_location(event.group_id)
    msg = event.message.extract_plain_text().strip()
    match_result = re_put_maij.match(msg)
    place_name = match_result[1].strip()
    mutate_str = match_result[2].strip()
    if '++' in mutate_str:
        mutate_str = '+1卡'
    elif '--' in mutate_str:
        mutate_str = '-1卡'
    operate_count = int(mutate_str.replace(' ','')[:-1])

    ##########
    async def do():
        response = client.put(url=f'{API_URL}/place/{location}/{place_name}', json={
            "qqId": event.user_id,
            "qqGroupId": event.group_id,
            "operateCount": operate_count
        })
        data = get_json_data_from_response(response)
        await bot.send(event,
                       f'''成功在{data["placeName"]}的队伍中{"添加" if operate_count > 0 else "移除"}{abs(operate_count)}张卡
当前排卡数为{data["cardCount"]}

{await build_announcement_list_str(bot, event, data["announcements"])}'''.strip(), at_sender=True)

    ##########

    await do_request(bot, event, place_name, do, handle_not_found=True)


# 设置机厅卡数
@sv.on_rex(re_set_maij)
async def handle_set_maij(
        bot: NoneBot,
        event: CQEvent,
):
    location = get_group_location(event.group_id)
    msg = event.message.extract_plain_text().strip()
    match_result = re_set_maij.match(msg)
    place_name = match_result[1].strip()
    operate_count = int(match_result[2].strip())

    ##########
    async def do():
        response = client.put(url=f'{API_URL}/place/{location}/{place_name}/set', json={
            "qqId": event.user_id,
            "qqGroupId": event.group_id,
            "operateCount": operate_count
        })
        data = get_json_data_from_response(response)
        await bot.send(event, f'''成功将{data["placeName"]}的队伍设置为{data["cardCount"]}张卡
        
{await build_announcement_list_str(bot, event, data["announcements"])}'''.strip(), at_sender=True)

    ##########

    await do_request(bot, event, place_name, do)


@sv.on_fullmatch('机厅列表')
async def handle_place_asc_list(
        bot: NoneBot,
        event: CQEvent,
):
    location = get_group_location(event.group_id)

    ##########
    async def do():
        response = client.get(url=f'{API_URL}/place/list/{location}')
        data = get_json_data_from_response(response)
        await bot.send(
            event, f'''自今日API初始化后，{location}共有{data['total']}所机厅的卡数被更新过，按其当前卡数的正序、更新时间的倒序的排列如下：
{get_place_list_str(data['records'])}'''.strip(), at_sender=True)

    ##########

    await do_request(bot, event, location, do)
