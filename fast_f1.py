# from cgi import test
import sys
from contextlib import contextmanager
import sched
import fastf1
from fastf1 import plotting
from matplotlib import pyplot as plt
import os
from datetime import datetime, tzinfo

os.chdir(os.path.dirname(os.path.abspath(__file__)))

plotting.setup_mpl()

fastf1.Cache.enable_cache('fastf1_cache')  # optional but recommended

# from contextlib import contextmanager
# import sys, os
# class HiddenPrints:
#     def __enter__(self):
#         self._original_stdout = sys.stdout
#         sys.stdout = open(os.devnull, 'w')

#     def __exit__(self, exc_type, exc_val, exc_tb):
#         sys.stdout.close()
#         sys.stdout = self._original_stdout

# @contextmanager
# def suppress_stdout():
#     with open(os.devnull, "w") as devnull:
#         old_stdout = sys.stdout
#         sys.stdout = sys.stdderr = devnull
#         try:
#             yield
#         finally:
#             sys.stdout = old_stdout


# print ("You can see this")
# with HiddenPrints():
#     print("You cannot see this")
# print ("And you can see this again")

# pass
# @contextmanager
# def suppress_stdout():
#     with open(os.devnull, "w") as devnull:
#         pass
#         old_stderr = sys.stdout
#         sys.stdout = devnull
#         try:
#             yield
#         finally:
#             sys.stdout = old_stderr

# race = fastf1.get_session(2020, 'Turkish Grand Prix', 'R')
# race.load()

# lec = race.laps.pick_driver('LEC')
# ham = race.laps.pick_driver('HAM')

# fig, ax = plt.subplots()
# ax.plot(lec['LapNumber'], lec['LapTime'], color='red')
# ax.plot(ham['LapNumber'], ham['LapTime'], color='cyan')
# ax.set_title("LEC vs HAM")
# ax.set_xlabel("Lap Number")
# ax.set_ylabel("Lap Time")
# plt.show()
#####
# session = fastf1.get_session(2019, 'Monza', 'Q')
# session.load(telemetry=False, laps=False, weather=False)
# vettel = session.get_driver('VET')
# print(f"Pronto {vettel['FirstName']}?")
#####
# session = fastf1.get_event(2022,1)
# print(session.get_session_date(5))
# print(session.event.get_session_name(1))
# print(session)
# print(session.date)
# print(session.event)
# print(session.event['Session3'])
# with suppress_stdout():
# sys.stdout = sys.stderr = os.devnull
# with HiddenPrints():
event = fastf1.get_event(2022, 'Singapore Grand Prix')
quali = event.get_session("Qualifying")
quali.load()
print(quali)

# ver_lap = quali.laps.pick_driver('PER').pick_fastest()
# lec_lap = quali.laps.pick_driver('LEC').pick_fastest()

# ver_tel = ver_lap.get_car_data().add_distance()
# ham_tel = lec_lap.get_car_data().add_distance()

# rbr_color = fastf1.plotting.team_color('RBR')
# fer_color = fastf1.plotting.team_color('FER')

# fig, ax = plt.subplots()
# ax.plot(ver_tel['Distance'], ver_tel['Speed'], color=rbr_color, label='PER')
# ax.plot(ham_tel['Distance'], ham_tel['Speed'], color=fer_color, label='LEC')

# ax.set_xlabel('Distance in m')
# ax.set_ylabel('Speed in km/h')

# ax.legend()
# plt.suptitle(f"Fastest Lap Comparison \n "
#              f"{quali.event['EventName']} {quali.event.year} Qualifying")

# plt.show()
# fp1 = event.get_session("Sprint")
# fp1.load()
# print(fp1)

schedule = fastf1.get_event_schedule(2022)
print(schedule.columns)
print(schedule.loc[schedule['RoundNumber'] != 0].iloc[:,5:7])
print(schedule.get_event_by_name("Italian Grand Prix").get_race())

# session = fastf1.get_session(2022,'Bahrain')
# session = event
# session.load()
# print(session.results.FullName)
# print(session)
# sprint = event.get_qualifying()
# sprint.load()
# sys.stdout, sys.stderr = sys.__stdout__, sys.__stderr__
# print(sprint.results)


# session.load()
# print(dir(session))
# print(session.t0_date)
# print(session.Location)
# print(event.loc['Session3Date'])
# print(event.date)
# print(type(a))
# print(event.get_session_date(5))

# schedule = fastf1.get_event_schedule(2022)
# print(schedule['EventName'])
# print(schedule.Location)
# print(schedule.Country)
# print(session)
# print(schedule.loc[schedule['RoundNumber'] != 0])
# print(schedule.is_testing())

# for round in schedule:
#     if round!=0: print(round)
# print(schedule)
# print(schedule['Session3'])
# print(schedule.iloc[:,1:4])
# print(schedule.loc[1:4])
# spa = fastf1.get_session(2022, 'Belgium','Race')
# spa.load()
# bahrain = fastf1.get_session(2022, 3, 1)
# bahrain.load()
# a=bahrain.results
# print(a.columns)
# print(a['TeamName'])
# print(a[-5:-1])
# print(bahrain.results[])
# drivers = []
# for driver in bahrain.results['FullName']:
#     print(driver)
#     print()
# testing = fastf1.get_testing_session(2022,2,1)
# testing.load()
# print(testing.results['FullName'])

# print(len(bahrain.results))
# print(bahrain.results['Abbreviation'])
# bahrain_results = fastf1.core.
# print(spa.laps['Driver'])
# print(spa.laps)
# for index in range(20):
#     print(spa.results['FullName'][index])
#     print(spa.results['DriverNumber'][index])
#     print("--")
# for driver_num, name in spa.results['FullName'].iterrows():
    # print(driver_num)
# print(spa.columns)
# print(spa.results.iloc[0:10].loc[:, ['Abbreviation', 'Q3']])
# print(spa.results.columns)
# print(spa.results['Points'])
