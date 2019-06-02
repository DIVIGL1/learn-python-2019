# -*- coding: utf-8 -*-
import requests

API_URL = "http://api.worldweatheronline.com/premium/v1/weather.ashx"
MY_CITY = "Nizhny Novgorod, Russia"

def weather_in_the_city(city_name):
    params = {
        "key": "c9dc532058eb43ffb80175050190206",
        "q": city_name,
        "format": "json",
        "num_of_days": 1,
        "lang": "ru"
    }
    result = requests.get(API_URL,params=params)
    weather = result.json()
    if "data" in weather:
        if "current_condition" in weather["data"]:
            try:
                return(weather["data"]["current_condition"][0])
            except (IndexError, TypeError):
                return(False)
    return(False)

if __name__ == "__main__":
    print(weather_in_the_city(MY_CITY))