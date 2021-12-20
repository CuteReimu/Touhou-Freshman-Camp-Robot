import chat_pipeline
import chat_pipeline_bilibili_video
import chat_pipeline_repeater_interruption
import chat_pipeline_update


def deal_with_msg(qq_group_number: str, qq: str, msg: str):
    for pipeline in chat_pipeline.pipelines:
        msg = pipeline.execute(qq_group_number, qq, msg)
        if msg == '':
            break


def __init_chat_pipeline(pipeline: chat_pipeline.IChatPipeline):
    pipeline.on_init()
    chat_pipeline.pipelines.append(pipeline)


def init_chat_pipeline():
    __init_chat_pipeline(chat_pipeline.MessagePipeline())
    __init_chat_pipeline(chat_pipeline_bilibili_video.BilibiliVideoPipeline())
    __init_chat_pipeline(chat_pipeline_repeater_interruption.RepeaterInterruptionPipeline())
    __init_chat_pipeline(chat_pipeline_update.UpdatePipeline())
