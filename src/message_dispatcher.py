import message
import message_admin
import message_live
import message_schedule
import message_thwiki
import message_vote
import message_whitelist


def __init_message(msg: message.IMessageDispatcher):
    if msg.name in message.messages:
        raise KeyError
    message.messages[msg.name] = msg


def init_message():
    message_admin.on_init()
    message_whitelist.on_init()
    message_schedule.on_init()
    message_vote.on_init()
    # __init_message(message.Test())
    __init_message(message.GetTips())
    __init_message(message.GetTips2())
    __init_message(message_admin.GetAdmin())
    __init_message(message_admin.DelAdmin())
    __init_message(message_admin.AddAdmin())
    __init_message(message_whitelist.GetWhitelist())
    __init_message(message_whitelist.DelWhitelist())
    __init_message(message_whitelist.AddWhitelist())
    __init_message(message_whitelist.CheckWhitelist())
    __init_message(message_live.GetLiveState())
    __init_message(message_live.StartLive())
    __init_message(message_live.StopLive())
    __init_message(message_live.ChangeLiveTitle())
    __init_message(message_schedule.AddSchedule())
    __init_message(message_schedule.DelSchedule())
    __init_message(message_schedule.ListAllSchedule())
    __init_message(message_vote.AddVote())
    __init_message(message_vote.DelVote())
    __init_message(message_vote.ShowVote())
    __init_message(message_vote.DoVote())
    __init_message(message_vote.AddVoteForbiddenWords())
    __init_message(message_vote.DelVoteForbiddenWords())
    __init_message(message_thwiki.GetEvents())
