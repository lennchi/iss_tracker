import requests
from datetime import datetime, timezone, timedelta
import smtplib
import time
import config


LAT = 50.1570
LNG = 14.7447
MY_COOR_MIN = (45.15, 9.74)
MY_COOR_MAX = (55.15, 19.74)
CEST_TZ = timezone(timedelta(hours=2))


def is_nighttime():
    """ Check if it's currently nighttime in Celakovice (CEST) based on sunset/sunrise times """
    response = requests.get(url=f"https://api.sunrise-sunset.org/json?lat={LAT}&lng={LNG}&formatted=0")
    response.raise_for_status()

    sunset_str = response.json()["results"]["sunset"][11:16]
    sunset_utc = datetime.strptime(sunset_str, "%H:%M")
    sunset = sunset_utc.replace(tzinfo=timezone.utc).astimezone(CEST_TZ).strftime("%H:%M")

    sunrise_str = response.json()["results"]["sunrise"][11:16]
    sunrise_utc = datetime.strptime(sunrise_str, "%H:%M")
    sunrise = sunrise_utc.replace(tzinfo=timezone.utc).astimezone(CEST_TZ).strftime("%H:%M")
    now = datetime.now().strftime("%H:%M")
    return False if sunrise < now < sunset else True

def check_iss():
    """ Return the ISS's current position """
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()

    iss_lat = float(response.json()["iss_position"]["latitude"])
    iss_lng = float(response.json()["iss_position"]["longitude"])
    return iss_lat, iss_lng


def send_email():
    """ Notify me if the ISS is overhead """
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=config.email, password=config.psw)
        connection.sendmail(from_addr=config.email,
                            to_addrs=config.recipient,
                            msg=f"Subject: Look up!\n\nThe ISS is flying over you now! :)")
        connection.close()


while True:
    if is_nighttime():
        check_date = datetime.now().strftime('%Y-%m-%d')
        check_time = datetime.now().strftime('%H:%M:%S')
        print(f"Checked {check_date} at {check_time} {check_iss()}, night: {is_nighttime()}")
        if MY_COOR_MIN < check_iss() < MY_COOR_MAX and is_nighttime():
            send_email()
            print("Email sent!")
    time.sleep(300)

