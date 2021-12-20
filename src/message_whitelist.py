import os

import message
import message_admin
import mirai_bot
from logger import logger
from mirai_bot_chain import plain

whitelist_cache: set[int] = set()


def on_init():
    if os.path.exists('../whitelist.txt'):
        with open('../whitelist.txt', 'r') as f:
            line = f.readline()
            while line:
                line = line.strip()
                if line != '':
                    whitelist_cache.add(int(line))
                line = f.readline()


def update_whitelist_file():
    is_first = True
    try:
        with open('../whitelist.txt', 'w') as f:
            for key in whitelist_cache:
                if is_first:
                    f.write(str(key))
                    is_first = False
                else:
                    f.write('\n' + str(key))
    except IOError:
        logger.error('update whitelist file failed')


class DelWhitelist(message.IMessageDispatcher):
    def __init__(self):
        super().__init__('删除白名单', '删除白名单 对方QQ号')

    def check_auth(self, qq: int) -> bool:
        return qq in message_admin.admin_cache

    def execute(self, qq_group_number: int, qq: int, *args: str) -> None:
        if len(args) != 1:
            mirai_bot.send_group_message(qq_group_number, [plain('指令格式如下：\n删除白名单 对方QQ号')])
            return
        target = int(args[0])
        if target not in whitelist_cache:
            mirai_bot.send_group_message(qq_group_number, [plain(args[0] + '并不是白名单')])
            return
        whitelist_cache.remove(target)
        update_whitelist_file()
        mirai_bot.send_group_message(qq_group_number, [plain('已删除白名单：' + args[0])])


class AddWhitelist(message.IMessageDispatcher):
    def __init__(self):
        super().__init__('增加白名单', '增加白名单 对方QQ号')

    def check_auth(self, qq: int) -> bool:
        return qq in message_admin.admin_cache

    def execute(self, qq_group_number: int, qq: int, *args: str) -> None:
        if len(args) != 1:
            mirai_bot.send_group_message(qq_group_number, [plain('指令格式如下：\n增加白名单 对方QQ号')])
            return
        target = int(args[0])
        if target in whitelist_cache:
            mirai_bot.send_group_message(qq_group_number, [plain(args[0] + '已经是白名单了')])
            return
        whitelist_cache.add(target)
        update_whitelist_file()
        mirai_bot.send_group_message(qq_group_number, [plain('已增加白名单：' + args[0])])


class GetWhitelist(message.IMessageDispatcher):
    def __init__(self):
        super().__init__('列出所有白名单', '列出所有白名单')

    def check_auth(self, qq: int) -> bool:
        return qq in message_admin.admin_cache

    def execute(self, qq_group_number: int, qq: int, *args: str) -> None:
        if len(args) != 0:
            return
        msg = "白名单列表："
        for whitelist in whitelist_cache:
            msg += '\n' + str(whitelist)
        mirai_bot.send_group_message(qq_group_number, [plain(msg)])


class CheckWhitelist(message.IMessageDispatcher):
    def __init__(self):
        super().__init__('查看白名单', '查看白名单 对方QQ号')

    def check_auth(self, qq: int) -> bool:
        return True

    def execute(self, qq_group_number: int, qq: int, *args: str) -> None:
        if len(args) != 1:
            mirai_bot.send_group_message(qq_group_number, [plain('指令格式如下：\n查看白名单 对方QQ号')])
            return
        if int(args[0]) in whitelist_cache:
            mirai_bot.send_group_message(qq_group_number, [plain(args[0] + '是白名单')])
        else:
            mirai_bot.send_group_message(qq_group_number, [plain(args[0] + '不是白名单')])
