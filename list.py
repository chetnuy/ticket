#!/usr/bin/python

import  urllib3
import  json
import  certifi
import asciichartpy
import  time


def graph_requet(ticket, range):

    link = 'https://query1.finance.yahoo.com/v8/finance/chart/SBER.ME?range=2d&includePrePost=false&interval=1h&corsDomain=finance.yahoo.com&.tsrc=finance'
    link = link.replace('SBER.ME', ticket)
    link = link.replace('2d', range)
    if range == '1mo':
        link = link.replace('1h', '1d')
    elif range == '1y':
        link = link.replace('1h', '5d')
    elif range == 'max':
        link = link.replace('1h', '3mo')
    elif range == '1d':
        link = link.replace('1h', '15m')
    print(link)

    http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED',ca_certs=certifi.where())
    socket = http.request('GET', link)
    reply = json.loads(socket.data.decode('utf-8'))
    return reply

#def graph_format (reply):






massive = (graph_requet('SBER.ME', 'max'))
#print(massive)
#mass = massive['chart']['result']
#print(mass)
timestamp = massive['chart']['result'][0]['timestamp']
mass = massive['chart']['result'][0]['indicators']['quote'][0]['open']
#mass = mass['quote'][0]['open']
print(len(mass))
print(mass)
# while len(mass) > 70:
#      for x in mass:
#          if mass.append(i) == 0:



mass = [x for x in mass if x is not None]

while len(mass) >= 70:
    for x in range(len(mass)):
       # print(array[x])
        if x %3 == 0 and x < len(mass):
            del mass[x]

print(mass)
print(timestamp)
print(timestamp[0],timestamp[-1])

time_tuple = time.localtime(timestamp[0])
print(time.strftime("%D %H:%M", time_tuple))
time_tuple = time.localtime(timestamp[-1])
print(time.strftime("%D %H:%M", time_tuple))

print(asciichartpy.plot(mass, {'height': 10}))
