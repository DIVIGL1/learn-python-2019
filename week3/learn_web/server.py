# -*- coding: utf-8 -*-
from flask import Flask
import weather

app = Flask(__name__)

@app.route("/")
def index():
    weather_info = weather.weather_in_the_city(weather.MY_CITY)
    if weather_info:
        return( f"Погода: {weather_info['temp_C']}, ощущается как {weather_info['FeelsLikeC']}")
    else:
        return("Сервис погоды временно не доступен...")

if __name__ == "__main__":
#    app.config["DEBUG"] = True
    app.run()

    