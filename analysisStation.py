# -*- coding: utf-8 -*-
"""

Usage:
    analysisStation.py [-gd] <from> <to> <date>

Options:
    -h,--help       显示帮助菜单
    -g              高铁
    -d              动车

Example:

    analysisStation 南京 北京 2016-10-14
    analysisStation -g 南京 北京 2016-10-14

"""
from parseStationName import stationsInfo
from docopt import docopt
import requests
from prettytable import PrettyTable
import json


def cli():
    arguments = docopt(__doc__)
    print(arguments)
    from_station = stationsInfo.get(arguments['<from>'])
    to_station = stationsInfo.get(arguments['<to>'])
    date = arguments['<date>']
    url = 'https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date={}&leftTicketDTO.from_station={}&leftTicketDTO.to_station={}&purpose_codes=ADULT'.format(
        date, from_station, to_station)
    resp = requests.get(url, verify=False)
    headers = '车次 出发站 终点站 发车时间 结束时间 历时 商务 一等 二等 软卧 硬卧 软座 硬座 无座'.split()
    pt = PrettyTable()
    pt._set_field_names(headers)

    #假数据用于测试
    # filename = 'stationData.json'
    # with open(filename, encoding='utf-8') as f:
    #     pop_data = json.load(f)
    # resp = pop_data

    resp = dict(resp.json())
    rows = resp['data']['result']

    for row in rows:
        print(row)
        s = parse(row)
        pt.add_row([
            s['train'], resp['data']['map'].get(
                s['s1']), resp['data']['map'].get(s['s4']), s['start_time'],
            s['arrive_time'], s['spent_time'], s['business_class'],
            s['one_class'], s['two_class'], s['soft_bed'], s['hard_bed'],
            s['soft_seat'], s['hard_seat'], s['no_seat']
        ])
    print(pt)


def parse(str):
    coms = str.split('|')
    # i = 0
    # while i < len(coms):
    #     print(i, "   ", coms[i])
    #     i = i + 1
    stationDataInfo = {}
    stationDataInfo['train'] = coms[3]
    stationDataInfo['s1'] = coms[4]
    stationDataInfo['s2'] = coms[5]
    stationDataInfo['s3'] = coms[6]
    stationDataInfo['s4'] = coms[7]
    stationDataInfo['start_time'] = coms[8]
    stationDataInfo['arrive_time'] = coms[9]
    stationDataInfo['spent_time'] = coms[10]
    stationDataInfo['motor_bed'] = coms[33]  #动卧
    stationDataInfo['business_class'] = coms[32]  #商务座
    stationDataInfo['one_class'] = coms[31]  #一等
    stationDataInfo['two_class'] = coms[30]  #二等
    stationDataInfo['no_seat'] = coms[29]  #无
    stationDataInfo['hard_bed'] = coms[28]  #硬座
    stationDataInfo['soft_seat'] = coms[27]  #软座
    stationDataInfo['hard_seat'] = coms[26]  #硬卧
    stationDataInfo['soft_seat2'] = coms[25]
    stationDataInfo['hard_seat2'] = coms[24]
    stationDataInfo['soft_bed'] = coms[23]  #软卧
    stationDataInfo['high_soft_bed'] = coms[22]  #高级软卧
    stationDataInfo['other'] = coms[21]
    return stationDataInfo


if __name__ == "__main__":
    cli()
