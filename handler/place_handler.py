import re
from re import IGNORECASE

from nonebot import NoneBot
from hoshino.typing import CQEvent
from .handle_utils import get_group_location, do_request
from ..const import *
from ..maij import sv
from ..http.http_client import client
from ..http.http_utils import get_json_data_from_response
from ..utils import format_local_date_time

re_maij = re.compile(r'(j|jr|几|几人|几卡|有几人|有多少人|有几卡)$', flags=IGNORECASE)
re_put_maij = re.compile(r'(([+-][1-9][0-9]*卡)|(\+\+|--))$')
re_set_maij = re.compile(r'(=(0|([1-9][0-9]*))卡)$')


# 查询机厅几卡
@sv.on_rex(re_maij)
async def handle_maij(
        bot: NoneBot,
        event: CQEvent,
):
    location = get_group_location(event.group_id)
    msg = event.message.extract_plain_text().strip()
    place_name = msg[:-len(re_maij.findall(msg)[0])]

    ##########
    async def do():
        response = client.get(url=f'{API_URL}/place/{location}/{place_name}')
        data = get_json_data_from_response(response)
        await bot.send(event, f'''{data["placeName"]}的当前卡数为{data["cardCount"]}
上次更新时间为{format_local_date_time(data["updateTime"])}''', at_sender=True)

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
    operate_count = re_put_maij.findall(msg)[0][0]
    place_name = msg[:-len(operate_count)]
    if operate_count == '++':
        operate_count = '+1卡'
    elif operate_count == '--':
        operate_count = '-1卡'
    operate_count = int(operate_count[:-1])

    ##########
    async def do():
        response = client.put(url=f'{API_URL}/place/{location}/{place_name}', json={
            "qqId": event.user_id,
            "qqGroupId": event.group_id,
            "operateCount": operate_count
        })
        data = get_json_data_from_response(response)
        await bot.send(event,
                       f'''成功在{place_name}的队伍中{"添加" if operate_count > 0 else "移除"}{abs(operate_count)}张卡
当前排卡数为{data["cardCount"]}''', at_sender=True)

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
    operate_count = re_set_maij.findall(msg)[0][0]
    place_name = msg[:-len(operate_count)]
    operate_count = int(operate_count[1:-1])

    ##########
    async def do():
        response = client.put(url=f'{API_URL}/place/{location}/{place_name}/set', json={
            "qqId": event.user_id,
            "qqGroupId": event.group_id,
            "operateCount": operate_count
        })
        data = get_json_data_from_response(response)
        await bot.send(event, f'''成功将{place_name}的队伍设置为{operate_count}张卡
当前排卡数为{data["cardCount"]}''', at_sender=True)

    ##########

    await do_request(bot, event, place_name, do)
