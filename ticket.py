#!/usr/bin/env python
# @author      : nevernew (nevernew@mail.ru)
# @created     : 26/02/2019
# @description : v.0.8 add ticket.list

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
        self._return = self.request(self.ticket)
    
    def join(self):
        threading.Thread.join(self)
        return self._return

    def request(self, ticket):
        link = "https://query1.finance.yahoo.com/v7/finance/quote?lang=en-US&region=US&corsDomain=finance.yahoo.com&fields="
        fields = "symbol,marketState,regularMarketPrice,regularMarketChange,regularMarketChangePercent,preMarketPrice,preMarketChange,\
preMarketChangePercent,postMarketPrice,postMarketChange,postMarketChangePercent"
        http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED',ca_certs=certifi.where())
        socket = http.request('GET', link+fields+'&symbols='+ticket)
        reply = json.loads(socket.data.decode('utf-8'))
        field = reply['quoteResponse']['result'][0]
        return field


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
        link = link.replace('2d', range)
        if range == '1mo':
            link = link.replace('1h', '1d')
        elif range == '1y':
            link = link.replace('1h', '5d')
        elif range == 'max':
            link = link.replace('1h', '3mo')
        elif range == '1d':
            link = link.replace('1h', '15m')
        http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED',ca_certs=certifi.where())
        socket = http.request('GET', link)
        reply = json.loads(socket.data.decode('utf-8'))
        return reply


    def graph_format(self, reply):
        timestamp = reply['chart']['result'][0]['timestamp']
        ticket = reply['chart']['result'][0]['meta']
        price = reply['chart']['result'][0]['indicators']['quote'][0]['open']
        mass = [x for x in price if x is not None]

        while len(mass) >= 70:
            for x in range(len(mass)):
                if x % 3 == 0 and x < len(mass):
                    del mass[x]

        print(ticket.get("symbol"), "timestamp:", ''.join(args.t))
        time_tuple1 = time.localtime(timestamp[0])
        time_tuple2 = time.localtime(timestamp[-1])
        print("START:",(time.strftime("%D %H:%M", time_tuple1)),"     ","END:",(time.strftime("%D %H:%M", time_tuple2)))
        print(asciichartpy.plot(mass, {'height': 10}))
        print("-----------------------------------------------")



class ReadConfig():

    def __init__(self, configPath):
        self.configPath = configPath
        self.TicketListFromConf = []
        self.RawConfig = []
        self.ParseConfFile()


    def ParseConfFile(self):
        file = open(configPath, 'r')
        self.RawConfig=(file.read().splitlines())

        for i in self.RawConfig:
            if "###" in i:
                continue
            elif ";;;" in i:
                continue
            else:
                self.TicketListFromConf.append(i)

    def getTupleConfig(self):
        return self.TicketListFromConf, self.RawConfig


class FormatList():
    
    def __init__(self, tupleConfig):
        self.tupleConfig = tupleConfig


    def read(self):
        return 0
    

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
configPath= os.path.join(my_path, "ticket.list")
threads = []
dticket = {}

if args.info:
    file = open(infoFile, "r")
    print (file.read())
    sys.exit(0)

if args.list:

    myReadConfig = ReadConfig(configPath)
    tupleConfig = myReadConfig.getTupleConfig()

    for i in tupleConfig[0]:
        thread = Ticket(i)
        thread.start()
        threads.append(thread)

    for x in threads:
        x.join()
        dticket.update({x:x.join()})

    for i in range (len(tupleConfig[1])):
       if "###" in tupleConfig[1][i]:
            continue
       elif ";;;" in tupleConfig[1][i]:
            print(tupleConfig[1][i])
       else :
           for val in dticket.values():
                if tupleConfig[1][i] == val.get('symbol'):
                   if val.get('regularMarketChangePercent') < 0:
                        print(Fore.RED,end='')
                   elif val.get('regularMarketChangePercent') > 0:
                        print(Fore.GREEN,end='')
                   print('{:15} {:<10} {:<10}  {:5.2}'"%"  .format(val.get('symbol'),val.get('regularMarketPreviousClose'),val.get('regularMarketPrice'),val.get('regularMarketChangePercent')))
                   print(Fore.RESET,end='')

    sys.exit(0)


if args.name != False:

    for tick in args.name:
        thread = Ticket(tick)
        thread.start()
        threads.append(thread)

    for i in threads:
        i.join()
        if i.join().get('regularMarketChangePercent') < 0:
             print(Fore.RED,end='')
        elif i.join().get('regularMarketChangePercent')> 0:
             print(Fore.GREEN,end='')
        print('{:15} {:<10} {:<10}  {:5.2}'"%"  .format(i.join().get('symbol'),i.join().get('regularMarketPreviousClose'),i.join().get('regularMarketPrice'),i.join().get('regularMarketChangePercent')))
        print(Fore.RESET,end='')

#    sys.exit(0)

if args.g != None:
    for tick in args.g:
        thread_graph= Graph(tick, args.t)
        thread_graph.start()


if not args.name  and not args.g :
    parser.print_help(sys.stderr)
    sys.exit(0)
