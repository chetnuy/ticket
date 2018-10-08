#!/usr/bin/python

from colorama import Fore

def cprint (messages):
    print(Fore.RED + messages, Fore.RESET)

cprint('hane')
print('line')
cprint("new line")
