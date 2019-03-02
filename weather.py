# -*- coding: utf-8 -*-

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








# Uncomment the following for debugging

# def main():
#     weather = WeatherGod()
#     print(weather.generateWeatherReport("Hervanta"))
#
#
#
# main()
