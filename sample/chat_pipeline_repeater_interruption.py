import chat_pipeline
import config
import myqq
from datetime import datetime
from datetime import timedelta


class RepeaterInterruptionPipeline(chat_pipeline.IChatPipeline):
    def __init__(self):
        self.last_msg = {}
        self.counter = {}
        self.last_trigger = {}
        self.cool_down = timedelta(seconds=config.repeater_interruption['cool_down'])

    def on_init(self):
        for qq_group_number in config.repeater_interruption['qq_group']:
            self.last_msg[qq_group_number] = ''
            self.counter[qq_group_number] = 0
            self.last_trigger[qq_group_number] = datetime.today()

    def execute(self, qq_group_number: str, qq: str, msg: str) -> str:
        if qq_group_number in config.repeater_interruption['qq_group']:
            now = datetime.today()

            if msg == self.last_msg[qq_group_number]:
                self.counter[qq_group_number] += 1
            else:
                self.counter[qq_group_number] = 1

            if self.counter[qq_group_number] >= config.repeater_interruption['allowance'] \
                    and now - self.last_trigger[qq_group_number] > self.cool_down:
                if '打断复读~~+(^-^)' in msg:
                    myqq.send_group_message(qq_group_number, '(*/ω\\*)')
                else:
                    myqq.send_group_message(qq_group_number, '打断复读~~ (^-^)')
                self.counter[qq_group_number] = 1
                self.last_trigger[qq_group_number] = now

            self.last_msg[qq_group_number] = msg
        return msg
