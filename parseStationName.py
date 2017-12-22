# -*- coding: utf-8 -*-

import re
import requests

URL = "https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.9035"
resp = requests.get(URL)
stations = re.findall(r'[\u4e00-\u9fa5]+\|[A-Z]+', resp.text)
stationsInfo = {}
for station in stations:
    key = station.split('|', 1)[0]
    value = station.split('|', 1)[1]
    stationsInfo[key] = value
    