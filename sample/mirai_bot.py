from distutils.log import debug
import json

import requests
from flask import Flask, request
from gevent import pywsgi

import chat_pipeline_manager
import config
from logger import logger

app = Flask(__name__)


def start_listen() -> None:
    # chat_pipeline_manager.init_chat_pipeline()
    server = pywsgi.WSGIServer(
        (config.mirai['callback_ip'], config.mirai['callback_port']),
        application=app, log=None
    )
    logger.info('port %d start listen', config.mirai['callback_port'])
    server.serve_forever()


# webhook
@app.route('/', methods=['POST'])
def deal_with_message() -> str:
    bin_data = request.get_data()
    try:
        data = json.loads(bin_data)
    except json.decoder.JSONDecodeError:
        logger.error('json请求无法解析：%s', bin_data)
        return json.dumps({"status": 0, "msg": "bad request"})
    else:
        logger.debug('receive msg: %s', json.dumps(data))
        msg_type: str = data.get('type')
        sender: dict = data.get('sender')
        msg_chain: list = data.get('messageChain')
        if msg_type in ['BotOnlineEvent', 'BotReloginEvent']:
            logger.info('mirai bot [%d] connected' % data.get('qq'))
            verify()
            bind()
            return json.dumps({"status": 1})
        elif msg_type in ['BotOfflineEventActive', 'BotOfflineEventForce', 'BotOfflineEventDropped']:
            logger.info('mirai bot [%d] disconnected' % data.get('qq'))
            release()
            return json.dumps({"status": 0, "msg": "bot logout"})

        if msg_type is None:
            logger.error("bad request")
            return json.dumps({"status": 0, "msg": "bad request"})
        if msg_type == 'GroupMessage':
            if str(sender['id']) != config.qq['robot_self_qq'] and str(sender['group']['id']) in config.qq['available_qq_group']:
                # chat_pipeline_manager.deal_with_msg(sender['group']['id'], sender['id'], msg_chain)
                print('deal_with_msg')
                ''' TODO
                deal_with_msg(sender['group']['id'], sender['id'], msg_chain)
                Args:
                    qq_group_number: int
                    qq: int
                    msg: list[MessageType]
                '''

            return json.dumps({"status": 1})
        elif msg_type == 'FriendMessage':
            pass    # TODO deal_with_msg
        elif msg_type == 'TempMessage':
            pass    # TODO deal_with_msg
    return json.dumps({"status": 1})


# mirai http 认证
def verify() -> bool:
    resp = requests.post(
        url=config.mirai['api_url']+'/verify',
        json={'verifyKey': config.mirai['verifyKey']}
    )
    logger.debug('verify, return: %s' % resp.text)
    if resp.status_code == 200 and json.loads(resp.text)['code'] == 0:
        config.mirai['session'] = json.loads(resp.text)['session']
        logger.debug('verify successful')
        return True
    else:
        logger.error('verify failed')
        return False


def bind() -> bool:
    resp = requests.post(
        url=config.mirai['api_url']+'/bind',
        json={
            'sessionKey': config.mirai['session'],
            'qq': config.qq['robot_self_qq']
        }
    )
    logger.debug('bind, return: %s' % resp.text)
    if not(resp.status_code == 200 and json.loads(resp.text)['code'] == 0):
        logger.error('bind failed')
        return False
    return True


def release() -> bool:
    resp = requests.post(
        url=config.mirai['api_url']+'/release',
        json={
            'sessionKey': config.mirai['session'],
            'qq': config.qq['robot_self_qq'],
        }
    )
    logger.debug('release, return %s' % resp.text)
    if not(resp.status_code == 200 and json.loads(resp.text)['code'] == 0):
        logger.error('release failed')
        return False
    return True


# 消息发送
def send_group_message(group: int,  msg_chain: list) -> None:
    if not bind():
        verify()
        bind()
    resp = requests.post(
        url=config.mirai['api_url']+'/sendGroupMessage',
        json={
            'sessionKey': config.mirai['session'],
            'target': group,
            'messageChain': msg_chain
        }
    )
    logger.debug('send group message, return: %s' % resp.text)
    if not(resp.status_code == 200 and json.loads(resp.text)['code'] == 0):
        logger.error('send group message failed, group: %d' % group)


def send_temp_message(qq: int, group: int, msg_chain: list) -> None:
    if not bind():
        verify()
        bind()
    resp = requests.post(
        url=config.mirai['api_url']+'/sendTempMessage',
        json={
            'sessionKey': config.mirai['session'],
            'qq': qq,
            'group': group,
            'messageChain': msg_chain
        }
    )
    logger.debug('send temp message, return: %s' % resp.text)
    if not(resp.status_code == 200 and json.loads(resp.text)['code'] == 0):
        logger.error(
            'send temp message failed, group: %d, target: %d' % (group, qq))


def send_friend_message(qq: int, msg_chain: list) -> None:
    if not bind():
        verify()
        bind()
    resp = requests.post(
        url=config.mirai['api_url']+'/sendFriendMessage',
        json={
            'sessionKey': config.mirai['session'],
            'qq': qq,
            'messageChain': msg_chain
        }
    )
    logger.debug('send temp message, return: %s' % resp.text)
    if not(resp.status_code == 200 and json.loads(resp.text)['code'] == 0):
        logger.error('send temp message failed, target: %d' % qq)
