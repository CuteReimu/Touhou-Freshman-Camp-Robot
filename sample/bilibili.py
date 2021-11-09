import json
from sys import stdin

import requests
import requests.utils
import rsa

import config
import logger


def encrypt(public_key: bytes, data: bytes) -> bytes:
    pub_key = rsa.PublicKey.load_pkcs1_openssl_pem(public_key)
    return rsa.encrypt(data, pub_key)


def get_live_url() -> str:
    return 'https://live.bilibili.com/' + config.bilibili['room_id']


class Bilibili:
    def __init__(self):
        self.cookies = {}

    def login(self):
        if len(self.cookies) != 0:
            return
        resp = requests.get('https://passport.bilibili.com/web/captcha/combine?plat=6')
        if resp.status_code != 200:
            logger.error('login failed, status code: %d', resp.status_code)
            return
        login_resp = json.loads(resp.content.decode('utf-8'))
        if login_resp['code'] != 0:
            logger.error('登录bilibili获取人机校验失败, code: %d', login_resp['code'])
        gt = login_resp['data']['result']['gt']
        challenge = login_resp['data']['result']['challenge']
        key = login_resp['data']['result']['key']
        print('gt:', gt)
        print('challenge:', challenge)
        print('请前往以下链接进行人机验证：')
        print('https://kuresaru.github.io/geetest-validator/')
        print('请输入validate和seccode，中间用空格隔开：')
        input_line = stdin.readline()
        input_arr = input_line.split(' ', 2)
        validate = input_arr[0]
        seccode = input_arr[1]
        resp = requests.get('https://passport.bilibili.com/login?act=getkey')
        if resp.status_code != 200:
            logger.error('登录bilibili失败, status code: %d', resp.status_code)
            return
        get_key_resp = json.loads(resp.content.decode('utf-8'))
        user_name = config.bilibili['username']
        pwd = config.bilibili['password']
        encrypt_pwd = encrypt(get_key_resp['key'].encode('utf-8'), (get_key_resp['hash'] + pwd).encode('utf-8'))
        post_format = 'captchaType=6&username={0}&password={1}&keep=true&key={2}&challenge={3}&validate={4}&seccode={5}'
        post_msg = post_format.format(user_name, encrypt_pwd, key, challenge, validate, seccode)
        resp = requests.request(method='POST', headers={'content_type': 'application/x-www-form-urlencoded'},
                                url='https://passport.bilibili.com/web/login/v2', data=post_msg)
        if resp.status_code != 200:
            logger.error('登录bilibili失败, status code: %d', resp.status_code)
        login_success_resp = json.loads(resp.content.decode('utf-8'))
        if login_success_resp['code'] != 0:
            if login_success_resp['code'] != 2100:
                logger.error('登录bilibili失败，错误码：%d', login_success_resp['code'])
            else:
                logger.error('登录bilibili失败，错误码：%d, 错误信息：%s', login_success_resp['code'], resp.content.decode('utf-8'))
            return
        logger.info('登录bilibili成功')
        self.cookies = requests.utils.dict_from_cookiejar(resp.cookies)

    def get_live_status(self) -> str:
        resp = requests.request(method='GET',
                                url='https://api.live.bilibili.com/room/v1/Room/getRoomInfoOld?mid=611240532',
                                cookies=self.cookies,
                                headers={'content_type': 'application/x-www-form-urlencoded'})
        if resp.status_code != 200:
            logger.error("请求直播间信息失败，错误码：%s", resp.status_code)
            return ''
        live_status_resp = json.loads(resp.content.decode('utf-8'))
        if live_status_resp['code'] != 0:
            logger.error('请求直播间状态失败，错误码：%d，错误信息：%s，', live_status_resp['code'], live_status_resp['message'])
            return ''
        if live_status_resp['data']['liveStatus'] == 0:
            return '直播间状态：未开播'
        else:
            return '直播间状态：开播\n直播标题：{0}\n人气：{1}\n直播间地址：{2}'.format(live_status_resp['data']['title'],
                                                                  live_status_resp['data']['online'], get_live_url())

    # def start_live(self) -> str:
    #     bili_jct = self.cookies.get('bili_jct')
    #     if bili_jct is None:
    #         return 'B站登录过期'
    #     rid = config.bilibili['room_id']
    #     area = config.bilibili['area_v2']
    #     post_msg = 'room_id={0}&platform=pc&area_v2={1}&csrf_token={2}&csrf={3}'.format(rid, area, bili_jct, bili_jct)
    #     resp = requests.request(method='POST', url='https://api.live.bilibili.com/room/v1/Room/startLive',
    #                             cookies=self.cookies, data=post_msg,
    #                             headers={'content_type': 'application/x-www-form-urlencoded'})
    #     if resp.status_code != 200:
    #         logger.error('开启直播间失败，错误码：%d', resp.status_code)
    #         return ''

