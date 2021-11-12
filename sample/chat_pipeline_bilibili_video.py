import re

import chat_pipeline
import mirai_bot
from bilibili import bili
from mirai_bot_chain import plain, image


class BilibiliVideoPipeline(chat_pipeline.IChatPipeline):
    def on_init(self):
        pass

    def execute(self, qq_group_number: int, qq: int, msg_chain: list) -> str:
        if len(msg_chain) == 2 and msg_chain[1]['type'] == 'Plain':
            msg = msg_chain[1]['text']
            match_obj = re.match(r'^(?:https?://www\.bilibili\.com/video/)?av(\d{8})$', msg, re.I)
            resp = None
            if match_obj:
                resp = bili.get_video_info(aid=int(match_obj.group(1)))
            else:
                match_obj = re.match(r'^(?:https?://www\.bilibili\.com/video/)?bv([0-9A-Za-z]{10})$', msg, re.I)
                if match_obj:
                    resp = bili.get_video_info(bid=match_obj.group(1))
            if resp is not None:
                url = 'https://www.bilibili.com/video/' + resp['bvid']
                up = resp['owner']['name']
                ret = '{0}\n{1}\nUP主：{2}\n视频简介：{3}'.format(resp['title'], url, up, resp['desc'])
                mirai_bot.send_group_message(qq_group_number, [image(image_id='', url=resp['pic']), plain(ret)])
            return msg
