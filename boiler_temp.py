import re
import requests
from influxdb import InfluxDBClient
from time import localtime, strftime

#prod
esp_url = 'esp_url'


def log(string):
    dt = strftime("[%d-%m-%Y %H:%M:%S] ", localtime())
    with open("/var/log/esp_power.log", "a") as myfile:
        myfile.write(dt + string + "\r\n")
    pass

def get_data():
    print("Check response...")
    try:
        response = requests.get(esp_url, timeout=(15, 15))
        response.raise_for_status()

    except requests.exceptions.ReadTimeout:
        print('Oops. Read timeout occured')

    except requests.exceptions.ConnectTimeout:
        print('Oops. Connection timeout occured!')

    except requests.exceptions.ConnectionError:
        print('Seems like dns lookup failed..')

    except requests.exceptions.HTTPError as err:
        print('Oops. HTTP Error occured')
        print('Response is: {content}'.format(content=err.response.content))

    print("Response status code: " + str(response.status_code))

    text = response.text

    temp = re.search('(temp:)(\d+\.?\d+?)(C)', text)

    temp = float(temp.group(2))
    
    print(temp)

    json_body = [
        {
            "measurement": "boiler_temp",
            "tags": {
                "host": "home",
                "region": "ua"
            },
            "fields": {
                "temp": temp
            }
        }
    ]

    client = InfluxDBClient('host', port, 'user', 'pass', 'db')


    print("Write points: {0}".format(json_body))
    client.write_points(json_body)




    pass


get_data()





