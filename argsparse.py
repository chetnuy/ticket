#!/bin/python

import argparse

parser = argparse.ArgumentParser(description='Печать тикетов')
parser.add_argument('ticket',   type=str, nargs='+',
                    help='set ticket')
parser.add_argument('--graph', type=str, nargs='+',
                    help='sum the integers (default: find the max)')

args = parser.parse_args()

print ("mess",args.ticket)
print ("mess",args.graph)
