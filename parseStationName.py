# -*- coding: utf-8 -*-

import re
import requests

url = "https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.9035"
response = requests.get(url)
stations = re.findall(r'[\u4e00-\u9fa5]+\|[A-Z]+',response.text)
stationsInfo = {}
for station in stations:
    key = station.split('|',1)[0]
    value = station.split('|',1)[1]
    stationsInfo[key]=value