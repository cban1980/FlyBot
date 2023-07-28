#!/bin/env python
# -*- coding: utf-8 -*-
# Separate file for IRC functions that gets called in main.py.

from googletrans import Translator
from bs4 import BeautifulSoup as bs
import requests
import re 
import pyshorteners

def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    cleantext = cleantext.replace("&lt;", "<")
    cleantext = cleantext.replace("&gt;", ">")
    cleantext = cleantext.replace("&amp;", "&")
    " ".join(map(str, cleantext))
    return cleantext


def tr(fran, till, mening):
    """Translation function."""
    translator = Translator()
    translation = translator.translate(mening, src=fran, dest=till)
    return translation.text
def lk():
    "En lyckokaka."
    html = requests.get('http://www.fortunecookiemessage.com/').text
    soup = bs(html, 'html5lib')
    svar = soup.findAll("div", class_ = "quote")
    svar = cleanhtml(str(svar))
    translator = Translator()
    translation = translator.translate(svar, src="en", dest="sv")
    return translation.text.strip("[]")
def vader(city: str):
    # Fetch weather data from OpenWeatherMap
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city},se&units=metric&lang=sv&appid=71ca5f7c7040a2573a610541a5ea76af"
    url_forecast = f"http://api.openweathermap.org/data/2.5/forecast?q={city},se&units=metric&lang=sv&appid=71ca5f7c7040a2573a610541a5ea76af"

    response = requests.get(url)
    response_forecast = requests.get(url_forecast)

    if response.status_code == 200 and response_forecast.status_code == 200:
        data = response.json()
        temperature = data["main"]["temp"]
        pressure = data["main"]["pressure"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]
        wind_direction = data["wind"]["deg"]
        clouds = data["clouds"]["all"]
        weather = data["weather"][0]["description"]

        data_forecast = response_forecast.json()
        tomorrow_weather = data_forecast["list"][0]["weather"][0]["description"]

        return (f"Nuvarande väder i {city}: Temperatur: {temperature} grader Celsius, Lufttryck: {pressure} hPa, Luftfuktighet: {humidity}%, Vindhastighet: {wind_speed} m/s, Vindriktning: {wind_direction} grader, Molnighet: {clouds}%, Väderbeskrivning: {weather}. Imorgon: {tomorrow_weather}")
def tinyurl(arg):
    arg = str(arg)
    long_url = arg
    type_tiny = pyshorteners.Shortener()
    short_url = type_tiny.tinyurl.short(long_url)
    return short_url