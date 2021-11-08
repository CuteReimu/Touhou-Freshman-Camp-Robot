import json
import logger
import config
import requests
from message import Dispatcher
from flask import Flask, request
from gevent import pywsgi

app = Flask(__name__)
dispatcher = Dispatcher()


# 启动MyQQ的HTTP回调接口
def start_listen():
    server = pywsgi.WSGIServer((config.myqq['callback_ip'], config.myqq['callback_port']), app, log=None)
    logger.info('port %d start listen', config.myqq['callback_port'])
    server.serve_forever()


# HTTP回调接口的定义
@app.route('/', methods=['POST'])
def deal_with_message():
    bin_data = ''
    for m in request.form:
        bin_data = m
    if bin_data == '':
        logger.error("bad request")
        return json.dumps({"status": 0, "msg": "bad request"})
    data = json.loads(bin_data)
    from_qq = data.get('MQ_fromQQ')
    from_id = data.get('MQ_fromID')
    msg = data.get('MQ_msg')
    if from_qq is None or from_id is None or msg is None:
        logger.error("bad request")
        return json.dumps({"status": 0, "msg": "bad request"})
    if from_qq != config.qq['robot_self_qq'] and from_id in config.qq['available_qq_group']:
        arr = msg.split('+')  # MyQQ会自动把空格转为加号，所以这里要用+分隔
        d = dispatcher.messages.get(arr[0])
        if d is not None and d.check_auth(from_qq):
            logger.info("%s说：%s", from_qq, msg)
            d.execute(from_qq, arr[1:])
    return json.dumps({"status": 1})


def send_group_message(qq_group_number: str, msg: str):
    data = json.dumps({
        'function': 'Api_SendMsg',
        'token': config.myqq['token'],
        'params': {'c1': config.qq['robot_self_qq'], 'c2': '2', 'c3': qq_group_number, 'c5': msg}
    })
    logger.debug('post message: %s', data)
    resp = requests.request(method='POST', url='http://localhost:10100/MyQQHTTPAPI', data=data,
                            headers={'content-type': 'application/json'})
    # resp = requests.post('http://localhost:10100/MyQQHTTPAPI', json={
    #     'function': 'Api_SendMsg',
    #     'token': config.myqq['token'],
    #     'params': {'c1': config.qq['robot_self_qq'], 'c2': '2', 'c3': qq_group_number, 'c5': msg}
    # })
    if resp.status_code != 200:
        logger.error('send group message failed, qq_group_number: %s', qq_group_number)
