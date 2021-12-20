<div align="center">
  
# 东方Project沙包聚集地机器人
![](https://img.shields.io/github/languages/top/Touhou-Freshman-Camp/Touhou-Freshman-Camp-Robot "语言")
[![](https://img.shields.io/github/workflow/status/Touhou-Freshman-Camp/Touhou-Freshman-Camp-Robot/CodeQL)](https://github.com/FlyingLu/Touhou-Freshman-Camp-Robot/actions/workflows/codeql-analysis.yml "代码分析")
[![](https://img.shields.io/github/contributors/Touhou-Freshman-Camp/Touhou-Freshman-Camp-Robot)](https://github.com/FlyingLu/Touhou-Freshman-Camp-Robot/graphs/contributors "贡献者")
[![](https://img.shields.io/github/license/Touhou-Freshman-Camp/Touhou-Freshman-Camp-Robot)](https://github.com/FlyingLu/Touhou-Freshman-Camp-Robot/blob/master/LICENSE "许可协议")
</div>
  
这是东方Project沙包聚集地（以下简称“红群”）的机器人，基于`Python3`编写

## 声明
* **本项目采用`AGPLv3`协议开源，任何间接接触本项目的软件也要求使用`AGPLv3`协议开源**
* **不鼓励，不支持一切商业用途**
* **由于使用本项目提供的接口、文档等造成的不良影响和后果与本人和红群无关**
* 由于本项目的特殊性，可能随时停止开发或删档
* 本项目为开源项目，不接受任何的催单和索取行为

## 架构
整个框架包含以下三个部分：
* QQ登录部分使用的是MyQQ框架的HTTPAPI，官网：https://www.myqqx.com/
* Bilibili登录和开播部分是自己实现的，直接调用Bilibili的API接口：https://github.com/SocialSisterYi/bilibili-API-collect
* 权限管理部分，在程序内部维护了一个`dict`实现
* 消息处理部分

当收到消息时，消息将会被`chat_pipeline.py`里的`pipelines`中的所有消息处理器依次处理，机器人将会作出相应的反应。
默认已经提供了一个`MessagePipeline`，对群聊中的指令进行处理，详细可以参考`message`开头的文件。

## 安装方法
1. 安装python包依赖
```bash
pip install -r requirements.txt
```
2. 下载并安装MyQQ，并安装MyQQ的HTTPAPI插件，登录机器人QQ号
3. 将`config.py.template`重命名为`config.py`，并进行配置，注意要与myqq的回调和监听端口对应上
4. 运行main.py

## 后续优化
考虑到MyQQ框架并不算很稳定，我们已切出另一个Mirai分支，并支持了Mirai登录QQ和收发消息的功能。

## 主要开发人员
| 人员 | 功能 |
| ---- | ---- |
| 奇葩の灵梦 | 框架搭建、myqq接入、B站API接入、预约功能、投票功能  |
| 東方妖ゝ夢 | mirai接入 |
| Phiomoe | 打断复读功能 |
| Death | B站视频推送功能 |
