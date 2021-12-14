import chat_pipeline
import config
import myqq
from datetime import datetime
from datetime import timedelta


class RepeaterInterruptionPipeline(chat_pipeline.IChatPipeline):
    def __init__(self):
        self.__last_msg = {}
        self.__counter = {}
        self.__last_trigger = {}
        self.__cool_down = timedelta(seconds=config.repeater_interruption['cool_down'])

    def on_init(self):
        for qq_group_number in config.repeater_interruption['qq_group']:
            self.__last_msg[qq_group_number] = ''
            self.__counter[qq_group_number] = 0
            self.__last_trigger[qq_group_number] = datetime.now()

    def execute(self, qq_group_number: str, qq: str, msg: str) -> str:
        if qq_group_number in config.repeater_interruption['qq_group']:
            now = datetime.now()

            if msg == self.__last_msg[qq_group_number]:
                self.__counter[qq_group_number] += 1
            else:
                self.__counter[qq_group_number] = 1

            if self.__counter[qq_group_number] >= config.repeater_interruption['allowance'] \
                    and now - self.__last_trigger[qq_group_number] > self.__cool_down:
                if '打断复读~~+(^-^)' in msg:
                    myqq.send_group_message(qq_group_number, '(*/ω\\*)')
                else:
                    myqq.send_group_message(qq_group_number, '打断复读~~ (^-^)')
                self.__counter[qq_group_number] = 1
                self.__last_trigger[qq_group_number] = now

            self.__last_msg[qq_group_number] = msg
        return msg
