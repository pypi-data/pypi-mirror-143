<!--
 * @Author         : mengshouer
 * @Date           : 2021-03-16 00:00:00
 * @LastEditors    : mengshouer
 * @LastEditTime   : 2021-03-16 00:00:00
 * @Description    : None
 * @GitHub         : https://github.com/mengshouer/nonebot_plugin_analysis_bilibili
-->

<p align="center">
  <a href="https://v2.nonebot.dev/"><img src="https://v2.nonebot.dev/logo.png" width="200" height="200" alt="nonebot"></a>
</p>

<div align="center">

# nonebot_plugin_analysis_bilibili


_✨ NoneBot bilibili视频、番剧解析插件 ✨_

</div>

<p align="center">
  <a href="https://raw.githubusercontent.com/cscs181/QQ-Github-Bot/master/LICENSE">
    <img src="https://img.shields.io/github/license/cscs181/QQ-Github-Bot.svg" alt="license">
  </a>
  <a href="https://pypi.python.org/pypi/nonebot-plugin-analysis-bilibili">
    <img src="https://img.shields.io/pypi/v/nonebot-plugin-analysis-bilibili.svg" alt="pypi">
  </a>
  <img src="https://img.shields.io/badge/python-3.8+-blue.svg" alt="python">
</p>

## 使用方式
私聊或群聊发送bilibili的小程序/链接

## 安装
1. 使用nb-cli安装，不需要手动添加入口，更新使用pip
```
nb plugin install nonebot_plugin_analysis_bilibili
```
2. 使用pip安装和更新，初次安装需要手动添加入口
```
pip install --upgrade nonebot_plugin_analysis_bilibili
```
pip安装后在 Nonebot2 入口文件（例如 bot.py ）增加：
``` python
nonebot.load_plugin("nonebot_plugin_analysis_bilibili")
```

附：[NekoAria的带图片版本(不支持a16)](https://github.com/NekoAria/nonebot_plugin_analysis_bilibili)
