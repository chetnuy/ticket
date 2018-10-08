#!/bin/python

import certifi
import urllib3
import  json

def price(ticket):
    link = "https://query1.finance.yahoo.com/v7/finance/quote?lang=en-US&region=US&corsDomain=finance.yahoo.com&fields="
    fields = "symbol,marketState,regularMarketPrice,regularMarketChange,regularMarketChangePercent,preMarketPrice,preMarketChange,\
preMarketChangePercent,postMarketPrice,postMarketChange,postMarketChangePercent"

    http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED',ca_certs=certifi.where())
    #make https request line
    socket = http.request('GET', link+fields+'&symbols='+ticket)
    d = json.loads(socket.data.decode('utf-8'))
    return d

ticket =price('1810.HK')
#print(ticket)
print(ticket['quoteResponse']['result'][0]['symbol'],ticket['quoteResponse']['result'][0]['regularMarketPreviousClose'],ticket['quoteResponse']['result'][0]['regularMarketPrice'],ticket['quoteResponse']['result'][0]['regularMarketChangePercent'])
ticket =price('AAPL')
#print(ticket)
print(ticket['quoteResponse']['result'][0]['symbol'],ticket['quoteResponse']['result'][0]['regularMarketPrice'],ticket['quoteResponse']['result'][0]['preMarketChangePercent'])
