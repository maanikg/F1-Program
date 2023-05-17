from bs4 import BeautifulSoup
import requests
import time
import os


class Track:
    # make lap_record time object
    def __init__(self, name="", circuit_link="", track_img_folder="",country = "",location = ""): #city=""):
        self.name = name
        self.location = location
        self.country = country
        self.circuit_link = circuit_link

        circuit_link_html = requests.get(circuit_link)
        circuit_link_doc = BeautifulSoup(circuit_link_html.text, "html.parser")

        circuit_length_text = (circuit_link_doc.find_all(
            class_="f1-stat")[2].find_all("p")[1].text)
        race_length_text = (circuit_link_doc.find_all(
            class_="f1-stat")[3].find_all("p")[1].text)

        self.num_laps = (int)(circuit_link_doc.find_all(
            class_="f1-stat")[1].find_all("p")[1].text)
        self.length_unit = ''.join(
            x for x in circuit_length_text if x.isalpha())
        self.circuit_length = (float)(circuit_length_text[:circuit_length_text.find(
            self.length_unit)])
        self.race_length = (float)(
            race_length_text[:race_length_text.find(self.length_unit)])

        self.img_url = circuit_link_doc.find_all(
            "picture", class_="f1-external-link--no-image")[1].find("img")['data-src']
        self.img_filename = r"{}{}{}".format(
            (track_img_folder + "/"), name, ".png")

        if not os.path.isfile(self.img_filename):
            with open(self.img_filename, "wb") as file:
                file.write(requests.get(self.img_url).content)
