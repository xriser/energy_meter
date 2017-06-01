import re
import json
from influxdb import InfluxDBClient

protocol = 'json'

client = InfluxDBClient('host', 8086, 'user', 'pass', 'db')

rs = client.query("SELECT * FROM energy_meter WHERE time > '2017-04-01' AND time < '2017-06-02'")
points = list(rs.get_points())

for item in points:
    item = str(item)
    #print(item)
    time = re.search("(time\':\s\')(.*Z)", item)
    time = time.group(2)
    h = re.search("(.*T)(\d+)(:)", time)
    h = int(h.group(2))
    v = re.search("(voltage\':\s)(\d+(\.\d+)?)", item)
    c = re.search("(current\':\s)(\d+(\.\d+)?)", item)
    p = re.search("(power\':\s)(\d+(\.\d+)?)", item)
    e = re.search("(energy\':\s)(\d+(\.\d+)?)", item)


    v = float(v.group(2))
    c = float(c.group(2))
    p = float(p.group(2))
    e = float(e.group(2))

    json_body = [
        {
            "measurement": "energy_meter",
            "tags": {
                "host": "home",
                "region": "ua"
            },
            "time": time,
            "fields": {
                "voltage": v,
                "current": c,
                "power": p,
                "energy": e,
                "night": 1
            }
        }
    ]

    if h >= 20 or h <= 4:
        print(json_body)
        client.write_points(json_body)
