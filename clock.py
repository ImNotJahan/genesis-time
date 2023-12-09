import requests
import json
import datetime
from os import system
from time import sleep
from config import lat, lng, tzId

response = requests.get("https://api.sunrise-sunset.org/json?lat={}&lng={}&tzId={}".format(lat, lng, tzId))
data = json.loads(response.text)["results"]

start = data["astronomical_twilight_begin"]
end = data["astronomical_twilight_end"]

def time_to_decimal(time_data):
    if(type(time_data) is str):
        pm = time_data.split(' ')[1] == "PM"
        stamp = time_data.split(' ')[0].split(':')
        time = 0

        if(pm):
            time += 12 * 60 * 60

        time += int(stamp[0]) * 60 * 60
        time += int(stamp[1]) * 60
        time += int(stamp[2])

        return time
    
    if(type(time_data) is datetime.time):
        time = time_data.hour * 60 * 60
        time += time_data.minute * 60
        time += time_data.second

        return time
    
    return -1

start_decimal = time_to_decimal(start)
end_decimal = time_to_decimal(end)

day_length = end_decimal - start_decimal
night_length = 24 * 60 * 60 - day_length
last_time = ""

system("title genTime")

def day_time():
    current_time = datetime.datetime.now().time()
    current_time = time_to_decimal(current_time)
    current_time -= start_decimal
    day_progress = current_time / day_length

    hour = int(day_progress * 7)
    minute = int(day_progress * 86 * 7 % 86)
    second = int(day_progress * 86 * 7 * 79 % 79)

    # owr
    return str(f"{hour:2d}") + ":" + str(f"{minute:02d}") + ":" + str(f"{second:02d}" + 'O')

def night_time():
    current_time = datetime.datetime.now().time()
    next_day_p = current_time.hour < 12
    current_time = time_to_decimal(current_time)
    current_time -= end_decimal

    if(next_day_p):
        current_time += 24 * 60 * 60
    
    night_progress = current_time / night_length

    hour = int(night_progress * 13)
    minute = int(night_progress * 17 * 13 % 17)
    second = int(night_progress * 17 * 13 * 79 % 79)

    # hakhoshek
    return str(f"{hour:02d}") + ":" + str(f"{minute:02d}") + ":" + str(f"{second:02d}" + 'H')


while(True):
    time = 0
    
    if(time_to_decimal(datetime.datetime.now().time()) > end_decimal):
        time = night_time()
    else:
        time = day_time()
    
    if(last_time != time):
        print('\r' + time, end='', flush=True)
        last_time = time

    sleep(0.5)
