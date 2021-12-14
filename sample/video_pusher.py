import chat_pipeline_manager
import os
from schedule import schedule
from bilibili import bili
import config

class NewVideoPusher():
    def __init__(self, mid):
        self.__mid = int(mid)
        if os.path.exists('../latestvideo.txt'):
            with open('../latestvideo.txt', 'r') as f:
                self.__lastestId = f.readline()
        else:
            self.__lastestId = ''

    def __get_new_video(self):
        video_list = bili.get_user_video(self.__mid)
        new_video_list = []
        if self.__lastestId != '':
            i = 0
            while video_list[i]['bvid'] != self.__lastestId:
                new_video_list.append(video_list[i]['bvid'])
                i += 1
        if self.__lastestId != video_list[0]['bvid']:
            self.__lastestId = video_list[0]['bvid']
            with open('../latestvideo.txt', 'w') as f:
                f.write(video_list[0]['bvid'])
        return new_video_list

    def __push_new_video(self):
        new_video_list = self.__get_new_video()
        if len(new_video_list) != 0:
            for i in new_video_list:
                for j in config.schedule['qq_group']:
                    chat_pipeline_manager.deal_with_msg(j, '', i)
    
    def start(self):
        schedule.add(config.schedule['video_push_delay'], self.__push_new_video)

videoPusher = NewVideoPusher(config.bilibili['mid'])