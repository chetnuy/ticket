#!/usr/bin/env python
# @author      : nevernew (nevernew@mail.ru)
# @created     : 26/02/2019
# @description :  this ticket.py OOP version

import threading
import certifi
import os.path
import  sys
import  time
import urllib3
import  json
from colorama import  Fore
import argparse
import asciichartpy


class Ticket(threading.Thread) :

    def __init__ (self, ticket):
        threading.Thread.__init__(self)
        self.ticket = ticket

    
    def run(self):
        reply = self.request(self.ticket)
        self.format(reply)


    def request(self, ticket):

        link = "https://query1.finance.yahoo.com/v7/finance/quote?lang=en-US&region=US&corsDomain=finance.yahoo.com&fields="
        fields = "symbol,marketState,regularMarketPrice,regularMarketChange,regularMarketChangePercent,preMarketPrice,preMarketChange,\
preMarketChangePercent,postMarketPrice,postMarketChange,postMarketChangePercent"

        http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED',ca_certs=certifi.where())
        socket = http.request('GET', link+fields+'&symbols='+ticket)
        reply = json.loads(socket.data.decode('utf-8'))
        return reply


    def format(self, reply):
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


class Graph(threading.Thread):

    def __init__(self, ticket_graph, range_graph):
        threading.Thread.__init__(self)
        self.ticket_graph = ticket_graph
        self.range_graph = range_graph

    def run(self):
        graph_reply = self.graph_request(self.ticket_graph, self.range_graph)
        self.graph_format(graph_reply)



    def graph_request(self, ticket, range):
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
       # print(link)

        http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED',ca_certs=certifi.where())
        socket = http.request('GET', link)
        reply = json.loads(socket.data.decode('utf-8'))
        return reply


    def graph_format(self, reply):
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
        print(ticket.get("symbol"), "timestamp:", ''.join(args.t))
        time_tuple1 = time.localtime(timestamp[0])
        time_tuple2 = time.localtime(timestamp[-1])
        #print(time.strftime("%D %H:%M", time_tuple))
        print("START:",(time.strftime("%D %H:%M", time_tuple1)),"     ","END:",(time.strftime("%D %H:%M", time_tuple2)))
        #print("dhh",mass)
        print(asciichartpy.plot(mass, {'height': 10}))
        print("-----------------------------------------------")




#thread_names = ['RUB=X', 'CNY=X', 'SBER.ME', 'LKOH.ME', 'YNDX.ME']
#long = [ '1d', '1mo', '1y', '1mo', '1y']
#
#for i in range(5):
#    thread = Ticket(thread_names[i])
##    thread.setName(thread_names[i])
#    thread.start()
#for i in range(5):
#    thread2= Graph(thread_names[i], long[i])
#    thread2.start()
#


parser = argparse.ArgumentParser(description='Ticket review')
parser.add_argument('name',   type=str, nargs='*',
                    help='set ticket for current worth')
parser.add_argument('-g', type=str, nargs='+',
                    help='graph for ticket')
parser.add_argument('-t', type=str, nargs='+', default='5d',
                    help='timestamp   (default:week; possibly:  1d,1mo,1y,max)')
parser.add_argument ('-i', '--info', action='store_const', const=True,
                    help='information of ticket')
parser.add_argument ('-l', '--list', action='store_const', const=True,
                     help='setup list of ticket')

args = parser.parse_args()



# if args.name == type(None) and args.g == type(None):
my_path = os.path.abspath(os.path.dirname(__file__))
infoFile = os.path.join(my_path, "info.txt")
listFile = os.path.join(my_path, "list.txt")
if args.info:
    file = open(infoFile, "r")
    print (file.read())
    sys.exit(0)
if args.list:
    file = open(listFile, 'r')
    rlist=(file.read().splitlines())
    for i in rlist:
        thread = Ticket(i)
        thread.start()
    sys.exit(0)
if not args.name  and not args.g :
    parser.print_help(sys.stderr)
    sys.exit(0)
if args.name != False:
    for tick in args.name:
        thread = Ticket(tick)
        thread.start()
    print("-----------------------------------------------")
if args.g != None:
    for tick in args.g:
      #  tic=graph_request(tick,args.t)
      #  graph_format(tic)
        thread2= Graph(tick, args.t)
        thread2.start()




