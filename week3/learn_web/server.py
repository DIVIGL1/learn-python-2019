# -*- coding: utf-8 -*-
from flask import Flask, render_template

from python_org_news import get_python_news
import weather


app = Flask(__name__)

@app.route("/")
def index():
    local_page_title = "Новости Python"
    weather_info = weather.weather_in_the_city(weather.MY_CITY)
    news_list = get_python_news()
    return( render_template("index.html", page_title=local_page_title, weather=weather_info, news_list=news_list) )

if __name__ == "__main__":
#    app.config["DEBUG"] = True
    app.run()

    