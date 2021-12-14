import chat_pipeline_manager
import os
from schedule import schedule
from bilibili import bili
import config

class newVedioPusher():
    def __init__(self, mid, delay: int = 600):
        self.__mid = mid
        self.__delay = delay

    def __get_new_vedio(self):
        vedio_list = bili.get_user_vedio(self.__mid)
        new_vedio_list = []
        if os.path.exists('../latestVedio.txt'):
            with open('../latestVedio.txt', 'r') as f:
                lastestId = f.read()
                if(lastestId != ''):
                    i = 0
                    while(vedio_list[i]['bvid'] != lastestId):
                        new_vedio_list.append(vedio_list[i]['bvid'])
                        i += 1
                f.close()
        with open('../latestVedio.txt', 'w') as f:
            f.write(vedio_list[0]['bvid'])
            f.close()
        return new_vedio_list

    def __push_new_vedio(self):
        new_vedio_list = self.__get_new_vedio()
        print(new_vedio_list)
        if (len(new_vedio_list) != 0):
            for i in new_vedio_list:
                for j in config.qq['available_qq_group']:
                    print(i,j)
                    chat_pipeline_manager.deal_with_msg(j, '', i)
    
    def start(self):
        schedule.add(self.__delay, self.__push_new_vedio)

videoPusher = newVedioPusher(config.bilibili['mid'])