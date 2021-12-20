import sched
import threading
import time
from datetime import datetime


class Schedule:
    def __init__(self):
        self.__id = 0
        self.__scheduler = sched.scheduler(time.time, time.sleep)
        self.cache: dict[int, sched.Event] = {}

    def run(self):
        threading.Thread(target=self.__scheduler.run, daemon=True).start()

    def add(self, delay: int, action, argument=()) -> None:
        event = self.__scheduler.enter(delay, 1, action, argument)
        self.__id += 1
        self.cache[self.__id] = event

    def addabs(self, date_obj: datetime, action, argument=()) -> None:
        event = self.__scheduler.enterabs(date_obj, 1, action, argument)
        self.__id += 1
        self.cache[self.__id] = event

    def remove(self, idx: int) -> bool:
        try:
            schedule_data = self.cache.pop(idx)
            self.__scheduler.cancel(schedule_data.event)
        except KeyError:
            return False


schedule = Schedule()
