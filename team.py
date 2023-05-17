from driver import Driver
import PIL.Image
from PIL import ImageTk


class Team:

    def __init__(self, name="", main_color=None, sec_color=None, points=0, pu=None, alt_name=None, font_color = "white"):
        self.name = name
        self.alt_name = alt_name
        self.pu = pu
        self.main_color = main_color
        self.sec_color = sec_color
        self.font_color = font_color
        self.drivers = []
        self.points = points
        self.logo_url = ""
        self.logo_filename = ""
        self.logo = None
        self.f1_name = (name + " " + (pu if not pu == None else "")).strip()
