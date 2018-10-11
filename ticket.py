#!/bin/python

import certifi
import  sys
import  time
import urllib3
import  json
from colorama import  Fore
import argparse
import asciichartpy

#args parse
parser = argparse.ArgumentParser(description='Ticket review')
parser.add_argument('name',   type=str, nargs='*',
                    help='set ticket for current worth')
parser.add_argument('-g', type=str, nargs='+',
                    help='graph for ticket')
parser.add_argument('-t', type=str, nargs='+', default='5d',
                    help='timestamp   (default:week; possibly:  1d,1mo,1y,max)')

args = parser.parse_args()
def request(ticket):

    link = "https://query1.finance.yahoo.com/v7/finance/quote?lang=en-US&region=US&corsDomain=finance.yahoo.com&fields="
    fields = "symbol,marketState,regularMarketPrice,regularMarketChange,regularMarketChangePercent,preMarketPrice,preMarketChange,\
preMarketChangePercent,postMarketPrice,postMarketChange,postMarketChangePercent"

    http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED',ca_certs=certifi.where())
    socket = http.request('GET', link+fields+'&symbols='+ticket)
    reply = json.loads(socket.data.decode('utf-8'))
    return reply


def format(reply):
    field = reply['quoteResponse']['result'][0]
    #print(field)
    #print(field.get('regularMarketChangePercent'))
    if field.get('regularMarketChangePercent') < 0:
        print(Fore.RED,end='')
    elif field.get('regularMarketChangePercent') > 0:
        print(Fore.GREEN,end='')


  #print(field.get('symbol'),field.get('regularMarketPreviousClose'),field.get('regularMarketPrice'),field.get('regularMarketChangePercent'))
    print('{:15} {:<10} {:<10}  {:5.2}'"%"  .format(field.get('symbol'),field.get('regularMarketPreviousClose'),field.get('regularMarketPrice'),field.get('regularMarketChangePercent')))
    #print('{1}      {0}'.format('one', 'two'))

    print(Fore.RESET,end='')

def graph_request(ticket, range):
    ticket = ''.join(ticket)
    range = ''.join(range)


    link = 'https://query1.finance.yahoo.com/v8/finance/chart/SBER.ME?range=2d&includePrePost=false&interval=1h&corsDomain=finance.yahoo.com&.tsrc=finance'
    link = link.replace('SBER.ME', ticket)
  #  print(range)
    link = link.replace('2d', range)
    if range == '1mo':
        link = link.replace('1h', '1d')
    elif range == '1y':
        link = link.replace('1h', '5d')
    elif range == 'max':
        link = link.replace('1h', '3mo')
    elif range == '1d':
        link = link.replace('1h', '15m')
  #  print(link)

    http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED',ca_certs=certifi.where())
    socket = http.request('GET', link)
    reply = json.loads(socket.data.decode('utf-8'))
    return reply


def graph_format(reply):
    timestamp = reply['chart']['result'][0]['timestamp']
    ticket = reply['chart']['result'][0]['meta']
    price = reply['chart']['result'][0]['indicators']['quote'][0]['open']
    #print(price )
    #print(timestamp)
    mass = [x for x in price if x is not None]

    while len(mass) >= 70:
        for x in range(len(mass)):
            # print(array[x])
            if x % 3 == 0 and x < len(mass):
                del mass[x]

    #range = ''.join(range)
    print(ticket.get("symbol"), "time:", ''.join(args.t))
    time_tuple1 = time.localtime(timestamp[0])
    time_tuple2 = time.localtime(timestamp[-1])
    #print(time.strftime("%D %H:%M", time_tuple))
    print("START:",(time.strftime("%D %H:%M", time_tuple1)),"     ","END:",(time.strftime("%D %H:%M", time_tuple2)))
    print(asciichartpy.plot(mass, {'height': 10}))
    print("-----------------------------------------------")



if args.name == None and args.g == None:
    parser.print_help(sys.stderr)
    sys.exit(1)
if args.name != None:
    for tick in args.name:
        ticket =request(tick)
        format(ticket)
    print("-----------------------------------------------")
if args.g != None:
    for tick in args.g:
        tic=graph_request(tick,args.t)
        graph_format(tic)




