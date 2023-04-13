# from UmasBot import TIMEOUT, MAXATT,LENDATA,SLEEP
import http.client as httplib
import threading

import gspread
import time
import threading

SLEEP = 1  # ZADERZKA текста на экране
PAUSE = 3  # Пауза перед стартом следующего робота
MAXATT = 1  # Кол-во попыток подключения
TIMEOUT = 3  # Ожидание видеопотока
LENDATA = 1364  # Размер блока данных

timeout = 0.1


def verify(udphostport, mcast):
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


def splitdiapazon(diapazoncount):
    startIP = 0
    endIP = 255
    count = endIP - startIP + 1
    # print(count)

    porc = int(count / diapazoncount)
    likut = count % porc
    # print(porc)
    # print(likut)
    counts = [porc] * (diapazoncount - 1)
    counts.append(porc + likut)
    # print(counts)
    diapazons = []
    IP1 = startIP

    for c in counts:
        IP2 = IP1 + c
        IP1 = IP2 - c
        diapazons.append([IP1, IP2])
        # print( '%s-%s' % (numToIP(IP1),numToIP(IP2)))
        IP1 = IP2
    # print(diapazons)
    return diapazons


spreadKey = '1oQwjv5YwyNytc2jtzlpmShOxOHTRS04uUi8-dNiwZJ4'
# spreadKey='1__W0BD2Oydd2K9pzM60h7qvI8t-RzPQA3ctBqADPRpw'
# sheetName = 'Pacient'
sheetName = 'kanal'
# sheetName='mcast'
scopes = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

gs = gspread.service_account(filename='creds.json', scopes=scopes)
sh = gs.open_by_key(spreadKey)
wsh = sh.worksheet(sheetName)

hostport = '5.129.76.19:81'
d = splitdiapazon(4)
# print(d)
table = []


class ScanPORTS(threading.Thread):

    def __init__(self, start_host, end_host):
        threading.Thread.__init__(self)
        self.daemon = True
        # self.target=self.run
        self.start_host = start_host
        self.end_host = end_host
        # self.mcast = mcast
        # self.run()

    def run(self):
        print("%s - pradedu darbą (%s - %s)" % (self.name, self.start_host, self.end_host))
        start = time.time()
        try:
            for host in range(self.start_host, self.end_host):
                mcast = '239.1.4.%s:1234' % (host)
                # print(mcast)
                ok = verify(hostport, mcast)
                print([self.name, mcast, ok])
                if ok:
                    table.append([self.name, host, mcast, ok])
                # time.sleep(0.1)
        except:
            pass
        # time.sleep(300)
        print("%s - baigiau darbą per %s s " % (self.name, round(time.time() - start)))


if __name__ == "__main__":
    st = time.time()
    scans = []
    for k in d:
        # mcast = '234.0.0.%s:1234' % (k)
        # ok = verify(udphostport=hostport, mcast=mcast)
        ip1 = k[0]
        ip2 = k[1]
        scan = ScanPORTS(ip1, ip2)
        scan.start()
        scans.append(scan)

        # print((numToIP(ip1),numToIP(ip2),ports))
        time.sleep(PAUSE)
    for t in scans:
        t.join()

    # scan.join(
    print(len(table))

    wsh.update('K1', table)
    print("Uztrukau %s s" % (round(time.time() - st)))
