# -*- coding: utf-8 -*-
t = '******************************************'
x = '## (C) Vilius Erslovas, Rokiškis - 2022 ##'

# Skriptas skenuoja IP portus, ir išsaugo į masyvą tuos, iš kurių transliuojama IP televizija


import time
import gspread
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

SLEEP = 1                                   # ZADERZKA текста на экране
PAUSE = 2                                 # Пауза перед стартом следующего робота
MAXATT = 2                                  # Кол-во попыток подключения
TIMEOUT = 3                                 # Ожидание видеопотока
LENDATA = 1364                              # Размер блока данных

timeout = 0.25
mcast = "239.1.21.34:1234"                  # mcastas, kuriam yra transliacija
start_host = '5.129.50.0'                   # skenuojamo diapazono pradžia
end_host = '5.129.76.255'                   # skenuojamo diapazono pabaiga
ports = [81]                                # skenuojami portai (masyvas)
threads_count = 100                         # srautų, kurie skenuos, skaičius
tvList = []
scans = []


def read_old_IP():
    credentials = {
        "type": "service_account",
        "project_id": "project-id-6662602496862781661",
        "private_key_id": "6a935059d7f4020688e58f31b11f29c38fb910e2",
        "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDIjqGT8UMxyPnx\n+26CKHZjasuOwXC+ypk7DH9hQR5VU9fX7ItNZXjBqqgCOQSVImDSvhv8mcmykk6Z\npnoUigaPjw2V3xV+9E1tqdiBseXXWSajcaicaejwieqyNYsnhKgIjsadXUgc/xrJ\ngrd0CeNxBL/b9gH43E9baNUeQdh/p3iisMLUYZnaBW8yCC5o2mZyPM6zgq4xTWMu\nG3Z1oxeYgIl/bFqa8t7WHIoMuG3bz7881st6JHaK3wstw54YDjgn/1iHRZIWZsr1\ngkZhUr5tX/UvSnO6BxLJow3RJUKsT9YYk2tOuCYtgUgR1AGGi9RVJqJXcJUYYbS8\nCfGVQrHRAgMBAAECggEAJcIorHQ/PNfEKuk16H5ar6PzF/jWU61MBQB42OQMJG9p\nEydfIJ6qifepsuVuNe+nf/W3yipf/WUrNCVSFZzY2F1L5vv9jY3MKAnSj7Rg+9a2\nfg4Pewc7ilHE5HFNNg71HctXnFfsFD15GxgnlsqnzebhgjWCMIq1zBVkDlLCQmH8\n/PFN77rCQ+L505gUG1ho8+r3UrMMxiacQqvwkD6WzfJoZKp2NBuAsJ5CjzcBEL+N\nTxTZCfoMAovI8EmFgyROVMw7AXUwOrtoiUYZ48RZkEwjI+cjig2WOvlX8opmniOM\nviHse8pN61DQAFg46XvcujSdKN4M4N7AFdhYPrTjQwKBgQD7f+YYBX1YO/sXnU50\n4d+XiZ7jPSaomH7V94SyS2/yeBXOe//ZgbFgNKkkXVYYqz4lbiiVRaHd64paVwWb\ng1F8rDX9SFOpai+c9r9MEgbmjC0Jm8l4vz9+hWLip4nuTEyNmUxyybkOKLEzjP3u\nuQxlOa5SbzgNP8lGioueReEMowKBgQDMJV5lXRrtdc4N3zvXj8lz6UWpsqqVwBMw\nJFY8Iv8+Iz6fmoj2hVlWoDpI0zb2qANPNHT3H8/qA96tFPoUc7sYBIvPthOJoKKg\n2kiff4p5jlEMNkmQQglFo/sO9Ts99LiaXYGc3vGXxcPXs/tHn35fGUjKnzbi7oYB\n0FeTmM5a+wKBgGNPqvV7XXa1IL6/cFa5RsiZIHPNFvHmXddyCSU6orcVck76Khqi\nmv9JbC0e6juNi1nOeRoQyA1Q0G5CBMXXAhuACUW+BMNWWfzadsm8KJtraPFtYg5b\nPuBgHZ8w10eRO32CtmxxebC8otSfbTqSOfHS6CJHJtQchwdi+CUEpQyPAoGAJ1OX\nkK1T76S/EhsL+yW+6C5q9hruE7URvTdyyVjwlLbTbImnkt3zbOWm9LqDnxaUtKBl\nW+nr8qfWML+WwXPd+e1+RYBM2TlxuszyKo+2TF5nLJQUrc6a3KiPR71kMTZAjbQv\nsNmd7t/xL0+Du7N087r6M9ZiC2tps1XAWTWZoxsCgYEAk76zjkDY74II8UPmbgH9\nn+Q37gdB+DM4FoMXk3byf5M9K+4LNqnQYaPWJG9oLpo4d+ILRW6dVneNZMBakabs\nKKg4CAq1QPcFTev3G7TNjHYm8MlLYzzHigLoscrBc0UXUnH3Ce937NmNzPqwbVc+\nX2btmuI0MFZecXX/X3NfbRU=\n-----END PRIVATE KEY-----\n",
        "client_email": "iptv-246@project-id-6662602496862781661.iam.gserviceaccount.com",
        "client_id": "100643725159989766637",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/iptv-246%40project-id-6662602496862781661.iam.gserviceaccount.com"
    }

    gc = gspread.service_account_from_dict(credentials)
    spreadKey = '1__W0BD2Oydd2K9pzM60h7qvI8t-RzPQA3ctBqADPRpw'
    sheetName = 'IP'
    sh = gc.open_by_key(spreadKey)
    ws = sh.worksheet(sheetName)
    iplist=ws.col_values(2)
    print(iplist)
    # iplist.remove('aist')
    # for ip in iplist:
    #     if verify(udphostport=ip,mcast = "234.0.0.200:2000")==False:
    #         iplist.remove(ip)
    # # ws.batch_clear("B2:B300")
    # for ip in iplist:
    #     if verify(udphostport=ip,mcast = "234.0.0.200:2000")==False:
    #         iplist.remove(ip)
    list=[1, 2, "aa"]
    cells=[]
    cellsToUpdate = ws.range("B214:D214")
    # ws.cell(214,2,list[0])
    cells.append(ws.cell(214,2,list[0]))
    cells.append(ws.cell(214, 3, list[1]))
    cells.append(ws.cell(214, 4, list[2]))
    ws.update_cells(cells)




def ipToNum(ip):
    data = ip.split('.')
    return int(data[0]) * 256 ** 3 + int(data[1]) * 256 ** 2 + int(data[2]) * 256 ** 1 + int(data[3]) * 256 ** 0


def numToIP(num):
    "Convert 32-bit integer to dotted IPv4 address."
    return ".".join(map(lambda n: str(num >> n & 0xFF), [24, 16, 8, 0]))


def splitdiapazon(start_host, end_host, diapazoncount):
    # start_host = self.host  # '185.134.36.0'
    # end_host = '185.134.39.255'
    startIP = ipToNum(start_host)
    endIP = ipToNum(end_host)
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

def scanPorts():
    a = time.time()
    diapasons = splitdiapazon(start_host=start_host, end_host=end_host, diapazoncount=threads_count)
    for diapason in diapasons:
        ip1 = diapason[0]
        ip2 = diapason[1]
        scan = ScanPORTS(ip1, ip2, ports)
        scan.start()
        scans.append(scan)
        time.sleep(PAUSE)
    for t in scans:
        t.join()
    print(tvList)
    print("%s s" % (round(time.time() - a, 2)))

def aclient(udphostport):
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



def isudpxy(udphostport):
    try:
        stream = httplib.HTTPConnection(udphostport, timeout=timeout)
        stream.request("GET", "/stat")
        sresponse = stream.getresponse()
        hdr = sresponse.getheaders()[0]
        return str(hdr).find("Serve") > 0 and str(hdr).find("udpxy") > 0
    except:
        return False

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


class ScanPORTS(threading.Thread):

    def __init__(self, start_host, end_host, ports):
        threading.Thread.__init__(self)
        self.daemon = True
        # self.target=self.run
        self.start_host = start_host
        self.end_host = end_host
        self.ports = ports

    def run(self):
        print('Skenuojamas diapazonas %s - %s' % (numToIP(self.start_host), numToIP(self.end_host)))
        # print (self.start_host, self.end_host)
        for host in range(self.start_host, self.end_host):
            for port in self.ports:
                udphostport = '%s:%s' % (numToIP(host), port)
                # print (udphostport)
                isUdpxy = isudpxy(udphostport)
                if isUdpxy:
                    klientSk = aclient(udphostport)
                    # print (udphostport,klientSk)
                    if klientSk > 0:
                        geras = [udphostport, klientSk]
                        print(geras)
                        tvList.append(geras)
                    # elif klientSk == 0:
                        # print(udphostport, klientSk)
                        if verify(udphostport, mcast):
                            geras = [udphostport, klientSk]
                            print(geras)
                            tvList.append(geras)
        time.sleep(PAUSE)
        print('Baigiau diapazoną %s - %s' % (numToIP(self.start_host), numToIP(self.end_host)))








if __name__ == "__main__":
    scanPorts()
    #read_old_IP()
