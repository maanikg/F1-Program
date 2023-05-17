from datetime import datetime
# from fast_f1 import *
from fastf1 import *
# import time


class Session:
    def __init__(self, name="", gmt_offset="", start_string="", end_string="",session_number=0, session_reference = None):
        self.name = name
        self.gmt_offset = gmt_offset
        self.start_time = datetime.strptime(
            (start_string+gmt_offset), "%Y-%m-%dT%X%z")
        self.end_time = datetime.strptime(
            (end_string+gmt_offset), "%Y-%m-%dT%X%z")

        self.start_time_local = (self.start_time).astimezone(
            datetime.now().utcoffset())
        self.end_time_local = (self.end_time).astimezone(
            datetime.now().utcoffset())
        self.session_number = session_number
        self.session_reference = session_reference
        # self.session_reference.load()

        # self.started = False
        # self.completed = False
        # curr_time = datetime.now().astimezone(datetime.now().utcoffset())
        # if curr_time > self.start_time_local:
        #     self.started = True
        #     if curr_time > self.end_time_local:
        #         self.completed = True
