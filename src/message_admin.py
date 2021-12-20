import os

import config
import message
import mirai_bot
from logger import logger
from mirai_bot_chain import plain

admin_cache: set[int] = set()


def on_init():
    if os.path.exists('../admin.txt'):
        with open('../admin.txt', 'r') as f:
            line = f.readline()
            while line:
                line = line.strip()
                if line != '':
                    admin_cache.add(int(line))
                line = f.readline()
    admin_cache.add(config.qq['super_admin_qq'])


def update_admin_file():
    is_first = True
    try:
        with open('../admin.txt', 'w') as f:
            for key in admin_cache:
                if is_first:
                    f.write(str(key))
                    is_first = False
                else:
                    f.write('\n' + str(key))
    except IOError:
        logger.error('update admin file failed')


class DelAdmin(message.IMessageDispatcher):
    def __init__(self):
        super().__init__('删除管理员', '删除管理员 对方QQ号')

    def check_auth(self, qq: int) -> bool:
        return qq == config.qq['super_admin_qq']

    def execute(self, qq_group_number: int, qq: int, *args: str) -> None:
        if len(args) != 1:
            return
        target = int(args[0])
        if target == config.qq['super_admin_qq']:
            mirai_bot.send_group_message(qq_group_number, [plain('你不能删除自己')])
            return
        if target not in admin_cache:
            mirai_bot.send_group_message(qq_group_number, [plain(args[0] + '并不是管理员')])
            return
        admin_cache.remove(int(target))
        update_admin_file()
        mirai_bot.send_group_message(qq_group_number, [plain('已删除管理员：' + args[0])])


class AddAdmin(message.IMessageDispatcher):
    def __init__(self):
        super().__init__('增加管理员', '增加管理员 对方QQ号')

    def check_auth(self, qq: int) -> bool:
        return qq == config.qq['super_admin_qq']

    def execute(self, qq_group_number: int, qq: int, *args: str) -> None:
        if len(args) != 1:
            return
        target = int(args[0])
        if target in admin_cache:
            mirai_bot.send_group_message(qq_group_number, [plain(args[0] + '已经是管理员了')])
            return
        admin_cache.add(int(target))
        update_admin_file()
        mirai_bot.send_group_message(qq_group_number, [plain('已增加管理员：' + args[0])])


class GetAdmin(message.IMessageDispatcher):
    def __init__(self):
        super().__init__('查看管理员', '查看管理员')

    def check_auth(self, qq: int) -> bool:
        return True

    def execute(self, qq_group_number: int, qq: int, *args: str) -> None:
        if len(args) != 0:
            return
        msg = "管理员列表："
        for admin in admin_cache:
            msg += '\n' + str(admin)
        mirai_bot.send_group_message(qq_group_number, [plain(msg)])
