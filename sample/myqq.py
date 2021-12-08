import json
import urllib.parse

import requests
from flask import Flask, request
from gevent import pywsgi

import chat_pipeline_manager
import config
from logger import logger

app = Flask(__name__)


# 启动MyQQ的HTTP回调接口
def start_listen() -> None:
    chat_pipeline_manager.init_chat_pipeline()
    server = pywsgi.WSGIServer((config.myqq['callback_ip'], config.myqq['callback_port']), app, log=None)
    logger.info('port %d start listen', config.myqq['callback_port'])
    server.serve_forever()


# HTTP回调接口的定义
@app.route('/', methods=['POST'])
def deal_with_message() -> str:
    bin_data = request.get_data()
    try:
        data = json.loads(bin_data)
    except json.decoder.JSONDecodeError:
        logger.error('json请求无法解析：%s', bin_data)
        return json.dumps({"status": 0, "msg": "bad request"})
    if data.get('MQ_type') != 2:
        return json.dumps({"status": 1})
    from_qq = data.get('MQ_fromQQ')
    from_id = data.get('MQ_fromID')
    msg = urllib.parse.unquote(data.get('MQ_msg'))
    if from_qq is None or from_id is None or msg is None:
        logger.error("bad request")
        return json.dumps({"status": 0, "msg": "bad request"})
    if from_qq != config.qq['robot_self_qq'] and from_id in config.qq['available_qq_group']:
        chat_pipeline_manager.deal_with_msg(from_id, from_qq, msg)
    return json.dumps({"status": 1})


def send_group_message(qq_group_number: str, msg: str) -> None:
    resp = requests.post(config.myqq['api_url'], json={
        'function': 'Api_SendMsg',
        'token': config.myqq['token'],
        'params': {'c1': config.qq['robot_self_qq'], 'c2': '2', 'c3': qq_group_number, 'c5': msg}
    })
    logger.debug('send group message, return: %s', resp.content.decode('utf-8'))
    if resp.status_code != 200:
        logger.error('send group message failed, qq_group_number: %s', qq_group_number)


def send_private_message(qq_group_number: str, qq: str, msg: str) -> None:
    resp = requests.post(config.myqq['api_url'], json={
        'function': 'Api_SendMsg',
        'token': config.myqq['token'],
        'params': {'c1': config.qq['robot_self_qq'], 'c2': '4', 'c3': qq_group_number, 'c4': qq, 'c5': msg}
    })
    logger.debug('send private message, return: %s', resp.content.decode('utf-8'))
    if resp.status_code != 200:
        logger.error('send private message failed, qq_group_number: %s', qq_group_number)


# 无用的接口，发送图片可以直接使用[pic=http://www.myqq.com]，后接本地路径或者url都行
# def upload_pic(qq_group_number: str, pic_url: str) -> str:
#     resp = requests.post(config.myqq['api_url'], json={
#         'function': 'Api_UpLoadPic',
#         'token': config.myqq['token'],
#         'params': {'c1': config.qq['robot_self_qq'], 'c2': '2', 'c3': qq_group_number, 'c4': pic_url}
#     })
#     ret_str = resp.content.decode('utf-8')
#     logger.debug('upload pic, return: %s', ret_str)
#     if resp.status_code != 200:
#         logger.error('upload pic failed, qq_group_number: %s', qq_group_number)
#         return ''
#     ret = json.loads(ret_str)
#     if ret['code'] != 200:
#         logger.error('upload pic failed, qq_group_number: %s, error code: %d, error msg: %s', qq_group_number,
#                      ret['code'], ret['msg'])
#         return ''
#     return ret['data']['ret']
