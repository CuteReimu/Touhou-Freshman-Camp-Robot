import os
from pathlib import Path

import chat_pipeline
import config
import myqq


class UpdatePipeline(chat_pipeline.IChatPipeline):
    def __init__(self):
        self.__update_content = ''
        self.__already_group_ids = set()

    def on_init(self):
        p = Path('../update.txt')
        if p.exists():
            self.__update_content = p.read_text('utf-8').strip()
            p.rename('../update.txt.bak')

    def execute(self, qq_group_number: str, qq: str, msg: str) -> str:
        if len(self.__update_content) > 0 and qq_group_number in config.qq['available_qq_group']:
            if qq_group_number not in self.__already_group_ids:
                self.__already_group_ids.add(qq_group_number)
                myqq.send_group_message(qq_group_number, self.__update_content)
        return msg
