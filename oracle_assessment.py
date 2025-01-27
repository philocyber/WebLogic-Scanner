#!/usr/bin/env python
# _*_ coding:utf-8 _*_

import sys
import requests
from requests.exceptions import Timeout
from app.platform import Color
import subprocess
import argparse
from app.main import pentest


def read_file(file):
    with open(file) as fp:
        lines = fp.read()
        urls = lines.split('\n')
        ip_from_urls = list()
    for url_file in urls:
        url_file = url_file.split('/')[2]
        url_file = url_file.split(':')[0]
        has_ip = subprocess.check_output(['dig', url_file, '+short', '|', 'sed', "'/[a-z]/d'", '|', 'sed', '-n', 'lp'])
        if has_ip.decode():
            value = has_ip.decode().split("\n")
            ip = value[-2]
            port = '7001'
            print('Starting scanner against:', url_file + ' [' + ip + ']')
            ip_from_urls.append(ip)
            exception(ip, port)
        else:
            continue
    print('\nScan and exploitation completed\n')
    return


def read_url(url, port):
    # taking the url as a unique parameter I change it to obtain an IP address
    ip_to_url = subprocess.check_output(['dig', url, '+short', '|', 'sed', "'/[a-z]/d'", '|', 'sed', '-n', 'lp'])
    if ip_to_url.decode():
        value = ip_to_url.decode().split('\n')
        ip = value[-2]
        print('Starting scanner against:', ip)
        # with this, I try to create a Timeout Exception to finish the program if applies..
        try:
            response = requests.get('http://' + str(ip) + ':' + '7001', verify=False, timeout=10)
        except Timeout as e:
            print(Color.OKBLUE + '-\nTimeout Limit exceeded - Looks like your target is not a WebLogic '
                                 'Server\n- ' + Color.ENDC)
            sys.exit()
        if response.status_code == 200:
            pentest(ip, port)
        else:
            sys.exit()
    else:
        sys.exit()
    print('\nScan and exploitation completed\n')
    return


def exception(ip, port):
    try:
        response = requests.get('http://' + str(ip) + ':' + '7001', verify=False, timeout=10)
    except Timeout as e:
        print(Color.OKBLUE + '-\nTimeout Limit exceeded - Destination Host [' + str(ip) + '] unreachable\n- '
              + Color.ENDC)
        return
    except requests.exceptions.ConnectionError as i:
        print(Color.OKBLUE + '-\nConnection Error - Destination Host [' + str(ip) + '] unreachable\n- '
              + Color.ENDC)
        return
    print(response.status_code)
    if response.status_code == 200:
        pentest(ip, port)
    else:
        return
    return


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-u ', '--url',
                        help="specify the url, like the following example:\n-u example.com ",
                        required=False)
    parser.add_argument('-i ', '--ip',
                        help="specify an IP address, like the following example:\n-i 192.168.0.50",
                        required=False)
    parser.add_argument('-f ', '--file',
                        help="specify a file, like the following example:\n-f example.txt ",
                        required=False)
    args = parser.parse_args()

    if not args.url and not args.file and not args.ip:
        print("[*]\nYou need at least one argument, choose between -u [URL], -i [IP] or -f [FILE]\n[*]")
        parser.print_help()
        sys.exit()
    if args.url and not args.file and not args.ip:
        if args.url:
            url = str(args.url)
            port = '7001'
            read_url(url, port)
        else:
            print("\nHouston, we have a problem, please try the following:")
            print('[*] python oracle_assessment.py -u example.com\n[*] python oracle_assessment.py -i 192.168.0.50\n'
                  '[*] python oracle_assessment.py -f example.txt')
    if args.ip and not args.url and not args.file:
        if args.ip:
            ip = str(args.ip)
            port = '7001'
            pentest(ip, port)
        else:
            print("\nHouston, we have a problem, please try the following:")
            print('[*] python oracle_assessment.py -u example.com\n[*] python oracle_assessment.py -i 192.168.0.50\n'
                  '[*] python oracle_assessment.py -f example.txt')
    if args.file and not args.url and not args.ip:
        if args.file:
            file = str(args.file)
            read_file(file)
        else:
            print("\nHouston, we have a problem, please try the following:")
            print('[*] python oracle_assessment.py -u example.com\n[*] python oracle_assessment.py -i 192.168.0.50\n'
                  '[*] python oracle_assessment.py -f example.txt')
