# from track import *
import time
import requests
from bs4 import BeautifulSoup
from session import *
from track import *
from fastf1 import *
import fastf1

#Session - FP1, FP2, FP3, Qualifying, Race


class Race:

    def link_convert(self, link):
        return "http://www.formula1.com"+link

    # def find_session(self, session_name):
    #     for session in self.sessions:
    #         if session.name == session_name:
    #             return session
# load sessions
    def __init__(self, country="", name="", round=0, raw_link="", official_title="", track_img_folder="", location="", event_reference=None):
        self.link = self.link_convert(raw_link)
        self.location = location
        self.official_title = official_title
        self.name = name
        self.country = country
        self.round = round
        self.event_reference = event_reference

        race_link_html = requests.get(self.link)
        race_link_doc = BeautifulSoup(race_link_html.text, "html.parser")

        script = (race_link_doc.find_all("script")[2]).text.strip()
        script_replaced = script.replace('{', '}').replace('"', '').split('}')
        script_dict = dict(item.split(":")
                           for item in script_replaced[1].split(","))
        script_dict_final = {
            key.strip():
            (value.strip().encode('iso-8859-1').decode("utf-8")
             ).encode('iso-8859-1').decode('unicode-escape')
            for (key, value) in script_dict.items()}

        track_name = script_dict_final['trackName']
        # track_city = script_dict_final['trackCity']

        self.sessions = []
        sessions_info = (race_link_doc.find(
            class_="f1-race-hub--timetable-listings")).find_all("div", recursive=False)
        for session_info in reversed(sessions_info):
            session_name = session_info.find(
                class_="f1-timetable--title").text
            gmt_offset = session_info['data-gmt-offset']
            session_start_string = session_info['data-start-time']
            session_end_string = session_info['data-end-time']
            session_reference = event_reference.get_session(session_name)
            self.sessions.append(Session(name=session_name, gmt_offset=gmt_offset,
                                 start_string=session_start_string, end_string=session_end_string))#, session_reference=session_reference))
        for i in range(0, 5):
            self.sessions[i].session_number = i+1
        self.sessions.sort(key=lambda x: x.session_number)
        # self.sessions.sort(key=lambda x: x.start_time)

        raw_circuit_link = race_link_doc.find("a", text="Circuit")['href']
        circuit_link = self.link_convert(raw_circuit_link)

        self.track = Track(circuit_link=circuit_link, location=location,
                           name=track_name, track_img_folder=track_img_folder, country=country)
