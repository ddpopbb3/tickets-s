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
from colorama import init, Fore

init()


def cli():
    arguments = docopt(__doc__)
    print(arguments)
    from_station = stationsInfo.get(arguments['<from>'])
    to_station = stationsInfo.get(arguments['<to>'])
    date = arguments['<date>']
    url = 'https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date={}&leftTicketDTO.from_station={}&leftTicketDTO.to_station={}&purpose_codes=ADULT'.format(
        date, from_station, to_station)
    resp = requests.get(url)
    # resp = requests.get(url, verify=False) #这里不懂教程里为什么不验证合法性

    #把数据写到stationData.json里
    # 这里是为了分析数据格式，因为12306的数据格式经常变
    # with open('stationData.json', 'w') as f:
    #     json.dump(resp, f, ensure_ascii=False)

    #假数据用于测试
    # filename = 'stationData.json'
    # with open(filename, encoding='utf-8') as f:
    #     pop_data = json.load(f)
    # resp = pop_data

    #翻转键值
    stationsDict = dict((v, k) for k, v in stationsInfo.items())

    data = Station(dict(resp.json())['data']['result'])
    data.print(stationsDict)  # 为了正确显示，将翻转后的车次的字典传进去


class Station(object):
    def __init__(self, stationDataInfos):
        self.__stationDataInfos = stationDataInfos

    def parse(self, stationDataInfo):
        coms = stationDataInfo.split('|')
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

    def get_stationDataInfos(self):
        return self.__stationDataInfos

    def print(self, stationsDict):
        headers = '车次 车站 时间 历时 商务 一等 二等 软卧 硬卧 软座 硬座 无座'.split()
        pt = PrettyTable()
        pt._set_field_names(headers)
        for row in self.__stationDataInfos:
            s = self.parse(row)
            pt.add_row([
                s['train'], '\n'.join([
                    Fore.GREEN + stationsDict.get(s['s1']) + Fore.RESET,
                    Fore.RED + stationsDict.get(s['s4']) + Fore.RESET
                ]), '\n'.join([
                    Fore.GREEN + s['start_time'] + Fore.RESET,
                    Fore.RED + s['arrive_time'] + Fore.RESET
                ]), s['spent_time'], s['business_class'], s['one_class'],
                s['two_class'], s['soft_bed'], s['hard_bed'], s['soft_seat'],
                s['hard_seat'], s['no_seat']
            ])
        print(pt)


if __name__ == "__main__":
    cli()
