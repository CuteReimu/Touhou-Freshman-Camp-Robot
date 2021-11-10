import os

import message
import message_admin
import myqq
from logger import logger

whitelist_cache: set[str] = set()


def on_init():
    if os.path.exists('../whitelist.txt'):
        with open('../whitelist.txt', 'r') as f:
            line = f.readline()
            while line:
                line = line.strip()
                if line != '':
                    whitelist_cache.add(line)
                line = f.readline()


def update_whitelist_file():
    is_first = True
    try:
        with open('../whitelist.txt', 'w') as f:
            for key in whitelist_cache:
                if is_first:
                    f.write(key)
                    is_first = False
                else:
                    f.write('\n' + key)
    except IOError:
        logger.error('update whitelist file failed')


class DelWhitelist(message.IMessageDispatcher):
    def __init__(self):
        super().__init__('删除白名单', '删除白名单 对方QQ号')

    def check_auth(self, qq: str) -> bool:
        return qq in message_admin.admin_cache

    def execute(self, qq_group_number: str, qq: str, *args: str) -> None:
        if len(args) != 1:
            return
        target = args[0]
        if target not in whitelist_cache:
            myqq.send_group_message(qq_group_number, target + '并不是白名单')
            return
        whitelist_cache.remove(target)
        update_whitelist_file()
        myqq.send_group_message(qq_group_number, '已删除白名单：' + target)


class AddWhitelist(message.IMessageDispatcher):
    def __init__(self):
        super().__init__('增加白名单', '增加白名单 对方QQ号')

    def check_auth(self, qq: str) -> bool:
        return qq in message_admin.admin_cache

    def execute(self, qq_group_number: str, qq: str, *args: str) -> None:
        if len(args) != 1:
            return
        target = args[0]
        if target in whitelist_cache:
            myqq.send_group_message(qq_group_number, target + '已经是白名单了')
            return
        whitelist_cache.add(target)
        update_whitelist_file()
        myqq.send_group_message(qq_group_number, '已增加白名单：' + target)


class GetWhitelist(message.IMessageDispatcher):
    def __init__(self):
        super().__init__('列出所有白名单', '列出所有白名单')

    def check_auth(self, qq: str) -> bool:
        return qq in message_admin.admin_cache

    def execute(self, qq_group_number: str, qq: str, *args: str) -> None:
        if len(args) != 0:
            return
        msg = "白名单列表："
        for whitelist in whitelist_cache:
            msg += '\n' + whitelist
        myqq.send_group_message(qq_group_number, msg)


class CheckWhitelist(message.IMessageDispatcher):
    def __init__(self):
        super().__init__('查看白名单', '查看白名单 对方QQ号')

    def check_auth(self, qq: str) -> bool:
        return qq in message_admin.admin_cache

    def execute(self, qq_group_number: str, qq: str, *args: str) -> None:
        if len(args) != 1:
            return
        if args[0] in whitelist_cache:
            myqq.send_group_message(qq_group_number, args[0] + '是白名单')
        else:
            myqq.send_group_message(qq_group_number, args[0] + '不是白名单')
