import re

import chat_pipeline
import myqq
from bilibili import bili


class BilibiliVideoPipeline(chat_pipeline.IChatPipeline):
    def on_init(self):
        pass

    def execute(self, qq_group_number: str, qq: str, msg: str) -> str:
        match_obj = re.search(r'(?:https?://www\.bilibili\.com/video/|\A)av(\d+)', msg, re.I)
        resp = None
        if match_obj:
            resp = bili.get_video_info(aid=int(match_obj.group(1)))
        else:
            match_obj = re.search(r'(?:https?://(?:www\.bilibili\.com/video|b23\.tv)/)?bv([0-9A-Za-z]{10})', msg, re.I)
            if match_obj:
                resp = bili.get_video_info(bid=match_obj.group(1))
            else:
                match_obj = re.search(r'https?://b23\.tv/[0-9A-Za-z]{7}', msg, re.I)
                if match_obj:
                    bili.get_video_info(qq_group_number=qq_group_number, qq=qq, short_url=match_obj.group(0))
        if resp is not None:
            pic_url = '[pic=%s]' % resp['pic']
            url = 'https://www.bilibili.com/video/' + resp['bvid']
            up = resp['owner']['name']
            ret = '{0}\n{1}\n{2}\nUP主：{3}\n视频简介：{4}'.format(pic_url, resp['title'], url, up, resp['desc'])
            myqq.send_group_message(qq_group_number, ret)
        return msg
