import requests
import pandas as pd
import datetime
import operator
import datetime
import time
import os

API_KEY = os.environ["WUNDERGROUND_APIKEY"]

def get_current(station):
    time.sleep(1)
    res = requests.get("http://api.wunderground.com/api/{}/conditions/astronomy/q/pws:{}.json".format(API_KEY, station['key']))
    data = res.json()

    #return data
    dt = datetime.datetime.fromtimestamp(int(data['current_observation']['local_epoch']))

    sunrise = dt.replace(hour=int(data['sun_phase']['sunrise']['hour']),
                         minute=int(data['sun_phase']['sunrise']['minute']), second=0)

    sunset = dt.replace(hour=int(data['sun_phase']['sunset']['hour']),
                         minute=int(data['sun_phase']['sunset']['minute']), second=0)

    return pd.DataFrame([{'timestamp': dt.strftime('%Y-%m-%d %H:%M:%S'),
             'pressure': float(data['current_observation']['pressure_in']),
             'degree': float(data['current_observation']['wind_degrees']),
             'speed': float(data['current_observation']['wind_mph']),
             'direction': data['current_observation']['wind_dir'],
             'gust': float(data['current_observation']['wind_gust_mph']),
             'sky': data['current_observation']['weather'],
             'humidity': float(data['current_observation']['relative_humidity'].replace("%","")),
             'dewpoint': data['current_observation']['dewpoint_f'],
             'temperature': float(data['current_observation']['temp_f']),
             'feelslike': float(data['current_observation']['feelslike_f']),
             'source': 'api.wunderground',
             'location': station['key'],
             'sunrise': sunrise.strftime('%Y-%m-%d %H:%M:%S'),
             'sunset': sunset.strftime('%Y-%m-%d %H:%M:%S'),
            }])

def get_forecast(station):
    time.sleep(1)
    res = requests.get("http://api.wunderground.com/api/{}/hourly/q/pws:{}.json".format(API_KEY, station['key']))
    history = res.json()

    rows = []
    for hour in history['hourly_forecast']:
        rows.append({ 'timestamp': datetime.datetime.fromtimestamp(int(hour['FCTTIME']['epoch'])).strftime('%Y-%m-%d %H:%M:%S'),
                      'direction': hour['wdir']['dir'],
                      'degree': float(hour['wdir']['degrees']),
                      'speed': float(hour['wspd']['english']),
                      'temperature': float(hour['temp']['english']),
                      'sky': hour['condition'],
                      'pressure': float(hour['mslp']['english']),
                      'humidity': hour['humidity'],
                      'source': 'api.wunderground',
                      'dewpoint': float(hour['dewpoint']['english']),
                      'feelslike': float(hour['feelslike']['english']),
                    })

    tmp = pd.DataFrame(rows)
    print(station, tmp.shape)
    try:
        tmp['current'] = tmp['timestamp'].min()
        tmp['name'] = station['name']
        tmp['location'] = station['key']
        return tmp
    except KeyError:
        print("station {} failed".format(station['key']))


if __name__ == "__main__":

    station = {'key': "KCOBOULD45", "name": "boulder"}
    print(get_current(station))

