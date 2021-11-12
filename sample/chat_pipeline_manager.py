import chat_pipeline
import chat_pipeline_bilibili_video


def deal_with_msg(qq_group_number: int, qq: int, msg_chain: list):
    for pipeline in chat_pipeline.pipelines:
        msg = pipeline.execute(qq_group_number, qq, msg_chain)
        if msg == '':
            break


def __init_chat_pipeline(pipeline: chat_pipeline.IChatPipeline):
    pipeline.on_init()
    chat_pipeline.pipelines.append(pipeline)


def init_chat_pipeline():
    __init_chat_pipeline(chat_pipeline.MessagePipeline())
    __init_chat_pipeline(chat_pipeline_bilibili_video.BilibiliVideoPipeline())
