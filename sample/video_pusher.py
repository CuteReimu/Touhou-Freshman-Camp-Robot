import chat_pipeline_manager
import os
from schedule import schedule
from bilibili import bili
import config

class newvideoPusher():
    def __init__(self, mid, delay: int = 600):
        self.__mid = mid
        self.__delay = delay

    def __get_new_video(self):
        video_list = bili.get_user_video(self.__mid)
        new_video_list = []
        if os.path.exists('../latestvideo.txt'):
            with open('../latestvideo.txt', 'r') as f:
                lastestId = f.read()
                if(lastestId != ''):
                    i = 0
                    while(video_list[i]['bvid'] != lastestId):
                        new_video_list.append(video_list[i]['bvid'])
                        i += 1
                f.close()
        with open('../latestvideo.txt', 'w') as f:
            f.write(video_list[0]['bvid'])
            f.close()
        return new_video_list

    def __push_new_video(self):
        new_video_list = self.__get_new_video()
        print(new_video_list)
        if (len(new_video_list) != 0):
            for i in new_video_list:
                for j in config.qq['available_qq_group']:
                    print(i,j)
                    chat_pipeline_manager.deal_with_msg(j, '', i)
    
    def start(self):
        schedule.add(self.__delay, self.__push_new_video)

videoPusher = newvideoPusher(config.bilibili['mid'])