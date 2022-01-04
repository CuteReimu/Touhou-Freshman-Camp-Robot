import datetime
import json
import time

import requests
from requests.adapters import HTTPAdapter

import message
import myqq
from logger import logging


class Event:
    def __init__(self, d: dict):
        self.start = d.get('startStr', '')
        self.types = d.get('type', [])
        self.desc = d.get('desc', '')

    def __lt__(self, other) -> bool:
        return self.start < other.start

    def __str__(self) -> str:
        return self.start + ('【%s】' % self.types[0] if self.types else ' ') + self.desc


class GetEvents(message.IMessageDispatcher):
    def __init__(self):
        self.__today = int(time.mktime(datetime.date.today().timetuple()))
        self.__delta = 7 * 24 * 3600
        self.__last_fetch_time: float = 0
        self.__cache_str = ''
        self.__last_request_time_dict = {}
        self.__last_request_time: float = 0

    @property
    def name(self) -> str:
        return '查新闻'

    @property
    def tips(self) -> str:
        return '查新闻' if self.__check_cd(time.time()) else ''

    def check_auth(self, qq: str) -> bool:
        return True

    def __check_cd(self, now: float, qq_group_number='') -> bool:
        if not qq_group_number:
            return now - self.__last_request_time >= 300
        if qq_group_number in self.__last_request_time_dict:
            return now - self.__last_request_time_dict[qq_group_number] >= 300
        return True

    def execute(self, qq_group_number: str, qq: str, *args: str) -> None:
        now = time.time()
        if not self.__check_cd(now, qq_group_number):
            myqq.send_group_message(qq_group_number, '这个功能每5分钟才能使用一次')
            return
        msg = self.__get_events(now)
        if msg:
            self.__last_request_time = now
            self.__last_request_time_dict[qq_group_number] = now
            myqq.send_group_message(qq_group_number, msg)

    def __get_events(self, now: float) -> str:
        if now - self.__last_fetch_time < 6 * 3600:
            return self.__cache_str
        start = time.strftime('%Y-%m-%d', time.localtime(now - self.__delta))
        end = time.strftime('%Y-%m-%d', time.localtime(now + self.__delta))
        try:
            with requests.Session() as req:
                req.mount('http://', HTTPAdapter(max_retries=3))
                req.mount('https://', HTTPAdapter(max_retries=3))
                resp = req.get(url='https://calendar.thwiki.cc/events/?start=%s&end=%s' % (start, end), timeout=20)
                data = json.loads(resp.text)
                ret_arr = []
                for d in data['results']:
                    ret_arr.append(Event(d))
                ret_arr.sort()
                self.__cache_str = '\n'.join([str(ret) for ret in ret_arr])
        except requests.exceptions.RequestException as e:
            logging.error('failed to access thwiki: %r' % e)
        except json.decoder.JSONDecodeError as e:
            logging.error('failed to decode json: %r' % e)
        except (TypeError, KeyError) as e:
            logging.error('there seems to be something wrong with thwiki events data: %r' % e)
        return self.__cache_str
