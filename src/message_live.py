import message
import message_admin
import message_whitelist
import myqq
from bilibili import bili

live_user = None


class GetLiveState(message.IMessageDispatcher):
    @property
    def name(self) -> str:
        return '直播状态'

    @property
    def tips(self) -> str:
        return '直播状态'

    def check_auth(self, qq: str) -> bool:
        return True

    def execute(self, qq_group_number: str, qq: str, *args: str) -> None:
        if len(args) != 0:
            return
        bili.get_live_status(qq_group_number)


class StartLive(message.IMessageDispatcher):
    @property
    def name(self) -> str:
        return '开始直播'

    @property
    def tips(self) -> str:
        return '开始直播'

    def check_auth(self, qq: str) -> bool:
        return qq in message_whitelist.whitelist_cache

    def execute(self, qq_group_number: str, qq: str, *args: str) -> None:
        if len(args) != 0:
            return
        if bili.start_live(qq_group_number, qq):
            global live_user
            live_user = qq


class StopLive(message.IMessageDispatcher):
    @property
    def name(self) -> str:
        return '关闭直播'

    @property
    def tips(self) -> str:
        return '关闭直播'

    def check_auth(self, qq: str) -> bool:
        return qq in message_whitelist.whitelist_cache

    def execute(self, qq_group_number: str, qq: str, *args: str) -> None:
        if len(args) != 0:
            return
        global live_user
        if live_user is not None and live_user != qq and qq not in message_admin.admin_cache:
            myqq.send_group_message('谢绝唐突关闭直播')
            return
        if bili.stop_live(qq_group_number):
            live_user = None


class ChangeLiveTitle(message.IMessageDispatcher):
    @property
    def name(self) -> str:
        return '修改直播标题'

    @property
    def tips(self) -> str:
        return '修改直播标题 新标题'

    def check_auth(self, qq: str) -> bool:
        return qq in message_whitelist.whitelist_cache

    def execute(self, qq_group_number: str, qq: str, *args: str) -> None:
        if len(args) < 1:
            myqq.send_group_message(qq_group_number, '指令格式如下：\n修改直播标题 新标题')
            return
        title = ' '.join(args)
        if len(title) > 20:
            return
        global live_user
        if live_user is not None and live_user != qq and qq not in message_admin.admin_cache:
            myqq.send_group_message('谢绝唐突修改直播标题')
            return
        bili.change_live_title(qq_group_number, title)
