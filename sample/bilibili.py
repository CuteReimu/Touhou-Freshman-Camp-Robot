import base64
import json
from sys import stdin

import requests
import requests.utils
import rsa

import config
import myqq
from logger import logger


def encrypt(public_key: bytes, data: bytes) -> bytes:
    pub_key = rsa.PublicKey.load_pkcs1_openssl_pem(public_key)
    return base64.urlsafe_b64encode(rsa.encrypt(data, pub_key))


def get_live_url() -> str:
    return 'https://live.bilibili.com/' + config.bilibili['room_id']


class Bilibili:
    def __init__(self):
        try:
            with open('../cookies.txt', 'r') as f:
                self.cookies = json.loads(f.read())
        except IOError:
            self.cookies = {}

    def login(self) -> None:
        if len(self.cookies) != 0:
            return
        resp = requests.get(
            'https://passport.bilibili.com/web/captcha/combine?plat=6')
        if resp.status_code != 200:
            logger.error('login failed, status code: %d', resp.status_code)
            raise RuntimeError
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
        print('验证后请输入validate：')
        validate = stdin.readline().strip()
        seccode = validate
        resp = requests.get('https://passport.bilibili.com/login?act=getkey')
        if resp.status_code != 200:
            logger.error('登录bilibili失败, status code: %d', resp.status_code)
            raise RuntimeError
        get_key_resp = json.loads(resp.content.decode('utf-8'))
        user_name = config.bilibili['username']
        pwd = config.bilibili['password']
        encrypt_pwd = encrypt(get_key_resp['key'].encode(
            'utf-8'), (get_key_resp['hash'] + pwd).encode('utf-8'))
        post_format = 'captchaType=6&username={0}&password={1}&keep=true&key={2}&challenge={3}&validate={4}&seccode={5}'
        post_msg = post_format.format(user_name, encrypt_pwd.decode(
            'utf-8'), key, challenge, validate, seccode)
        resp = requests.request(method='POST', headers={'Content-Type': 'application/x-www-form-urlencoded'},
                                url='https://passport.bilibili.com/web/login/v2', data=post_msg)
        if resp.status_code != 200:
            logger.error('登录bilibili失败, status code: %d', resp.status_code)
        login_success_resp = json.loads(resp.content.decode('utf-8'))
        if login_success_resp['code'] != 0:
            logger.error('登录bilibili失败，错误码：%d, 错误信息：%s',
                         login_success_resp['code'], login_success_resp['message'])
            raise RuntimeError
        logger.info('登录bilibili成功')
        self.cookies = requests.utils.dict_from_cookiejar(resp.cookies)
        logger.debug('设置cookie成功：{0}'.format(self.cookies))
        try:
            with open('../cookies.txt', 'w') as f:
                f.write(json.dumps(self.cookies))
        except IOError:
            logger.error('update cookies file failed')

    def get_live_status(self, qq_group_num: str) -> None:
        rid = config.bilibili['room_id']
        resp = requests.request(method='GET',
                                url='https://api.live.bilibili.com/room/v1/Room/get_info?id={0}'.format(
                                    rid),
                                cookies=self.cookies,
                                headers={'Content-Type': 'application/x-www-form-urlencoded'})
        if resp.status_code != 200:
            logger.error("请求直播间信息失败，错误码：%s，返回内容：%s",
                         resp.status_code, resp.content.decode('utf-8'))
            return
        live_status_resp = json.loads(resp.content.decode('utf-8'))
        if live_status_resp['code'] != 0:
            logger.error('请求直播间状态失败，错误码：%d，错误信息：%s，',
                         live_status_resp['code'], live_status_resp['message'])
            return
        if live_status_resp['data']['live_status'] == 0:
            myqq.send_group_message(qq_group_num, '直播间状态：未开播')
        else:
            msg = '直播间状态：开播\n直播标题：{0}\n人气：{1}\n直播间地址：{2}'.format(live_status_resp['data']['title'],
                                                                 live_status_resp['data']['online'], get_live_url())
            myqq.send_group_message(qq_group_num, msg)

    def start_live(self, qq_group_num: str, qq: str) -> None:
        bili_jct = self.cookies.get('bili_jct')
        if bili_jct is None:
            myqq.send_group_message(qq_group_num, 'B站登录过期')
            return
        rid = config.bilibili['room_id']
        area = config.bilibili['area_v2']
        post_msg = 'room_id={0}&platform=pc&area_v2={1}&csrf_token={2}&csrf={3}'.format(
            rid, area, bili_jct, bili_jct)
        resp = requests.request(method='POST', url='https://api.live.bilibili.com/room/v1/Room/startLive',
                                cookies=self.cookies, data=post_msg,
                                headers={'Content-Type': 'application/x-www-form-urlencoded'})
        if resp.status_code != 200:
            logger.error('开启直播间失败，错误码：%d', resp.status_code)
            return
        start_live_resp = json.loads(resp.content.decode('utf-8'))
        if start_live_resp['code'] != 0:
            logger.error('开启直播间失败，错误码：%d，错误信息1：%s，错误信息2：%s', start_live_resp['code'], start_live_resp['message'],
                         start_live_resp['msg'])
            return
        if start_live_resp['data']['change'] == 0:
            myqq.send_group_message(
                qq_group_num, '直播间本来就是开启的，推流码已私聊\n直播间地址：{0}\n快来围观吧！'.format(get_live_url()))
        else:
            msg = '直播间已开启，推流码已私聊，别忘了修改直播间标题哦！\n直播间地址：{0}\n快来围观吧！'.format(
                get_live_url())
            myqq.send_group_message(qq_group_num, msg)
        rtmp_addr = start_live_resp['data']['rtmp']['addr']
        rtmp_code = start_live_resp['data']['rtmp']['code']
        myqq.send_private_message(
            qq_group_num, qq, 'RTMP推流地址：{0}\n秘钥：{1}'.format(rtmp_addr, rtmp_code))

    def stop_live(self, qq_group_num: str) -> None:
        bili_jct = self.cookies.get('bili_jct')
        if bili_jct is None:
            return myqq.send_group_message(qq_group_num, 'B站登录过期')
        rid = config.bilibili['room_id']
        post_msg = 'room_id={0}&csrf={1}'.format(rid, bili_jct)
        resp = requests.request(method='POST', url='https://api.live.bilibili.com/room/v1/Room/stopLive',
                                cookies=self.cookies, data=post_msg,
                                headers={'Content-Type': 'application/x-www-form-urlencoded'})
        if resp.status_code != 200:
            logger.error('关闭直播间失败，错误码：%d', resp.status_code)
            return
        stop_live_resp = json.loads(resp.content.decode('utf-8'))
        if stop_live_resp['code'] != 0:
            logger.error('关闭直播间失败，错误码：%d，错误信息1：%s，错误信息2：%s', stop_live_resp['code'], stop_live_resp['message'],
                         stop_live_resp['msg'])
            return
        if stop_live_resp['data']['change'] == 0:
            myqq.send_group_message(qq_group_num, '直播间本来就是关闭的')
        else:
            myqq.send_group_message(qq_group_num, '直播间已关闭')

    def change_live_title(self, qq_group_num: str, title: str) -> None:
        bili_jct = self.cookies.get('bili_jct')
        if bili_jct is None:
            return myqq.send_group_message(qq_group_num, 'B站登录过期')
        rid = config.bilibili['room_id']
        post_msg = 'room_id={0}&title={1}&csrf={2}'.format(
            rid, title, bili_jct).encode('utf-8')
        resp = requests.request(method='POST', url='https://api.live.bilibili.com/room/v1/Room/update',
                                cookies=self.cookies, data=post_msg,
                                headers={'Content-Type': 'application/x-www-form-urlencoded'})
        if resp.status_code != 200:
            logger.error('修改直播间标题失败，错误码：%d', resp.status_code)
            return
        change_live_title_resp = json.loads(resp.content.decode('utf-8'))
        if change_live_title_resp['code'] != 0:
            logger.error('修改直播间标题失败，错误码：%d，错误信息1：%s，错误信息2：%s', change_live_title_resp['code'],
                         change_live_title_resp['message'],
                         change_live_title_resp['msg'])
            myqq.send_group_message(qq_group_num, '修改直播间标题失败，请联系管理员')
        else:
            myqq.send_group_message(qq_group_num, '直播间标题已修改为：' + title)

    def get_video_info(self, aid: int = 0, bid: str = None):
        if aid != 0:
            url = 'https://api.bilibili.com/x/web-interface/view?aid={0}'.format(
                aid)
        elif bid is not None and bid != '':
            url = 'https://api.bilibili.com/x/web-interface/view?bvid=' + bid
        else:
            logger.error('aid和bvid至少要填一项')
            return None
        resp = requests.request(method='GET', url=url, cookies=self.cookies)
        if resp.status_code != 200:
            logger.info('获取视频详细信息失败，错误码：%d', resp.status_code)
            return None
        video_info = json.loads(resp.content.decode('utf-8'))
        if video_info['code'] != 0:
            logger.info('获取视频详细信息失败，错误码：%d，错误信息1：%s',
                        video_info['code'], video_info['message'])
            return None
        else:
            return video_info['data']

    def get_user_vedio(self, mid:int, pn:int, ps:int, order:str, tid:int, keyword:str):
        if mid is None and mid != 0:
            logger.error('必须填写mid')
            return None
        if pn is None:
            pn = 1
        if ps is None:
            ps = 10
        res = requests.request(
            method='GET',
            url="http://api.bilibili.com/x/space/arc/search",
            params={'mid': mid, 'order': order, 'tid': tid,
                    'keyword': keyword, 'pn': pn, 'ps': ps},
            cookies=self.cookies,
            headers={'Content-Type': 'data/json'}
        )
        if res.status_code != 200:
            logger.info('获取用户视频列表失败，错误码：%d', res.status_code)
            return None
        user_vedio = json.loads(res.content.decode('utf-8'))
        if user_vedio['code'] == 0:
            return user_vedio['data']['list']['vlist']
        else:
            logger.info('获取用户视频列表失败，错误码：%d，错误信息1：%s',
                        user_vedio['code'], user_vedio['message'])
            return None


bili = Bilibili()
