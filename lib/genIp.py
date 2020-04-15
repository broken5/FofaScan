import re
import IPy
import os


class genIp(object):
    def __init__(self):
        self.result_info = []

    def isIP(self, ip):
        p = re.compile('^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$')
        if p.match(ip):
            return True
        else:
            return False

    def ip2num(self, ip):
        ips = [int(x) for x in ip.split('.')]
        return ips[0] << 24 | ips[1] << 16 | ips[2] << 8 | ips[3]

    def num2ip(self, num):
        return '%s.%s.%s.%s' % ((num >> 24) & 0xff, (num >> 16) & 0xff, (num >> 8) & 0xff, (num & 0xff))

    def dec255_to_bin8(self, dec_str):
        bin_str = bin(int(dec_str, 10)).replace("0b", '')
        headers = ['', '0', '00', '000', '0000', '00000', '000000', '0000000']
        if len(bin_str) < 8:
            bin_str = headers[8 - len(bin_str)] + bin_str
        return bin_str

    def ipstr_to_binstr(self, ip):
        a, b, c, d = ip.split(".")
        ipbin = self.dec255_to_bin8(a) + self.dec255_to_bin8(b) + self.dec255_to_bin8(c) + self.dec255_to_bin8(d)
        return ipbin

    def genip_by_ipy(self, net):
        ips = IPy.IP(net)
        return [ip.strNormal() for ip in ips][1:-1]

    def genip_by_range(self, ip_range):
        ips = []
        ips_1, ips_2, ips_3, ips_4 = ip_range
        for ip_1 in range(int(ips_1[0]), int(ips_1[-1])+1):
            for ip_2 in range(int(ips_2[0]), int(ips_2[-1]) + 1):
                for ip_3 in range(int(ips_3[0]), int(ips_3[-1]) + 1):
                    for ip_4 in range(int(ips_4[0]), int(ips_4[-1]) + 1):
                        ips.append(str(ip_1)+'.'+str(ip_2)+'.'+str(ip_3)+'.'+str(ip_4))
        return ips

    def binstr_to_ipstr(self, binstr):
        return str(int(binstr[0:8], base=2)) + "." + str(int(binstr[8:16], base=2)) + "." + str(
            int(binstr[16:24], base=2)) + "." + str(int(binstr[24:32], base=2))

    def FormtIP(self, ips):
        if ips.find('/') > 0:
            ip, mask = ips.split("/")
            ipbin = self.ipstr_to_binstr(ip)
            ipnet_bin = ipbin[0:int(mask)] + ipbin[int(mask):32].replace("1", "0")
            ipstart_bin = bin(int(ipnet_bin, base=2)).replace("0b", '')
            while len(ipstart_bin) < 32:
                ipstart_bin = '0' + ipstart_bin
            ipend_bin = bin(int(ipnet_bin, base=2) + pow(2, 32 - int(mask)) - 2).replace("0b", '')
            while len(ipend_bin) < 32:
                ipend_bin = '0' + ipend_bin
            ipnet = self.binstr_to_ipstr(ipstart_bin) + '/' + ips.split('/')[1]
            return self.genip_by_ipy(ipnet)
        # 把单独的IP直接返回
        elif self.isIP(ips):
            return [ips]
        elif ips.find('-') > 0:
            ip_range = []
            temp = ips.split('.')
            for i in temp:
                num_range = i.split('-')
                if len(num_range) < 2:
                    num_range.append(i)
                ip_range.append(num_range)
            return self.genip_by_range(ip_range)

    def run(self, ips):
        try:
            self.result_info = self.FormtIP(ips)
        except Exception as e:
            pass
        return self.result_info


if __name__ == '__main__':
    ip_list = genIp().run('101.226.212.191')
    print(ip_list)