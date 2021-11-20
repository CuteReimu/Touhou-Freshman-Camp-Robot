import chat_pipeline
import myqq
import config


class RepeaterInterruptionPipeline(chat_pipeline.IChatPipeline):
    def on_init(self):
        self.counter = 0
        self.last_msg = ''

    def execute(self, qq_group_number: str, qq: str, msg: str) -> str:
        if qq_group_number in config.repeater_interruption['qq_group']:
            if self.counter >= config.repeater_interruption['allowance']\
            and msg == '打断复读~~ (^-^)':
                myqq.send_group_message(qq_group_number, '(*/ω＼\*)')
                self.counter = 0
            elif self.counter >= config.repeater_interruption['allowance']:
                myqq.send_group_message(qq_group_number, '打断复读~~ (^-^)')
                self.counter = 0
            if msg == self.last_msg:
                self.counter += 1
            else:
                self.counter = 1
            self.last_msg = msg
        return msg
