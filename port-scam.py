#!/bin/python3
import sys
import socket
import concurrent.futures
from datetime import datetime
import argparse
import re
import sys


# help

parser = argparse.ArgumentParser()

subparsers = parser.add_subparsers(help='commands')
if(len(sys.argv) == 1):
    print("-h or --h for help")
else:
    pass
parser.add_argument('-p', action='store', nargs="+", type=int, dest='port',
                    default=[],
                    help='Enter port <port ranges>: Only scan specified ports Ex: -p 22 80 81 445 443')

parser.add_argument('-i', action='store', dest='ip', help='enter ip address')

value = parser.parse_args()


# regex chec
#re.match('\d+-\d+', a)


# Define our target
target = False
try:
    target = socket.gethostbyname(value.ip)  # translate hostname to IPv4
except:
    print("invalid amount of arguments")
    print("Syntax: python3 scanner.py")


# Add a pritty banner
def banner(target):
    print("-" * 50)
    print("scanning target " + target)
    print("Time started: " + str(datetime.now()))
    print("-"*50)


def port_scaner(target, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket.setdefaulttimeout(1)
        result = s.connect_ex((target, port))  # return error indator
        if result == 0:
            print("port {} is open".format(port))
        s.close()

    except KeyboardInterrupt:
        print("\nExiting program")
        sys.exit()

    except socket.gaierror:
        print("Hostname could not be resolved.")
        sys.exit()

    except socket.error:
        print("couldn't connect to server")
        sys.exit()


banner(target)

# threading
with concurrent.futures.ThreadPoolExecutor() as execitor:
    if(value.port):
        result = [execitor.submit(port_scaner, target, ports)
                  for ports in value.port]
    else:
        result = [execitor.submit(port_scaner, target, ports)
                  for ports in range(1023)]
