import logger
import myqq
from bilibili import bili

if __name__ == '__main__':
    logger.init()
    bili.login()
    myqq.start_listen()
