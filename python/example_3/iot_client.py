#!/usr/bin/env python3

# Andreas Henelius <andreas.henelius@ttl.fi>,
# Jari Torniainen <jari.torniainen@ttl.fi>
# Finnish Institute of Occupational Health
# Copyright 2015
#
# This code is released under the MIT license
# http://opensource.org/licenses/mit-license.php
#
# Please see the file LICENSE for details

import requests
import time


def get_node_list(addr):
    """ Returns a list of available nodes. """
    return requests.get(addr + '/status/nodes').json()


def scale_value(value):
    """ Scale sensor value between 0 and 60. """

    if value > 1000:
        value = 1000
    elif value < 300:
        value = 300

    new_value = (value - 300.0) / 700.0

    return round(new_value * 60.0)


def print_luminance_level(addr):
    """ Prints the current luminance level to the console. """
    # Format the metric request
    addr += ('/iotnode/metric/'
             '{"type":"mean_luminance",'
             '"channels":["ch0"],'
             '"time_window":[5]}')

    # Request metric
    value = requests.get(addr).json()[0]['return']

    # Print response to the terminal
    print(time.ctime() +
          " " +
          '\033[93m' +
          '\033[1m' +
          ('*' * scale_value(value)) +
          '\033[0m')


def log_luminance(addr='http://127.0.0.1:8080'):
    """ MIDAS ambient light-level logger. """
    try:
        while True:
            node_list = get_node_list(addr)
            if 'iotnode' in node_list:
                print_luminance_level(addr)
            time.sleep(5)

    except KeyboardInterrupt:
        print("\nBye!")


if __name__ == '__main__':
    log_luminance()
