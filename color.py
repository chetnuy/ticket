#!/usr/bin/python

#from colorama import Fore, Back, Style
from colorama import Fore
print(Fore.RED + 'some red text', Fore.RESET)
print(Fore.GREEN + 'some red text', Fore.RESET)
#print(Back.GREEN + 'and with a green background')
#print(Style.DIM + 'and in dim text')
#print(Style.RESET_ALL)
print('back to normal now')

def cprint (messages):
    print(Fore.RED + messages, Fore.RESET)

cprint('hane')
