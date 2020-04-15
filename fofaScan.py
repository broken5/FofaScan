import requests
import config
import os
import math
import csv
import time
import fire
from base64 import b64encode
from lib.genIp import genIp


class FofaScan:
    def __init__(self, target):
        self.target = target
        self.ip_list = []

    def fofa_go(self, in_query_ip):
        url = 'https://fofa.so/api/v1/search/all'
        keyword = ''
        for ip in in_query_ip:
            keyword += 'ip="%s" || ' % ip
        keyword = keyword.strip(' || ')
        params = {
            'email': config.fofa_email,
            'key': config.fofa_key,
            'qbase64': b64encode(keyword.encode()),
            'fields': 'ip,host,title,port,protocol',
            'size': 10000
        }
        r = requests.get(url, params=params)
        return r.json().get('results')

    def get_ip_list(self, ip):
        gen = genIp()
        if os.path.isfile(ip):
            lines = open(ip).readlines()
            for line in lines:
                self.ip_list += gen.run(line.strip())
        else:
            self.ip_list += gen.run(ip)

    def run(self):
        filename = 'out_%s.csv' % str(int(time.time()))
        f = open('out/'+filename, 'a', newline='')
        f_csv = csv.writer(f)
        f_csv.writerow(['ip', 'host', 'title', 'port', 'protocol'])
        self.get_ip_list(self.target)
        total = math.ceil(len(self.ip_list) / 50)
        for i in range(total):
            in_query_ip = self.ip_list[i*50:i*50+50]
            results = self.fofa_go(in_query_ip)
            for info in results:
                if info[4]:
                    print(info)
                    f_csv.writerow(info)


def run(target):
    fofaScan = FofaScan(target)
    fofaScan.run()


if __name__ == '__main__':
    fire.Fire(run)
