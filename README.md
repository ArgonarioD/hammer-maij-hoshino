<div align="center">

# Hammer-MaiJ Hoshino

✨ 基于HoshinoBot操作Hammer-MaiJ API的方便特定地区排卡的HoshinoBot插件 ✨
</div>

<p align="center">
  <a href="https://raw.githubusercontent.com/ArgonarioD/nonebot-plugin-hammer-nbnhhsh/main/LICENSE">
    <img src="https://img.shields.io/github/license/ArgonarioD/hammer-maij-hoshino" alt="license">
  </a>
  <img src="https://img.shields.io/badge/python-3.8+-blue.svg" alt="python">
  <img src="https://img.shields.io/badge/Onebot-v11-lightgrey" alt="onebot11">
</p>

## 前言

本插件中所接入的Hammer-MaiJ机厅查卡API为本人开发的开放API，欢迎接入使用：[API文档](https://docs.hammer-hfut.tk:233/maij)

## 使用本插件

1. 将本项目的文件夹放入HoshinoBot的`hoshino/modules`目录下（可以考虑直接在该目录下用如下命令将本仓库clone至该目录下）

```shell
git clone https://github.com/ArgonarioD/hammer-maij-hoshino
```

2. 一般情况下，利用包管理器在HoshinoBot的python环境下安装`httpx`库，如

```shell
pip install httpx==0.23.0
```

3. 在`hoshino/config/__bot__.py`中的"启用模块"中添加`"hammer-maij-hoshino"`
4. 用HoshinoBot自带的botmanage插件启用`maij`服务，一般情况下，只需要在机器人所在的群中使用如下指令

```
启用 maij
```

5. 在你想要启用本插件的群中使用指令`maij.设置本群地区 <省市名>`后即可正常使用（**注：关于本命令，请详细查看下方的“命令”章节**）

> 注：如果您的HoshinoBot中安装了由[@Yuri-YuzuChaN](https://github.com/Yuri-YuzuChaN)
> 开发的[maimaiDX插件](https://github.com/Yuri-YuzuChaN/maimaiDX)
> ，由于本插件的指令可能与该插件有冲突，所以建议在启用本插件前将该插件路径中的`maimaiDX/maimai.py`
> 中第787行至第815行（`arcade_person`与`arcade_query_person`两个函数）注释掉

## 功能

与其他前端（一般情况下为其他QQ群Bot）共用Hammer-MaiJ机厅查卡API

- 提交API收录的机厅中的人数供其他人查阅（+/-/=三种方式变更卡数）
- 查阅其他人提交的API收录的机厅中的人数
- 查阅机厅中卡数的变更记录（本群内存在的人显示QQ号，不在本群内存在的人显示提交时所在的QQ群名）
- 查询本城市中自当日API重置后所有更新过卡数的机厅按卡数正序排列、更新时间倒序排列的列表

## 命令

| 命令                              | 说明                                                                                 |
|---------------------------------|------------------------------------------------------------------------------------|
| maij.设置本群地区 <省市名>               | 为该群设置固定地区，若不设置则下列指令都无法执行；其中省市名必须为API中收录的省市，且必须为如`安徽省合肥市`的标准写法，对于收录省市列表相关信息请查看API文档 |
| 机厅列表                            | 查询本城市中自当日API重置后所有更新过卡数的机厅按卡数正序排列、更新时间倒序排列的列表                                       |
| <机厅名称>j/jr/几/几人/几卡/有几人/有多少人/有几卡 | 查询指定机厅中的排卡数                                                                        |
| <机厅名称>j/jr/几/几人/几卡/有几人/有多少人/有几卡 | 查询指定机厅中的排卡数                                                                        |
| <机厅名称>+/-<数字>卡                  | 为指定机厅添加/移除指定排卡数                                                                    |
| <机厅名称>++/--                     | 为指定机厅添加/移除一张卡                                                                      |
| <机厅名称>=<数字>卡                    | 将指定机厅设置为指定排卡数                                                                      |
| <机厅名称>有谁                        | 查询今日指定机厅的排卡数变更记录                                                                   |

## 更新日志
### v1.1.0 (*2022-09-04*)
#### Features
- 实现了“机厅列表”功能
### v1.0.1 (*2022-09-01*)
#### Bugs Fixed
- 更新卡数时机厅全名显示错误
### v1.0.0 (*2022-08-31*)
发布本项目
## 鸣谢

- [onebot](https://github.com/botuniverse/onebot)
- [HoshinoBot](https://github.com/Ice-Cirno/HoshinoBot)

---
~~*如果觉得有用的话求点个Star啵QwQ*~~