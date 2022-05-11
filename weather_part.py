#!/usr/bin/python
import logging
import json
import sys
if (sys.version_info > (3,0)):
    import urllib.request
else:
    import urllib
import requests # conda install requests or pip install requests
from settings import LAT, LON, APIKEY, LANG, UNIT


logger = logging.getLogger('app')

# Global variables.
forecast_url = None


def get_forecast_URL_from_lat_long(latitude: int, longitude: int, apikey: str, lang: str, unit: str):
    """
    Make a request to api.weather.gov specifying latitude and longitude.
    The response should give us, among other things, the URL for the local weather forecast.
    """
    # Param check.
    if (latitude is None) or (longitude is None):
        logger.warning('weather_module.get_forecast_URL_from_lat_long(); missing latitude or longitude.')
        return None

    logger.info('weather_module.get_forecast_URL_from_lat_long(); trying...')
    api_url_base = 'https://devapi.qweather.com/v7/weather/now?'
    current_obs_url = '{0}location={1},{2}&key={3}&lang={4}&unit={5}'.format(api_url_base, longitude, latitude, apikey, lang, unit)
    response = requests.get(current_obs_url)
    if response.status_code == 200:
        forecast_data = json.loads(response.content.decode('utf-8'))
        weather = forecast_data['now']['text']
        feelsLike = forecast_data['now']['feelsLike']
        temp = forecast_data['now']['temp']
        windDir = forecast_data['now']['windDir']
        windSpeed = forecast_data['now']['windSpeed']
        humidity = forecast_data['now']['humidity']
        vis = forecast_data['now']['vis']
        cloud = forecast_data['now']['cloud']
        forecast_data = '当前天气：{6}，温度 {0}℃，体感温度 {1}℃，云量 {5}%\n风向 {2}，风速 {3}公里/小时，能见度 {4}公里\n'.format(temp, feelsLike, windDir, windSpeed, vis, cloud, weather)
        #空气质量
        air_api_base = 'https://devapi.qweather.com/v7/air/now?'
        air_obs_url = '{0}location={1},{2}&key={3}&lang={4}&unit={5}'.format(air_api_base, longitude, latitude, apikey, lang, unit)
        response = requests.get(air_obs_url)
        if response.status_code == 200:
            air_data = json.loads(response.content.decode('utf-8'))
            air_aqi = air_data['now']['aqi']
            air_category = air_data['now']['category']
            air_data = '当前空气质量：{0}，AQI指数：{1}\n'.format(air_category, air_aqi)
            #生活指数
            life_index_base = 'https://devapi.qweather.com/v7/indices/1d?type=1,3,5,8,9,14&'
            life_obs_url = '{0}location={1},{2}&key={3}&lang={4}&unit={5}'.format(life_index_base, longitude, latitude, apikey, lang, unit)
            response = requests.get(life_obs_url)
            if response.status_code == 200:
                life_data = json.loads(response.content.decode('utf-8'))
                life_index = '\b'
                for i in life_data['daily']:
                    life_name = i['name']
                    life_category = i['category']
                    life_index = '{0}{1}：{2}\n'.format(life_index, life_name, life_category)
        forecast_data = '{0}{1}{2}'.format(forecast_data, air_data, life_index)
        if forecast_data:
            logger.info('weather_module.get_forecast_URL_from_lat_long(); returning forecast data.')
            return forecast_data
        else:
            logger.warning('weather_module.get_forecast_URL_from_lat_long(); no data to return.')
            return None
    else:
        logger.warning('[?] Unexpected Error: [HTTP {0}]: Content: {1}'.format(response.status_code, response.content))
        return None


def get_weather_forecast():
    """
    Calls above functions to get a list of 'period' weather forecast data from api.weather.gov.
    LATITUDE and LONGITUDE are expected to be present in a settings.py file.
    """

    global forecast_url

    # Get the forecast URL from latitude and longitude.
    if forecast_url is None:
        #forecast_url = get_forecast_URL_from_lat_long(LATITUDE, LONGITUDE, APIKEY, LANG, UNIT)
        #forecast_url = get_forecast_URL_from_lat_long(LAT, LON, APIKEY, LANG, UNIT)
        #print(get_forecast_URL_from_lat_long(LAT, LON, APIKEY, LANG, UNIT))
        return get_forecast_URL_from_lat_long(LAT, LON, APIKEY, LANG, UNIT)
    
    # Get current forecast periods.
    #return get_weather_forecast_from_URL(forecast_url)
    

