import chat_pipeline
import mirai_bot
from mirai_bot_chain import plain
import config


class RepeaterInterruptionPipeline(chat_pipeline.IChatPipeline):
    def on_init(self):
        self.counter = 1
        self.last_msg_chain = []

    def execute(self, qq_group_number: int, qq: int, msg_chain: list) -> str:
        if qq_group_number in config.repeater_interruption['qq_group']:
            if self.counter >= config.repeater_interruption['allowance'] \
            and msg_chain[1]['type'] == 'Plain' \
            and msg_chain[1]['text'] == '打断复读~~ (^-^)':
                mirai_bot.send_group_message(qq_group_number, [plain('(*/ω＼\*)')])
                self.counter = 0
            elif self.counter >= config.repeater_interruption['allowance']:
                mirai_bot.send_group_message(qq_group_number, [plain('打断复读~~ (^-^)')])
                self.counter = 0
            if self.__equals(msg_chain, self.last_msg_chain):
                self.counter += 1
            else:
                self.counter = 1
            self.last_msg_chain = msg_chain
        return ' '

    def __equals(msg_chain: list, last_msg_chain: list) -> bool:
        if len(msg_chain) < 2 or len(msg_chain) != len(last_msg_chain):
            return False

        for msg_idx in range(1, len(msg_chain)):
            if msg_chain[msg_idx]['type'] != last_msg_chain[msg_idx]['type']:
                return False

            if msg_chain[msg_idx]['type'] == 'Plain':
                if msg_chain[msg_idx]['text'] == last_msg_chain[msg_idx]['text']:
                    return True
            elif msg_chain[msg_idx]['type'] == 'At':
                if msg_chain[msg_idx]['target'] == last_msg_chain[msg_idx]['target']:
                    return True
            elif msg_chain[msg_idx]['type'] == 'Image':
                if msg_chain[msg_idx]['imageId'] == last_msg_chain[msg_idx]['imageId']:
                    return True
                elif msg_chain[msg_idx]['url'] == last_msg_chain[msg_idx]['url']:
                    return True

        return False
