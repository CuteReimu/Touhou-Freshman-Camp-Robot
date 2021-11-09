import logging
import os
from logging import handlers

import config

__l = logging.getLogger('robot')


def debug(msg, *args, **kwargs):
    __l.debug(msg, *args, **kwargs)


def info(msg, *args, **kwargs):
    __l.info(msg, *args, **kwargs)


def warning(msg, *args, **kwargs):
    __l.warning(msg, *args, **kwargs)


def error(msg, *args, **kwargs):
    __l.error(msg, *args, **kwargs)


def critical(msg, *args, **kwargs):
    __l.critical(msg, *args, **kwargs)


def init():
    log_format = logging.Formatter('[%(levelname)s] %(asctime)s [%(filename)s:%(lineno)d]: %(message)s')
    log_path = config.logging_config['log_path']
    if not os.path.exists(log_path):
        os.mkdir(log_path)
    # console.log
    fhc_file = os.path.join(log_path, 'console.log')
    fhc = handlers.TimedRotatingFileHandler(filename=fhc_file, when='d', backupCount=7, encoding='utf-8')
    fhc.setLevel(config.logging_config['console_file_level'])
    fhc.setFormatter(log_format)
    __l.addHandler(fhc)
    # error.log
    fhe_file = os.path.join(log_path, 'error.log')
    fhe = handlers.TimedRotatingFileHandler(filename=fhe_file, when='d', backupCount=7, encoding='utf-8')
    fhe.setLevel(config.logging_config['error_file_level'])
    fhe.setFormatter(log_format)
    __l.addHandler(fhe)
    # 控制台输出
    ch = logging.StreamHandler()
    ch.setLevel(config.logging_config['console_level'])
    ch.setFormatter(log_format)
    __l.addHandler(ch)
    __l.setLevel(logging.DEBUG)
    info("logger start")
