import json
import logging

import config
from flask import Flask, request

app = Flask(__name__)


# 启动MyQQ的HTTP回调接口
def start_listen():
    app.run(
        host=config.myqq['callback_ip'],
        port=config.myqq['callback_port'],
        debug=config.debug_mode
    )


# HTTP回调接口的定义
@app.route('/', methods=['POST'])
def deal_with_message():
    data = request.json
    if not ('MQ_fromQQ' in data and 'MQ_fromID' in data and 'MQ_msg' in data):
        return json.dumps({"status": 0, "msg": "bad request"})
    from_qq = data['MQ_fromQQ']
    if from_qq != config.qq['robot_self_qq'] and data['MQ_fromID'] in config.qq['available_qq_group']:
        msg = data['MQ_msg']
        logging.info("%s：%s", from_qq, msg)
        msg.split('+')  # MyQQ会自动把空格转为加号，所以这里要用+分隔
    return json.dumps({"status": 1})
