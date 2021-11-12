import os
import time
from datetime import datetime, timedelta

from readerwriterlock import rwlock

import config
import message
import message_whitelist
import myqq
from logger import logger
from schedule import schedule

schedule_id = 0


class ScheduleData:
    def __init__(self, date_obj: datetime, tips: str, deltas: list[timedelta]):
        global schedule_id
        schedule_id += 1
        self.id = schedule_id
        self.date_obj = date_obj
        self.tips = tips
        self.deltas = deltas

    def __lt__(self, other):
        return self.date_obj < other.date_obj


schedule_cache: list[ScheduleData] = []
lock = rwlock.RWLockWrite()
time_format = '%Y/%m/%d|%H-%M-%S'


def update_schedule_file():
    is_first = True
    try:
        with open('../schedule.txt', 'w') as f:
            for data in schedule_cache:
                date_obj = data.date_obj
                if is_first:
                    f.write('{0} {1}'.format(date_obj.strftime(time_format), data.tips))
                    is_first = False
                else:
                    f.write('\n' + '{0} {1}'.format(date_obj.strftime(time_format), data.tips))
    except IOError:
        logger.error('update schedule file failed')


def __custom_sorted_fun(data1: tuple[datetime, str, list[timedelta]],
                        data2: tuple[datetime, str, list[timedelta]]) -> int:
    if data1[1] < data2[1]:
        return -1
    elif data1[1] > data2[1]:
        return 1
    return 0


__custom_sorted = __custom_sorted_fun


def __action():
    write_lock = lock.gen_wlock()
    write_lock.acquire()
    try:
        now = datetime.fromtimestamp(time.time())
        pop_id = []
        for data_id in range(len(schedule_cache)):
            data = schedule_cache[data_id]
            date_obj = data.date_obj
            if now >= date_obj:
                pop_id.append(data_id)
                continue
            msg = data.tips
            deltas = data.deltas
            pop_idx = []
            for delta_idx in range(len(deltas)):
                if now >= date_obj - deltas[delta_idx]:
                    pop_idx.append(delta_idx)
            if pop_idx:
                for qq_group_number in config.schedule['qq_group']:
                    myqq.send_group_message(qq_group_number, '温馨提醒：\n{0} 将于{1}开始'.format(msg, date_obj))
                pop_idx.reverse()
                for idx in pop_idx:
                    deltas.pop(idx)
        if pop_id:
            pop_id.reverse()
            for data_id in pop_id:
                schedule_cache.pop(data_id)
            update_schedule_file()
    except Exception as e:
        logger.error(str(e))
    finally:
        write_lock.release()
        schedule.add(60, __action)


def on_init():
    if os.path.exists('../schedule.txt'):
        with open('../schedule.txt', 'r') as f:
            delta = config.schedule['before']
            line = f.readline()
            while line:
                line = line.strip()
                if line != '':
                    arr = line.split(' ')
                    msg = arr[1]
                    for i in range(2, len(arr)):
                        msg += ' ' + arr[i]
                    date_obj = datetime.strptime(arr[0], time_format)
                    schedule_cache.append(ScheduleData(date_obj, arr[1], delta.copy()))
                line = f.readline()
            schedule_cache.sort()
    schedule.add(60, __action)
    schedule.run()


class AddSchedule(message.IMessageDispatcher):
    def __init__(self):
        super().__init__('增加预约', '增加预约 211225 190000 预约文字\n                 年月日 时分秒')

    def check_auth(self, qq: str) -> bool:
        return qq in message_whitelist.whitelist_cache

    def execute(self, qq_group_number: str, qq: str, *args: str) -> None:
        if len(args) < 3:
            myqq.send_group_message(qq_group_number, '指令格式如下：\n增加预约 211225 190000 预约文字\n                 年月日 时分秒')
            return
        try:
            date_obj = datetime.strptime(args[0] + args[1], '%y%m%d%H%M%S')
        except ValueError:
            myqq.send_group_message(qq_group_number, '日期或时间格式错误')
            return
        if len(args) > 12:
            return
        msg = ''
        for i in range(2, len(args)):
            if msg != '':
                msg += ' '
            msg += args[i]
        global __custom_sorted
        write_lock = lock.gen_wlock()
        write_lock.acquire()
        try:
            schedule_cache.append(ScheduleData(date_obj, msg, config.schedule['before'].copy()))
            schedule_cache.sort()
            update_schedule_file()
        finally:
            write_lock.release()
        myqq.send_group_message(qq_group_number, '增加预约成功')


class DelSchedule(message.IMessageDispatcher):
    def __init__(self):
        super().__init__('删除预约', '删除预约 序号（请先用“预约列表”查询序号）')

    def check_auth(self, qq: str) -> bool:
        return qq in message_whitelist.whitelist_cache

    def execute(self, qq_group_number: str, qq: str, *args: str) -> None:
        if len(args) != 1:
            myqq.send_group_message(qq_group_number, '指令格式如下：\n删除预约 序号')
            return
        try:
            del_idx = int(args[0])
        except ValueError:
            return
        succeed = False
        write_lock = lock.gen_wlock()
        write_lock.acquire()
        try:
            for idx in range(len(schedule_cache)):
                if schedule_cache[idx].id == del_idx:
                    schedule_cache.pop(idx)
                    update_schedule_file()
                    succeed = True
                    break
        finally:
            write_lock.release()
        if succeed:
            myqq.send_group_message(qq_group_number, '删除预约成功')
        else:
            myqq.send_group_message(qq_group_number, '找不到这条预约，请再次确认序号是否正确')


class ListAllSchedule(message.IMessageDispatcher):
    def __init__(self):
        super().__init__('预约列表', '预约列表 想要展示的行数（默认5行）')

    def check_auth(self, qq: str) -> bool:
        return True

    def execute(self, qq_group_number: str, qq: str, *args: str) -> None:
        if len(args) == 0:
            count = 5
        elif len(args) == 1:
            try:
                count = int(args[1])
            except ValueError:
                return
        else:
            myqq.send_group_message(qq_group_number, '指令格式如下：\n预约列表 想要展示的行数')
            return
        ret = ''
        i = 0
        read_lock = lock.gen_rlock()
        read_lock.acquire()
        try:
            for data in schedule_cache:
                if i >= count:
                    break
                if ret != '':
                    ret += '\n'
                ret += '{0}  {1}  {2}'.format(data.id, data.date_obj, data.tips)
                i += 1
        finally:
            read_lock.release()
        myqq.send_group_message(qq_group_number, ret)
