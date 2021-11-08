import logging
import config
import os
import myqq


def __start_logging():
    log_path = config.logging_config['log_path']
    if not os.path.exists(log_path):
        os.mkdir(log_path)
    fh = logging.FileHandler(os.path.join(log_path, 'console.log'), 'a', encoding='utf-8')
    fh.setLevel(logging.INFO)
    fh.setFormatter(logging.Formatter('[%(asctime)s] - %(filename)s] - %(levelname)s: %(message)s'))


if __name__ == '__main__':
    __start_logging()
    myqq.start_listen()
