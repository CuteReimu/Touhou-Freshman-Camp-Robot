import sched
import threading
import time
from datetime import datetime


class Schedule:
    def __init__(self):
        self.__lock = threading.Lock()
        self.__id = 0
        self.__scheduler = sched.scheduler(time.time, time.sleep)
        self.cache: dict[int, sched.Event] = {}

    def run(self):
        threading.Thread(target=self.__scheduler.run, daemon=True).start()

    def __action(self, action, action_id: int):
        with self.__lock:
            try:
                self.cache.pop(action_id)
            except KeyError:
                pass
        action()

    def add(self, delay: int, action, argument=()) -> int:
        with self.__lock:
            self.__id += 1
            if delay > 0:
                event = self.__scheduler.enter(delay, 1, self.__action(action, self.__id), argument)
                self.cache[self.__id] = event
            else:
                action()
            return self.__id

    def addabs(self, date_obj: datetime, action, argument=()) -> int:
        with self.__lock:
            self.__id += 1
            if date_obj > datetime.now():
                event = self.__scheduler.enterabs(date_obj, 1, action, argument)
                self.cache[self.__id] = event
            else:
                action()
            return self.__id

    def remove(self, idx: int) -> bool:
        with self.__lock:
            try:
                schedule_data = self.cache.pop(idx)
                self.__scheduler.cancel(schedule_data.event)
            except KeyError:
                return False


schedule = Schedule()
