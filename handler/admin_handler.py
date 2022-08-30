from nonebot import on_command, CommandSession
from nonebot.permission import GROUP_ADMIN

from ..const import *
from ..http.http_client import client
from ..http.http_utils import get_json_data_from_response
from ..maij_config import plugin_config


@on_command('maij.设置本群地区', permission=GROUP_ADMIN, only_to_me=False, shell_like=True)  # maij.设置本群地区 <省市名>
async def handle_configure_group(session: CommandSession):
    if len(session.argv) != 1:
        await session.finish('格式有误，请使用"maij.设置本群地区 <省市名>"的格式')
    target_location = session.argv[0].strip()
    response = client.get(url=f'{API_URL}/place/supported')
    data = get_json_data_from_response(response)
    if len(list(filter(lambda l: l['cityName'] == target_location, data['records']))) == 0:
        await session.finish(
            'Hammer-MaiJ API暂不支持本城市，请查阅文档（https://docs.hammer-hfut.tk:233/maij/）确认支持的城市进行更正或阅读“令本服务支持其他地区”一节进行添加申请')

    plugin_config.group_location[session.event.group_id] = target_location
    plugin_config.write_to_disk()
    await session.finish(f"成功将本群的地区设置为{target_location}")
