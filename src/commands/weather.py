# -*- coding: utf-8 -*-
from telegram.ext import CallbackContext
from telegram import Update
from config import DARKSKYTOKEN
from geopy.geocoders import Nominatim
import requests


# Using free Dark Sky Api, see https://darksky.net/dev/
# Todo: Change Dark Sky to Ilmatieteen Laitos or/and Foreca
class WeatherGod:
    @staticmethod
    def __pullWeather(city):
        geolocator = Nominatim(user_agent='MobileBot')
        location = geolocator.geocode(city)
        rawWeatherData = requests.get('https://api.darksky.net/forecast/'
                                   f'{DARKSKYTOKEN}/{location.latitude},'
                                   f'{location.longitude}?units=si&lang=fi')

        return rawWeatherData.json()

    def generateWeatherReport(self, city):
        weatherDict = self.__pullWeather(city)
        message = f'Säätiedote {city}.' \
            f'\nTällä hetkellä lämpötila on ' \
            f'{weatherDict["currently"]["temperature"]} °C ' \
            f'ja sateen intensiivisyys on ' \
            f'{weatherDict["currently"]["precipIntensity"]} mm/h. ' \
            f'{weatherDict["hourly"]["summary"]} ' \
            f'\n\nTuleva viikko: {weatherDict["daily"]["summary"]}'
        return message

def weather(update: Update, context: CallbackContext):
    try:
        city = update.message.text[5:]
        weather = WeatherGod()
        context.bot.send_message(chat_id=update.message.chat_id,
                             text=weather.generateWeatherReport(city))
    except AttributeError:
        context.bot.send_message(chat_id=update.message.chat_id,
                             text="Komento vaatii parametrin >KAUPUNKI< \n"
                                  "Esim: /saa Hervanta ")
        return
