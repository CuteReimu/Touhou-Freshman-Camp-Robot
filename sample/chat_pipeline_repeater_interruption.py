import chat_pipeline
import mirai_bot
from mirai_bot_chain import plain


counter = 1
last_msg = ""


class RepeaterInterruptionPipeline(chat_pipeline.IChatPipeline):
    def on_init(self):
        pass

    def execute(self, qq_group_number: int, qq: int, msg_chain: list) -> str:
        global counter
        global last_msg
        
        if len(msg_chain) == 2 and msg_chain[1]['type'] == 'Plain':
            msg = msg_chain[1]['text']
            if counter >= 4 and msg == "打断复读 ^-^":
                mirai_bot.send_group_message(qq_group_number, [plain("(*/ω＼\*)")])
                counter = 1
            elif counter >= 4:
                mirai_bot.send_group_message(qq_group_number, [plain("打断复读~~ (^-^)")])
                counter = 1
            if msg == last_msg:
                counter += 1
            else:
                counter = 1
            last_msg = msg
                
        return msg