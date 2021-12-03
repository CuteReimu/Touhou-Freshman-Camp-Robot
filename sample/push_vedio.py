from schedule import schedule
from bilibili import bili
import config
import os
import chat_pipeline_manager

__delay = 600

def __get_new_vedio():
    vedio_list = bili.get_user_vedio(config.bilibili['mid'])
    new_vedio_list = []
    if os.path.exists('../lastestVedio.txt'):
        with open('../lastestVedio.txt', 'w+') as f:
            lastestId = f.read()
            if(lastestId != ''):
                i = 0
                while(vedio_list[i].bvid != lastestId):
                    new_vedio_list.append(vedio_list[i])
                    i += 1
            f.write(vedio_list[0].bvid)
    return new_vedio_list


def init():
    schedule.add(__delay, __get_new_vedio)
    pass
