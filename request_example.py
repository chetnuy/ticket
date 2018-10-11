#!/bin/python

import certifi
import urllib3
import  json
from colorama import  Fore
import argparse

# args pare
parser = argparse.ArgumentParser(description='Печать тикетов')
parser.add_argument('name',   type=str, nargs='+',
                    help='set ticket')
parser.add_argument('--graph', type=str, nargs='+',
                    help='sum the integers (default: find the max)')

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
    print('{:15} {:<10} {:<10} {:.6}'  .format(field.get('symbol'),field.get('regularMarketPreviousClose'),field.get('regularMarketPrice'),field.get('regularMarketChangePercent')))
    #print('{1}      {0}'.format('one', 'two'))

    print(Fore.RESET,end='')


for tick in args.name:
    ticket =request(tick)
    format(ticket)



