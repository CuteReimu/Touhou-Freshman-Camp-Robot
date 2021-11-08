import logging

myqq = {
    'token': 'qsfsqwdqwe1431c443c',
    'api_url': 'http://localhost:10100/MyQQHTTPAPI',
    'callback_ip': '127.0.0.1',
    'callback_port': 10111
}

bilibili = {
    'username': '13888888888',  # 用户名
    'password': '12345678',  # 密码
    'mid': '12345678',  # B站ID
    'room_id': '12345678',  # B站直播间房间号
    'area_v2': '236'  # 直播分区，236-主机游戏
}

qq = {
    'robot_self_qq': '12345678',  # 机器人自己的QQ号
    'super_admin_qq': '12345678',  # 超管的QQ号
    'available_qq_group': ['12345678', '23456789']  # 接收消息的QQ群
}

logging_config = {
    'log_path': '../logs',
    'console_level': logging.DEBUG,
    'console_file_level': logging.INFO,
    'error_file_level': logging.WARN
}
