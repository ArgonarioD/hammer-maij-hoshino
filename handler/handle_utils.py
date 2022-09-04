import traceback

from nonebot import NoneBot
from hoshino.typing import CQEvent

from ..http.response_exception import NotFoundError, MultipleChoicesError, ResponseError

from ..utils import format_local_date_time
from ..maij_config import plugin_config

end_line = '\n'


def get_group_location(group_id: int):
    if group_id not in plugin_config.group_location:
        raise ValueError('本群尚未配置地区')
    return plugin_config.group_location[group_id]


def get_place_list_str(places) -> str:
    result_list = [f'- {place["placeName"]}：{place["cardCount"]} ({format_local_date_time(place["updateTime"])})'
                   for place in places]
    return end_line.join(result_list)


async def do_request(bot: NoneBot, ev: CQEvent, place_name: str, func, handle_not_found: bool = False):
    try:
        await func()
    except NotFoundError:
        if handle_not_found:
            await bot.send(ev, f'找不到{place_name}所对应的机厅', at_sender=True)
    except MultipleChoicesError as me:
        await bot.send(ev, f'''找到了多个匹配您所说的地名{place_name}对应的地点，请用更具体一点的名称进行查询
匹配到的地点全称如下：
{end_line.join([f" - {s}" for s in me.choices])}''', at_sender=True)
    except ResponseError as rese:
        await bot.send(ev, f'{rese.message}', at_sender=True)
    except RuntimeError:
        await bot.send(ev, '出了点小错误，请稍后再试！', at_sender=True)
        traceback.print_exc()
