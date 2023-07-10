import re

from nonebot import NoneBot

from hoshino.typing import CQEvent
from .handle_utils import get_group_location, do_request
from ..const import *
from ..http.http_client import client
from ..http.http_utils import get_json_data_from_response
from ..maij import sv
from ..utils import build_announcement_str

re_add_announcement = re.compile(r'^(?:添加(?:一[个条])?|[加发]一?[个条])公告 (.+?)\s(.+)')
re_renewal_announcement = re.compile(r'^续一?[续下发]公告 (.+?) (\d+)')
re_delete_announcement = re.compile(r'^(?:[删移]除(?:一[个条])?|删一?[个条])公告 (.+?) (\d+)')


@sv.on_rex(re_add_announcement)
async def handle_add_announcement(
        bot: NoneBot,
        event: CQEvent,
):
    location = get_group_location(event.group_id)
    msg = event.message.extract_plain_text().strip()
    match_result = re_add_announcement.match(msg)
    place_name = match_result[1].strip()
    content = match_result[2].strip()

    ###########
    async def do():
        response = client.post(url=f'{API_URL}/place/{location}/{place_name}/announcement', json={
            'uploaderId': event.user_id,
            'uploaderGroupId': event.group_id,
            'announcementContent': content
        })
        data = get_json_data_from_response(response)
        await bot.send(event, f'''成功为{data["place"]["placeName"]}创建公告，公告内容如下：
{await build_announcement_str(bot, event, data)}'''.strip(), at_sender=True)

    ###########

    await do_request(bot, event, place_name, do)


@sv.on_rex(re_renewal_announcement)
async def handle_renewal_announcement(
        bot: NoneBot,
        event: CQEvent,
):
    location = get_group_location(event.group_id)
    msg = event.message.extract_plain_text().strip()
    match_result = re_renewal_announcement.match(msg)
    place_name = match_result[1].strip()
    try:
        announcement_id = int(match_result[2].strip())
    except ValueError:
        await bot.send(event, '请输入正确的公告ID。', at_sender=True)
        return

    ###########
    async def do():
        response = client.put(
            url=f'{API_URL}/place/{location}/{place_name}/announcement/{announcement_id}/renewal',
            json={
                "operatorId": event.user_id,
            })
        data = get_json_data_from_response(response)
        await bot.send(event, f'''成功为{data["place"]["placeName"]}的第{data["announcementId"]}号公告续期一周，其内容如下：
{await build_announcement_str(bot, event, data)}'''.strip(), at_sender=True)

    ###########

    await do_request(bot, event, place_name, do)


@sv.on_rex(re_delete_announcement)
async def handle_delete_announcement(
        bot: NoneBot,
        event: CQEvent,
):
    location = get_group_location(event.group_id)
    msg = event.message.extract_plain_text().strip()
    match_result = re_delete_announcement.match(msg)
    place_name = match_result[1].strip()
    try:
        announcement_id = int(match_result[2].strip())
    except ValueError:
        await bot.send(event, '请输入正确的公告ID。', at_sender=True)
        return

    ###########
    async def do():
        response = client.request('DELETE',
            url=f'{API_URL}/place/{location}/{place_name}/announcement/{announcement_id}',
            json={
                "deleterId": event.user_id,
            })
        data = get_json_data_from_response(response)
        await bot.send(event, f'''成功为{data["place"]["placeName"]}删除了第{data["announcementId"]}号公告，其内容如下：
{await build_announcement_str(bot, event, data)}'''.strip(), at_sender=True)

    ###########

    await do_request(bot, event, place_name, do)
