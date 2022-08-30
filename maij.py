from hoshino import Service, priv
from hoshino.log import new_logger

sv_help = '''maij.设置本群地区 <省市名> 为该群设置固定地区，其中省市名必须为API中收录的省市，且必须为如`安徽省合肥市`的标准写法，对于收录省市列表相关信息请查看API文档
<机厅名称>j/jr/几/几人/几卡/有几人/有多少人/有几卡 查询指定机厅中的排卡数
<机厅名称>+/-<数字>卡 为指定机厅添加/移除指定排卡数
<机厅名称>++/-- 为指定机厅添加/移除一张卡
<机厅名称>=<数字>卡 将指定机厅设置为指定排卡数
<机厅名称>有谁 查询今日指定机厅的排卡数变更记录
本查卡API为开放API，欢迎接入使用，文档地址https://docs.hammer-hfut.tk:233/maij/'''

sv = Service('maij', manage_priv=priv.ADMIN, enable_on_default=False, help_=sv_help)
log = new_logger('maij')
