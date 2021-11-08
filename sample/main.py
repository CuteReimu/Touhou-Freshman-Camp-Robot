import logging
import config

import myqq


if __name__ == '__main__':
    logging.basicConfig(filename=config.logging_config['log_file'], level=config.logging_config['level'])
    myqq.start_listen()
