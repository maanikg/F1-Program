import random
from turtle import width
from bs4 import BeautifulSoup
import requests
from PIL import ImageTk
from PIL import Image
from math import *
import fastf1
# from fastf1 import *
import pandas as pd
from team import *
from race import *
from track import *
from session import *
from tkinter import *
from tkinter.font import *
import os
import os.path


os.chdir(os.path.dirname(os.path.abspath(__file__)))


def init_drivers():
    init_drivers_session = get_session(2022, 3, 1)
    init_drivers_session.load()

    drivers.extend([Driver(first_name=driver.FirstName, last_name=driver.LastName,
                           full_name=driver.FullName, abbreviation=driver.Abbreviation, driver_number=driver.DriverNumber) for driver in init_drivers_session.results.itertuples()])

    driver_points_url = "https://www.formula1.com/en/results.html/2022/drivers.html"
    driver_points_html = requests.get(driver_points_url)
    driver_points_doc = BeautifulSoup(driver_points_html.text, "html.parser")

    driver_doc_contents = driver_points_doc.tbody.contents

    def join_names(name1, name2):
        return name1 + " " + name2

    for item in driver_doc_contents[1:-2:2]:
        driver_name1 = item.find(class_="hide-for-mobile").text.strip().lower()
        driver_name2 = item.find(class_="hide-for-tablet").text.strip().lower()
        for driver in drivers:
            if driver.full_name.lower() == join_names(driver_name1, driver_name2) or driver.full_name.lower() == join_names(driver_name2, driver_name1):
                # zhou guanyu confusion
                driver.points = (int)(item.contents[11].text.strip())
                for team in teams:
                    if team.f1_name == item.contents[9].text.strip():
                        driver.team = team

    drivers.sort(key=lambda x: x.points, reverse=True)
    for index in range(len(drivers)):
        drivers[index].position = index+1


def init_teams():
    team_points_url = "https://www.formula1.com/en/results.html/2022/team.html"
    team_points_html = requests.get(team_points_url)
    team_points_doc = BeautifulSoup(team_points_html.text, "html.parser")

    team_points_doc_contents = team_points_doc.tbody.contents
    for item in team_points_doc_contents[1::2]:
        for team in teams:
            if team.f1_name.lower() == item.contents[5].text.strip().lower():
                team.points = (int)(item.contents[7].text.strip())
                break

    teams_url = "https://www.formula1.com/en/teams.html"
    teams_html = requests.get(teams_url)
    teams_doc = BeautifulSoup(teams_html.text, "html.parser")

    teams_doc_contents = teams_doc.find_all(class_="col-12 col-md-6")
    for item in teams_doc_contents:
        for team in teams:
            team_name = item.find(
                class_="f1-color--black").string.strip().lower()
            if (str)(team.alt_name).lower() == team_name or team.name.lower() == team_name:
                team.logo_url = item.img['data-src']
                team.logo_filename = r"{}{}{}".format(
                    (TEAM_LOGO_FOLDER + "/"), team.name, ".png")

                if not os.path.isfile(team.logo_filename):
                    with open(team.logo_filename, "wb") as file:
                        file.write(requests.get(team.logo_url).content)
                team.logo = ImageTk.PhotoImage(
                    (PIL.Image.open(team.logo_filename)).resize(
                        (94, 94), PIL.Image.Resampling.LANCZOS)
                )
                break

    teams.sort(key=lambda x: x.points, reverse=True)

    for team in teams:
        team.drivers = [driver for driver in drivers if driver.team == team]


def init_races():
    schedule = get_event_schedule(2022)
    races_url = "https://www.formula1.com/en/racing/2022.html"
    races_html = requests.get(races_url)
    races_doc = BeautifulSoup(races_html.text, "html.parser")

    races_contents = races_doc.find_all(
        class_="col-12 col-sm-6 col-lg-4 col-xl-3")

    link_array = []
    for item in races_contents[2:]:
        head_tag = item.find(class_="event-item-wrapper event-item-link")
        raw_link = head_tag['href']
        link_array.append(raw_link)
    # temp_link_doc = BeautifulSoup(requests.get(
    #     ("http://www.formula1.com" + link_array[20])).text, "html.parser")
    # script = (temp_link_doc.find_all("script")[2]).text.strip()

    # print(script)
    # script_replaced = script.replace('{', '}').replace('"', '').split('}')
    # print(script_replaced[0])
    # script_dict = dict(item.split(":") for item in script_replaced[1].split(","))
    # print(script_dict)
    # script_dict_final = {
    #     key.strip():
    #     (value.strip().encode('iso-8859-1').decode("utf-8")
    #      ).encode('iso-8859-1').decode('unicode-escape')
    #     for (key, value) in script_dict.items()}

    # region ENABLE
    races.extend([Race(round=race.RoundNumber, country=race.Country,
                       official_title=race.OfficialEventName, name=race.EventName, location=race.Location, track_img_folder=TRACK_IMG_FOLDER, raw_link=link, event_reference=schedule.get_event_by_name(race.EventName))
                  for race in schedule.loc[schedule['RoundNumber'] != 0].itertuples() for link in link_array])
    # endregion

    # races.sort(key=lambda x: x.round, reverse=False)

    # region unneeded code
    # round_text = head_tag['data-roundtext'].lower()
    # round = (int)(round_text[round_text.find(" "):].strip())
    # country = head_tag['data-racecountryname']
    # year = (int)(head_tag['data-raceyear'].strip())
    # official_title = item.find(
    #     class_="event-title f1--xxs")['title'].encode('iso-8859-1').decode("utf-8")
    # races.append(Race(round=round, raw_link=raw_link, year=year,
    #              country=country, official_title=official_title, track_img_folder=TRACK_IMG_FOLDER))
    # endregion

    # for race, link in zip(races, link_array):
    #     race.raw_link = link
    return


def init_fonts():
    # head_team_name_font.config(family="")
    pass


def get_curr_time():
    return datetime.now().astimezone(datetime.now().utcoffset())


def get_local_utc_offset():
    curr_time = get_curr_time()
    curr_time_str = curr_time.strftime("%z")
    half_pos = ceil(len(curr_time_str)/2)
    first_half = curr_time_str[:half_pos]
    second_half = curr_time_str[half_pos:]
    return_str = ""
    if int(first_half) == 0 and int(second_half) == 0:
        return_str = "UTC"
    else:
        return_str = "UTC{}:{}".format(first_half, second_half)
    return return_str


def set_time_until():

    earlist_event_found = False
    for race in races:
        for session in race.sessions:
            if get_curr_time() < session.start_time_local:
                next_race_var.set("{} ({})".format(
                    race.official_title, session.name))
                if local_time.get():
                    next_session_time_str_var.set(
                        "Local Time ({}):".format(get_local_utc_offset()))
                    next_session_time_var.set(
                        session.start_time_local.strftime("%b %d %H:%M"))
                else:
                    next_session_time_str_var.set(
                        "Track Time (UTC{}):".format(session.gmt_offset))
                    next_session_time_var.set(
                        session.start_time.strftime("%b %d %H:%M"))
                countdown_str_var.set("Countdown:")
                # CHECK IF SESSION IS ONGOING

                time_until = session.start_time_local-get_curr_time()
                (time_until_days, time_until_hours, time_until_minutes,
                 time_until_seconds) = convert_time_until(time_until)

                if time_until.days >= 1:
                    countdown_var.set("{} days, {} hrs, {} mins".format(
                        time_until_days, time_until_hours, time_until_minutes))
                else:
                    countdown_var.set("{} hrs, {} mins, {} secs".format(
                        time_until_hours, time_until_minutes, time_until_seconds))
                earlist_event_found = True
                break
            elif get_curr_time() > session.start_time_local and get_curr_time() < session.end_time_local:
                next_race_var.set(
                    "{} ({} - LIVE)".format(race.official_title, session.name))
                # next_session_var.set("{} (LIVE)".format(session.name))
                next_session_time_var.set("")
                countdown_var.set("")
                earlist_event_found = True
                break
        if earlist_event_found:
            break


def convert_time_until(time):
    return (time.days, time.seconds//3600, (time.seconds//60) % 60, (time.seconds % 3600) % 60)


def update_countdown():
    set_time_until()
    main_window.after(1000, update_countdown)


def check_directory(directory):
    if not os.path.isdir(directory):
        os.mkdir(directory)


TEAM_LOGO_FOLDER = "Team Logos"
FASTF1_CACHE = "FastF1 Cache"
TRACK_IMG_FOLDER = "Track Images"
check_directory(TEAM_LOGO_FOLDER)
check_directory(FASTF1_CACHE)
check_directory(TRACK_IMG_FOLDER)

Cache.enable_cache(FASTF1_CACHE)


alfaromeo = Team("Alfa Romeo", pu="Ferrari",
                 main_color="#C92D4B", sec_color="#F9F9F8")
alpine = Team("Alpine", pu="Renault",
              main_color="#2293D1", sec_color="#FD4BC7")
alphatauri = Team("AlphaTauri", pu="RBPT",
                  main_color="#5E8FAA", sec_color="#F1F3F4")
astonmartin = Team("Aston Martin Aramco", pu="Mercedes", alt_name="Aston Martin",
                   main_color="#358C75", sec_color="#CEDC00")
haas = Team("Haas", alt_name="Haas F1 Team", pu="Ferrari", font_color="black",
            main_color="#B6BABD", sec_color="#F62039")
mclaren = Team("McLaren", pu="Mercedes", font_color="black",
               main_color="#F58020", sec_color="#47C7FC")
mercedes = Team("Mercedes", sec_color="#6CD3BF", font_color="black",
                main_color="#C6C6C6")  # 00A19C (aqua)
redbull = Team("Red Bull Racing", pu="RBPT",
               main_color="#3671C6", sec_color="#CC1E4A")
ferrari = Team("Ferrari", main_color="#F91536", sec_color="#FFEB00")
williams = Team("Williams", pu="Mercedes",
                sec_color="#37BEDD", main_color="#041E42")

teams = [alfaromeo, alpine, alphatauri, astonmartin,
         haas, mclaren, mercedes, redbull, ferrari, williams]

drivers = []
races = []

# organize graphics, etc. in functions
# Change font color, font

main_window = Tk()

init_drivers()
init_teams()
# init_races()

main_window.title("Formula One Racing Composite")
main_window.state('zoomed')

WIN_WIDTH = main_window.winfo_width()  # 1440 on Mac
WIN_HEIGHT = main_window.winfo_height()  # 799 on Mac
# MAX_LOGO_SIZE = (94, 94)

HEAD_RECT_HEIGHT = WIN_HEIGHT/5
HEAD_LINE_Y_POS = 8*HEAD_RECT_HEIGHT/9
HEAD_LINE_WIDTH = 5
HEAD_LABEL_WIDTH = WIN_WIDTH/3

head_rect_fill = StringVar()
head_accent_fill = StringVar()

head_rect_fill.set(teams[0].main_color)
head_accent_fill.set(teams[0].sec_color)

head_canvas = Canvas(main_window, width=WIN_WIDTH, height=HEAD_RECT_HEIGHT)
# head_frame = Frame(head_canvas, bg=teams[0].main_color)
head_frame = Frame(main_window, bg=teams[0].main_color)
head_rect = head_canvas.create_rectangle(
    0, 0, WIN_WIDTH, HEAD_RECT_HEIGHT, fill=teams[0].main_color, outline=teams[0].main_color)
head_accent = head_canvas.create_line(
    0, HEAD_LINE_Y_POS, WIN_WIDTH, HEAD_LINE_Y_POS, fill=head_accent_fill.get(), width=HEAD_LINE_WIDTH)
head_canvas.grid(row=0, column=0, sticky="nw", columnspan=3)
head_frame.grid(row=0, column=0, sticky="nw", padx=25, pady=25, columnspan=3)
main_window.grid_columnconfigure(0, weight=1)
main_window.grid_rowconfigure(0, weight=0)

logo_label = Label(head_frame, image=teams[0].logo)

# region label textvar's
team_name_var = StringVar()
team_pts_var = StringVar()
d1_name_var = StringVar()
d1_points_var = IntVar()
d2_name_var = StringVar()
d2_points_var = IntVar()
next_race_var = StringVar()
next_session_time_str_var = StringVar()
next_session_time_var = StringVar()
countdown_str_var = StringVar()
countdown_var = StringVar()
local_time = BooleanVar()
local_time.set(True)

team_name_var.set(teams[0].name)
team_pts_var.set("{} points".format(teams[0].points))

d1_name_var.set(
    "{}:".format(sorted(drivers, key=lambda x: x.team.points, reverse=True)[0].full_name))
d1_points_var.set(
    "{} points".format(sorted(drivers, key=lambda x: x.team.points, reverse=True)[0].points))
d2_name_var.set(
    "{}:".format(sorted(drivers, key=lambda x: x.team.points, reverse=True)[1].full_name))
d2_points_var.set(
    "{} points".format(sorted(drivers, key=lambda x: x.team.points, reverse=True)[1].points))
# endregion

set_time_until()

# init_fonts()

team_name_label = Label(head_frame, textvariable=team_name_var, font=(
    "Consolas", 30, ITALIC), anchor="sw")
team_points_label = Label(
    head_frame, textvariable=team_pts_var, anchor="nw", font=("Consolas", 22))
d1_name_label = Label(
    head_frame, textvariable=d1_name_var, anchor="se", font=("Consolas", 18))
d1_points_label = Label(head_frame, anchor="sw",
                        textvariable=d1_points_var, font=("Consolas", 18))
d2_name_label = Label(
    head_frame, textvariable=d2_name_var, anchor="ne", font=("Consolas", 18))
d2_points_label = Label(
    head_frame, textvariable=d2_points_var, anchor="nw", font=("Consolas", 18))
next_race_label = Label(head_frame, font=(
    "Consolas", 20, BOLD), anchor="se", textvariable=next_race_var)
next_session_time_str_label = Label(
    head_frame, anchor="e", textvariable=next_session_time_str_var, font=("Consolas", 18))
next_session_time_label = Label(
    head_frame, anchor="w", textvariable=next_session_time_var, font=("Consolas", 17))
countdown_str_label = Label(head_frame, anchor="e",
                            textvariable=countdown_str_var, font=("Consolas", 18))
countdown_label = Label(head_frame, anchor="w",
                        textvariable=countdown_var, font=("Consolas", 17))

head_labels = (logo_label, team_name_label, team_points_label, d1_name_label, d1_points_label,
               d2_name_label, d2_points_label, next_race_label, next_session_time_str_label,
               next_session_time_label, countdown_label, countdown_str_label)

# team_font = Font(family="Times New Roman",size=30)


def set_grid(widget, row, column, rowspan=1, columnspan=1):
    widget.grid(row=row, column=column, rowspan=rowspan,
                columnspan=columnspan, sticky="nsew")
    # widget.config(fg=teams[0].font_color)
    # widget.config(bg=teams[0].font_color)


set_grid(logo_label, 0, 0, 3)
set_grid(team_name_label, 0, 1)
set_grid(team_points_label, 1, 1, 2)
set_grid(d1_name_label, 0, 2)
set_grid(d2_name_label, 1, 2, 2)
set_grid(d1_points_label, 0, 3)
set_grid(d2_points_label, 1, 3, 2)
set_grid(next_race_label, 0, 4, 1, 2)
set_grid(next_session_time_str_label, 1, 4)
set_grid(countdown_str_label, 2, 4)
set_grid(next_session_time_label, 1, 5)
set_grid(countdown_label, 2, 5)

FRAME_HEIGHT = int((HEAD_LINE_Y_POS-50)//4)
NEXT_RACE_COL_WIDTH = int(WIN_WIDTH-748)

EMPTY_IMG = PhotoImage()
for label in head_frame.grid_slaves():
    if label.grid_info()['row'] == 0:
        label.config(height=2*FRAME_HEIGHT)
    else:
        label.config(height=FRAME_HEIGHT)
    if label.grid_info()["column"] != 0:
        label.config(image=EMPTY_IMG, compound=CENTER)
    match label.grid_info()['column']:
        case 0:
            pass
        case 1:
            label.config(width=300)
        case 2:
            label.config(width=200)
        case 3:
            label.config(width=150)
        case 4:
            label.config(width=(int)(NEXT_RACE_COL_WIDTH*2//3))
        case 5:
            label.config(width=NEXT_RACE_COL_WIDTH//3)
    label.config(bg=teams[0].main_color)
next_race_label.config(wraplength=NEXT_RACE_COL_WIDTH*3//4, justify='right')

team_var = IntVar()

for row in range(head_frame.grid_size()[1]):
    head_frame.grid_rowconfigure(row, weight=1)
for col in range(head_frame.grid_size()[0]):
    head_frame.grid_columnconfigure(col, weight=1)

# belgian_gp_url = "https://www.formula1.com/en/racing/2022/Belgium.html"
# belgian_gp_html = requests.get(belgian_gp_url)
# belgian_gp_doc = BeautifulSoup(belgian_gp_html.text, "html.parser")
# sessions_info = (belgian_gp_doc.find(
#     class_="f1-race-hub--timetable-listings")).find_all("div", recursive=False)

# region unneeded right now
# for session in sessions_info:
#     data_tracking = session.find(class_="f1-timetable--actions").a['href']
#     # if data_tracking.find(session.name.lower())!=-1:
#     # if name has practice: (different)
#     # if qualifying:
#     # q1
#     # else: scores, laps, total time, points, interval
#     print(data_tracking)
#     print("---")
# data_tracking = belgian_gp_doc.find()
# endregion


def update_team(team_index):
    curr_team = teams[team_index]
    team_name_var.set(curr_team.name)
    team_pts_var.set("{} points".format(curr_team.points))

    d1_name_var.set(
        "{}:".format(sorted(curr_team.drivers, key=lambda x: x.team.points, reverse=True)[0].full_name))
    d1_points_var.set(
        "{} points".format(sorted(curr_team.drivers, key=lambda x: x.team.points, reverse=True)[0].points))
    d2_name_var.set(
        "{}:".format(sorted(curr_team.drivers, key=lambda x: x.team.points, reverse=True)[1].full_name))
    d2_points_var.set(
        "{} points".format(sorted(curr_team.drivers, key=lambda x: x.team.points, reverse=True)[1].points))

    head_rect_fill.set(curr_team.main_color)
    head_accent_fill.set(curr_team.sec_color)

    head_canvas.itemconfig(
        head_rect, fill=head_rect_fill.get(), outline=curr_team.main_color)
    head_canvas.itemconfig(head_accent, fill=head_accent_fill.get())
    head_frame.config(bg=curr_team.main_color)

    for label in head_labels:
        label.config(bg=curr_team.main_color, fg=curr_team.font_color)

    logo_label.config(image=curr_team.logo)


def team_change(event):
    # CAN STILL BE MINIMIZED
    team_change_window = Toplevel()
    team_change_window.minsize(width=300, height=0)
    team_change_window.resizable(0, 0)
    team_change_window.title("Team Selection")
    team_change_window.grab_set_global()
    team_change_window.config(bg=teams[team_var.get()].main_color)

    for index in range(len(teams)):
        team_change_radio = Radiobutton(
            team_change_window,
            text="{} ({} points)".format(
                teams[index].name, str(teams[index].points)),
            variable=team_var,
            value=index,
            bg=teams[team_var.get()].main_color,
            fg=teams[team_var.get()].font_color
        )
        team_change_radio.pack(anchor=W)
    # team_change_window.config(anchor=W)

    def team_change_command():
        update_team(team_var.get())
        team_var.set(value=team_var.get())
        team_change_window.destroy()

    team_change_button = Button(
        team_change_window, text="Submit", command=team_change_command,
        # bg=teams[team_var.get()].main_color,
        highlightbackground=teams[team_var.get()].main_color
        # , fg=teams[team_var.get()].font_color
    )
    team_change_button.pack(anchor=CENTER)


def time_change(event):
    local_time.set(not local_time.get())


next_session_time_label.bind("<Button-1>", time_change)
logo_label.bind("<Button-1>", team_change)

laps_var = IntVar()
track_name_var = StringVar()
circuit_length_var = StringVar()
race_length_var = StringVar()
location_var = StringVar()
country_var = StringVar()
# add length unit

# region MAIN FRAME
main_frame = Frame(main_window)

track_img = ImageTk.PhotoImage((PIL.Image.open(f"{os.getcwd()}/Track Images/Circuit de Spa-Francorchamps.png")).resize(
    (888, 500), PIL.Image.Resampling.LANCZOS))
# 997,561
# img_test = PhotoImage(
#     file=f"{os.getcwd()}/Track Images/Bahrain International Circuit.png")
track_name_label = Label(main_frame, text="Circuit de Spa-Francorchamps",
                         border=1, relief=SOLID, font=("Consolas", 30))
# differentiate somehow if it is the next track (associated with upcoming event)
track_name_label.grid(row=1, column=0, sticky="nsew")

track_img_label = Label(main_frame, image=track_img,
                        borderwidth=1, relief=SOLID)
track_img_label.grid(row=2, column=0, sticky="nsew")

# main_frame.config(bg="blue")
main_frame.grid(row=1, column=1, sticky="ns")
main_window.grid_rowconfigure(1, weight=0)
# main_window.grid_columnconfigure(0, weight=0)
# endregion

# region FOOT FRAME
foot_frame = Frame(main_window, border=1, relief=SOLID)
# temp_label = Label(main_window,bg="red")
# temp_label.grid(row=2,column=0,sticky="nsew")
# main_window.grid_rowconfigure(2, weight=1)


location_label = Label(foot_frame, bg="red", anchor="sw", font=("Consolas", 30, BOLD),
                       text="Sakhir")  # , textvariable=location_var)
# textvariable=country_var)
country_label = Label(foot_frame, bg="black", text="Bahrain",
                      anchor="nw", font=("Consolas", 24))
laps_str_label = Label(foot_frame, bg="orange",
                       text='Laps:', anchor="e", font=("Consolas", 18))
laps_label = Label(foot_frame, bg="green", text="64", anchor="w", font=(
    "Consolas", 20, ITALIC))  # textvariable=laps_var)
circuit_length_str_label = Label(
    foot_frame, bg="purple", text='Circuit Length:', anchor="e", font=("Consolas", 18))
circuit_length_label = Label(
    foot_frame, bg="indigo", text="5.712 km", anchor="w", font=("Consolas", 20, ITALIC))  # textvariable=circuit_length_var)
race_length_str_label = Label(
    foot_frame, bg="violet", text='Race Length:', anchor="e", font=("Consolas", 18))
# textvariable=race_length_var)
race_length_label = Label(
    foot_frame, bg="blue", text="312.0 km", anchor="w", font=("Consolas", 20, ITALIC))

foot_labels = (location_label, country_label, laps_str_label,
               laps_label, circuit_length_str_label, circuit_length_label,
               race_length_str_label, race_length_label)

# region foot frame layout comments
# _          laps str    laps
# _
# location   c.str       c length
# country
# _          r. str      r length
# _
# endregion

set_grid(location_label, 0, 0, rowspan=3)
set_grid(country_label, 3, 0, rowspan=3)
set_grid(laps_str_label, 0, 1, rowspan=2)
set_grid(laps_label, 0, 2, rowspan=2)
set_grid(circuit_length_str_label, 2, 1, rowspan=2)
set_grid(circuit_length_label, 2, 2, rowspan=2)
set_grid(race_length_str_label, 4, 1, rowspan=2)
# changes bg color to team font color
set_grid(race_length_label, 4, 2, rowspan=2)

for label in foot_labels:
    label.config(border=0, relief=SOLID)
main_window.update()
FOOT_FRAME_HEIGHT = WIN_HEIGHT-head_canvas.winfo_height()-main_frame.winfo_height()
FOOT_FRAME_WIDTH = track_img_label.winfo_width()
foot_frame.config(height=FOOT_FRAME_HEIGHT, width=FOOT_FRAME_WIDTH)

for label in foot_frame.grid_slaves():
    label.config(border=0, relief=SOLID)
    label.config(image=EMPTY_IMG, compound=CENTER)
    label.config(height=int(FOOT_FRAME_HEIGHT//3))
    match label.grid_info()['column']:
        case 0:
            label.config(width=int(FOOT_FRAME_WIDTH/2))
        case 2:
            label.config(width=int(FOOT_FRAME_WIDTH/8))
        case 1:
            label.config(width=int(FOOT_FRAME_WIDTH/2) -
                         int(FOOT_FRAME_WIDTH/8))

for row in range(foot_frame.grid_size()[1]):
    foot_frame.grid_rowconfigure(row, weight=1)
for col in range(foot_frame.grid_size()[0]):
    foot_frame.grid_columnconfigure(col, weight=1)

foot_frame.config(border=0, relief=SOLID)
foot_frame.grid(row=2, column=1, sticky="ns")

# endregion

# region LEFT FRAME (all tracks)
left_frame = Frame(main_window, border=1, relief=SOLID)
LEFT_FRAME_WIDTH = (WIN_WIDTH - track_img_label.winfo_width())/2
LEFT_FRAME_HEIGHT = WIN_HEIGHT - head_canvas.winfo_height()
# for race in races:
#     pass

# left_frame.grid(row=1, column=0, sticky="nsew", rowspan=2)
left_frame.config(bg="red", width=LEFT_FRAME_WIDTH, height=LEFT_FRAME_HEIGHT)

# region test_race frame (currently inactive)
# TEST_RACE_WIDTH = 255
# temp_frame = Frame(left_frame, border =1, relief=SOLID)
# temp_frame.config(width = TEST_RACE_WIDTH, height = 100)
# temp_frame.grid(row=0,column=0, sticky="nsew")
# temp_frame.config(bg="orange")
# # left_frame.update()

# races_name = Label(temp_frame, text="Belgian Grand Prix", font = ("Consolas", 23, BOLD),bg="green", anchor = NW)
# races_name.grid(row=0,column=0, columnspan=3, sticky="nsew")
# races_name.config(image = EMPTY_IMG)
# races_name.config(width=TEST_RACE_WIDTH,compound=LEFT)

# races_name2 = Label(temp_frame, text="Circuit de Spa-Francorchamps", font = ("Consolas", 18),bg="blue", anchor = W)
# races_name2.grid(row=1,column=0, columnspan=3,sticky="nsew")
# races_name2.config(image = EMPTY_IMG)
# races_name2.config(width=TEST_RACE_WIDTH,compound=LEFT)
# # races_name2.config(image = EMPTY_IMG)
# # races_name2.config(width=LEFT_FRAME_WIDTH/2,compound=LEFT)
# races_name3 = Label(temp_frame,text="Sep 12 2022", font=("Consolas", 18),anchor = W)
# races_name3.grid(row=2,column=0, columnspan=3,sticky="nsew")
# races_name3.config(image = EMPTY_IMG)
# races_name3.config(width=TEST_RACE_WIDTH,compound=LEFT)

# dr1 = Label(temp_frame, text = "1 VER", font= ("Consolas", 16),anchor = W)
# dr1.grid(row=3, column=0, sticky="nsew")
# dr2 = Label(temp_frame, text = "2 PER", font= ("Consolas", 16), anchor = W)
# dr2.grid(row=3, column=1, sticky="nsew")
# dr3 = Label(temp_frame, text = "3 LEC", font= ("Consolas", 16), anchor = W)
# dr3.grid(row=3, column=2, sticky="nsew")
# endregion

left_frame.grid(row=1, column=0, sticky=NSEW, rowspan=2)
# region scrollbar functionality (currently active)
tracks_canvas = Canvas(left_frame)
tracks_scrollbar = Scrollbar(
    left_frame, orient=VERTICAL, command=tracks_canvas.yview)
scroll_frame = Frame(tracks_canvas)

tracks_scrollbar.pack(side=LEFT, fill=Y)
tracks_canvas.pack(side=RIGHT, fill=BOTH, expand=True)

main_window.update()
SCROLLBAR_WIDTH = tracks_scrollbar.winfo_width()
LEFT_FRAME_RACE_FRAME_WIDTH = LEFT_FRAME_WIDTH-SCROLLBAR_WIDTH-5
print(LEFT_FRAME_RACE_FRAME_WIDTH)

scroll_frame.bind(
    "<Configure>",
    lambda e: tracks_canvas.configure(
        scrollregion=tracks_canvas.bbox("all")
    )
)
tracks_canvas.create_window((0, 0), window=scroll_frame, anchor=NW)
tracks_canvas.configure(yscrollcommand=tracks_scrollbar.set)
for i in range(50):
    temp_frame = Frame(scroll_frame, width=LEFT_FRAME_RACE_FRAME_WIDTH, height=20, border=1,  # LEFT_FRAME_WIDTH-25
                       bg="orange",  # "#"+("%06x"%random.randint(0,16777215)),
                       relief=SOLID)
    temp_frame.pack()

    def temp_frame_click(event):
        event.widget.config(bg="red")
    temp_frame.bind("<Button-1>", temp_frame_click)

# temp_frames = list(scroll_frame.children.values())
# for frame in temp_frames:
#     def temp_frame_click(event):
#         event.widget.config(bg="red")
#         # print(temp_frames.index())
#     frame.bind("<Button-1>", temp_frame_click)


def _bound_to_mousewheel(event):
    tracks_canvas.bind_all("<MouseWheel>", _on_mousewheel)
    print("enter")


def _unbound_to_mousewheel(event):
    tracks_canvas.unbind_all("<MouseWheel>")
    print("leave")


def _on_mousewheel(event):
    tracks_canvas.yview_scroll(int(-1*(event.delta)), "units")


tracks_canvas.bind_all("<MouseWheel>", _on_mousewheel)
left_frame.bind('<Enter>', _bound_to_mousewheel)
left_frame.bind('<Leave>', _unbound_to_mousewheel)
# endregion
# endregion

# region RIGHT FRAME (??)
right_frame = Frame(main_window, border=1, relief=SOLID)
RIGHT_FRAME_WIDTH = LEFT_FRAME_WIDTH
RIGHT_FRAME_HEIGHT = LEFT_FRAME_HEIGHT
right_frame.grid(row=1, column=2, rowspan=2)
right_frame.config(bg="blue", width=RIGHT_FRAME_WIDTH,
                   height=RIGHT_FRAME_HEIGHT)

# endregion

# label_test2 = Label(main_window, bg="red")
# label_test2.grid(row=2, column=0, sticky="nsew")
# main_window.grid_rowconfigure(2, weight=1)

# label_test3 = Label(main_window, bg="blue")
# label_test3.grid(row=3, column=0, sticky="nsew")
# main_window.grid_rowconfigure(3, weight=1)

# label_test4 = Label(main_window, bg="green")
# label_test4.grid(row=4, column=0, sticky="nsew")
# main_window.grid_rowconfigure(4, weight=1)

# team_name_label.bind("<Button-1>", team_change)
# team_points_label.bind("<Button-1>", team_change)

# logo_label.config(bg="navy")

# lab3 = Label(main_window,bg="orange",text="lab3",width=100,anchor=W)
# lab3.grid(row=1,column=0,pady=40)

# print(head_frame.winfo_rootx())
# print(head_frame.winfo_rooty())
# label = Label(head_frame,bg="red",text="hello")
# label.grid(row=0,column=0)
# lab3 = Label(head_frame,bg="navy",text="hi")
# lab3.grid(row=1,column=1)

# label2 = Label(main_window,bg="yellow",text="t2")
# label2.grid(row=1,column=0)

# frame.pack(side=TOP)
# frame.place(x=10,y=10)
# label.pack(x=0,y=0)
# frame.place(x=0,y=0)

# head_back_frame = Frame(main_window,width=WIN_WIDTH,height=HEAD_RECT_HEIGHT,bg="black",borderwidth=0)
# label= Label(head_back_frame,width=1,bg="red")
# label.pack()
# head_back_frame.pack()
# head_frame = Frame(main_window,bg="yellow",borderwidth=2)
# head_team_label = Label(head_frame,text="TEAM NAME").grid(row=0,column=0)
# head_frame.pack()

# gap = 5
# line = header_canvas.create_line(0,gap,WIN_WIDTH,gap,fill="red",width=1)

# header_canvas.itemconfig(line,fill="orange") --> works
# label1 = Label(main_window,bg="red",width=WIN_WIDTH,height=1)
# label1.pack()
# header_frame = Frame(main_window)

# main_window.update() #94x94

# print(time.time())
# main_window.update()
# print(logo_label.winfo_width())

update_countdown()
main_window.mainloop()
# main_window.deiconify()
