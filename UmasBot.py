# -*- coding: utf-8 -*-
t = '******************************************'
x = '## (C) Vilius Erslovas, Rokiškis - 2022 ##'

import time
import iplib
import urllib.request as urlR
import http.client as httplib
import threading
import re

UDPXY = 'udpxy'
SERVE = 'server'
MSDLT = 'msd_lite'
ASTRA = 'astra relay'
NOSRV = 'no_serve'
PNAME = 'settings'

SLEEP = 1  # ZADERZKA текста на экране
PAUSE = 2  # Пауза перед стартом следующего робота
MAXATT = 2  # Кол-во попыток подключения
TIMEOUT = 3  # Ожидание видеопотока
LENDATA = 1364  # Размер блока данных
BOTNAME = 'UmasBot'
VERSION = '1.0.0'
LISTSERV = 'listerver.txt'
PATHNAME = PNAME, PNAME
timeout = 0.25
mcast = "234.0.0.200:2000"


def ipToNum(ip):
    data = ip.split('.')
    return int(data[0]) * 256 ** 3 + int(data[1]) * 256 ** 2 + int(data[2]) * 256 ** 1 + int(data[3]) * 256 ** 0


def numToIP(num):
    "Convert 32-bit integer to dotted IPv4 address."
    return ".".join(map(lambda n: str(num >> n & 0xFF), [24, 16, 8, 0]))


class UmasBot():
    tvList = []
    def __init__(self):
        print("%s\n%s\n%s\n" % (t, x, t))
        print("Sveiki, aš '%s-%s'" % (BOTNAME, VERSION))
        time.sleep(SLEEP)

    def aclient(self, udphostport):
        attempt = 0
        activeclient = -1
        html = "?"
        patt = "<td>.+</td>"
        while attempt < MAXATT:
            try:
                html = urlR.urlopen('http://%s/status' % udphostport, timeout=timeout).read()
                html = html.decode("utf-8")
                x = re.findall(patt, html)[3]
                x = x.split("<td>")[1].split("</td>")[0]
                # print(x, activeclient)
                activeclient = int(x)
                if activeclient >= 0:
                    return activeclient
                else:
                    attempt += 1
                    time.sleep(0.1)
            except:
                attempt += 1
                time.sleep(0.1)
        return activeclient

    def verify(self, udphostport, mcast):
        if mcast != '':
            attempt = 0
            verif = False
            while attempt < MAXATT:
                try:
                    stream = httplib.HTTPConnection(udphostport, timeout=TIMEOUT)
                    stream.request("GET", "/udp/%s" % mcast)
                    sresponse = stream.getresponse()
                    data = sresponse.read(LENDATA)
                    if len(data) == LENDATA:
                        verif = True
                        break
                    else:
                        attempt += 1
                        time.sleep(SLEEP)
                except:
                    attempt += 1
                    time.sleep(SLEEP)
        else:
            verif = True
        return verif



    def run(self):
        # '185.134.36.0 - 185.134.39.255'
        # timeout = 1
        start_host = '185.134.36.0'
        end_host = '185.134.39.255'
        startIP = iplib.IPv4Address(start_host)
        # endIP = iplib.IPv4Address(start_host)
        count = ipToNum(end_host) - ipToNum(start_host)
        # print(count)
        ports = [4022]
        # print (len(ports))
        scantimeM = count * len(ports) * timeout / 60
        scantimeH = count * len(ports) * timeout / 3600
        print('Skenuojamas diapazonas %s - %s /skenavimo trukmė ~ %s val (%s min)/' % (
            start_host, end_host, round(scantimeH, 2), round(scantimeM, 2)))
        pers = 10
        total = 0
        for i in range(count):
            host = str(startIP + i)
            done = i * 100 / count
            if done > 0 and done % pers == 0 and total < done:
                print('Nuskenuota %s proc. diapazono %s - %s' % (int(done), start_host, end_host))
                total = done
            for port in ports:
                udphostport = '%s:%s' % (host, port)
                isUdpxy = self.isudpxy(udphostport)
                if isUdpxy:
                    klientSk = self.aclient(udphostport)
                    if klientSk > 0:
                        geras = [host, port, klientSk]
                        print(geras)
                        self.tvList.append(geras)
                    elif klientSk == 0:
                        if self.verify(udphostport, mcast):
                            geras = [host, port, klientSk]
                            print(geras)
                            self.tvList.append(geras)

    def isudpxy(self, udphostport):
        try:
            stream = httplib.HTTPConnection(udphostport, timeout=timeout)
            stream.request("GET", "/stat")
            sresponse = stream.getresponse()
            hdr = sresponse.getheaders()[0]
            return str(hdr).find("Serve") > 0 and str(hdr).find("udpxy") > 0
        except:
            return False

    def getTvList(self):
        print(self.tvList)


 # def run(self):
    # print 'I start searching for an IPTV provider.\n"
    # while True:
    # 	for hsts in self.HOSTS:
    # 		hst= hsts.strip('\n\t\r')
    # 		COUNT_HOST = self.countip(hst)
    # 		HOST = hst.split('/')[0]
    # 		scan = ScanPORTS(self.UDPXY, self.MSDLT, self.ASTRA, HOST, self.PORTS,
    # 		COUNT_HOST, self.MCAST, self.TIOUT, self.TIMER)
    # 		scan.start()
    # 		time.sleep(PAUSE)
    # 	time.sleep(self.TIMER * 60)

    # class ScanPORTS (threading.Thread):
    # 	def __init__(self, udpxy, msdlt, astra, host, ports, count, mcast, timeout, timer):
    # 		threading.Thread.__init__(self)
    # 		self.daemon = True
    # 		self.udpxy = udpxy == 1
    # 		self.msdlt = msdlt == 1
    # 		self.antra = astra == 1
    # 		self.host = host
    # 		self.ports = ports
    # 		self.count = count
    # 		self.mcast = mcast
    # 		self.timeout = timeout
    # 		self.timer = timer

a = time.time()
b = UmasBot()
b.run()
b.getTvList()
# print(a)
# print(time.time())
print("%s s" % (round(time.time() - a, 2)))
# myIp="172.5.22.111"
# print (myIp)
# myNum=ipToNum(myIp)
# print (myNum)
# print(numToIP(myNum))
# UB=UmasBot()
# print(UB.aclient("178.163.2.1:4022"))
# print(UB.verify("178.163.2.1:4022", mcast))
# print(UB.aclient("185.134.38.66:4022"))
# print(UB.verify("185.134.38.66:4022", mcast))

# start="172.5.22.111"
# end="172.8.15.209"
# count=ipToNum(end)-ipToNum(start)
# ip = iplib.IPv4Address(start)
#
# print (ip)
# print (ip + count)

# stream = httplib.HTTPConnection('178.163.0.139:4022', timeout=0.25)
# stream.request("GET", "/stat")
# sresponse = stream.getresponse()
# aa=sresponse.getheaders()[0]
# print(str(aa).find("Serve") > 0 and str(aa).find("udpxy")>0)
# print(len(sresponse.getheaders()))
