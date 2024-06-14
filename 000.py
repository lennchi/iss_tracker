import requests
from datetime import datetime
import smtplib
import time
import config


LAT = 50.1570
LNG = 14.7447
MY_COOR_MIN = (45.15, 9.74)
MY_COOR_MAX = (55.15, 19.74)


def is_daytime():
    """ Check if it's currently nighttime in Celakovice based on sunset and sunrise times """
    response = requests.get(url=f"https://api.sunrise-sunset.org/json?lat={LAT}&lng={LNG}&formatted=0")
    response.raise_for_status()
    sunset_str = response.json()["results"]["sunset"][11:16]
    sunrise_str = response.json()["results"]["sunrise"][11:16]
    sunset = datetime.strptime(sunset_str, "%H:%M").strftime("%H:%M")
    sunrise = datetime.strptime(sunrise_str, "%H:%M").strftime("%H:%M")
    now = datetime.now().strftime("%H:%M")
    return sunset > now > sunrise