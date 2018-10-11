#!/bin/python

import certifi
import urllib3
import  json
from colorama import  Fore
import argparse

#args parse
parser = argparse.ArgumentParser(description='Ticket review')
parser.add_argument('name',   type=str, nargs='+',
                    help='set ticket')
parser.add_argument('-g', type=str, nargs='+',
                    help='graph for ticket(default: find the max)')
parser.add_argument('-t', type=str, nargs='+',
                    help='timestamp(default: week)')

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
    print('{:15} {:<10} {:<10}  {:5.2}'  .format(field.get('symbol'),field.get('regularMarketPreviousClose'),field.get('regularMarketPrice'),field.get('regularMarketChangePercent')))
    #print('{1}      {0}'.format('one', 'two'))

    print(Fore.RESET,end='')

def graph_request(ticket, range):

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


def graph_format(reply):
    timestamp = reply['chart']['result'][0]['timestamp']
    price = reply['chart']['result'][0]['indicators']['quote'][0]['open']





for tick in args.name:
    ticket =request(tick)
    format(ticket)
for tick in args.g:
    tick=graph_request(args.g,args.t)



