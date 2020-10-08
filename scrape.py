#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
import datetime
import webbrowser
import re

quote_url = "https://www.brainyquote.com/quote_of_the_day"
weather_url = "https://forecast.weather.gov/MapClick.php?lat=42.3761&lon=-71.1185"
news_url = "https://www.bbc.com/news/world"
stocks_url = "https://money.cnn.com/data/us_markets/"

with open("template.html") as f:
    template = BeautifulSoup(f, "html.parser")

quote = BeautifulSoup(requests.get(quote_url).content, "html.parser")
weather = BeautifulSoup(requests.get(weather_url).content, "html.parser")
news = BeautifulSoup(requests.get(news_url).content, "html.parser")
stocks = BeautifulSoup(requests.get(stocks_url).content, "html.parser")

with open("name") as f:
    name = f.read().rstrip()

hour = datetime.datetime.now().hour

time_of_day = (
    "morning" if 5 <= hour <= 11
    else
    "afternoon" if 12 <= hour <= 17
    else
    "evening" if 18 <= hour <= 22
    else
    "night")

for greeting in template.find_all(template="greeting"):
    greeting.string = "Good " + time_of_day + ", "  + name + "!"

template.find(template="quote").string = quote.find("img", class_="p-qotd")["alt"]

conditions_container = template.find(template="conditions")
conditions = weather.find(id="current_conditions-summary")
conditions_container.string = conditions.find(class_="myforecast-current-lrg").get_text()
conditions_break_tag = template.new_tag("br")
conditions_container.append(conditions_break_tag)
conditions_container.append(conditions.find(class_="myforecast-current").get_text())
template.find(template="forecast").string = weather.find(id="detailed-forecast-body").find(class_="forecast-text").get_text()

headlines_container = template.find(template="headlines")
headlines = news.find(id="featured-contents").parent.find_all("a", class_="gs-c-promo-heading")
for headline in headlines[:5]:
    headline_tag = template.new_tag("a", href="https://www.bbc.com" + headline["href"], target="_blank")
    headline_tag["class"] = "w3-button w3-hover-none w3-hover-text-green"
    headline_tag.string = headline.find(class_="gs-c-promo-heading__title").get_text()
    break_tag = template.new_tag("br")
    headlines_container.append(headline_tag)
    headlines_container.append(break_tag)

stocks_container = template.find(template="stocks")
stocks_list = stocks.find(id="wsod_tickerRoll").find_all("li")
for stock in stocks_list:
    stocks_container.append(stock.find(class_="wsod_symbol").get_text())
    stocks_container.append(": ")
    stocks_container.append(stock.find(class_="quotePctChange").get_text())
    break_tag = template.new_tag("br")
    stocks_container.append(break_tag)

with open("out.html", mode="w") as f:
    f.write(str(template))

webbrowser.open("out.html")
