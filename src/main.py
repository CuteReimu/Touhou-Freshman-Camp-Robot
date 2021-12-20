import logger
import mirai_bot
from bilibili import bili

if __name__ == '__main__':
    logger.init()
    bili.login()
    # mirai_bot.start_listen()
    mirai_bot.start_listen()
