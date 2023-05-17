# from main import *
from team import *


class Driver:
    def __init__(self, full_name="", number=0, nationality=None, team=None,
                 points=0, position=0, last_name="", first_name="", abbreviation="", driver_number=0):
        self.full_name = full_name
        self.first_name = first_name
        self.abbreviation = abbreviation
        self.driver_number = driver_number
        self.last_name = last_name
        self.number = number
        self.nationality = nationality
        self.team = team
        self.points = points
        self.position = position
