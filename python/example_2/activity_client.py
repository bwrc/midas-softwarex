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


def print_activity_metrics(addr, node_name):
    """ Retrive and print activity metrics of the specified node. """
    # Format the metric request
    addr = addr + '/' + node_name + '/metric/'
    addr += ('[{"type":"current_app"},'
             '{"type":"idle_time"},'
             '{"type":"net_stat_sent"},'
             '{"type":"net_stat_recv"}]')
    responses = requests.get(addr).json()

    # Parse response and print result to the terminal
    s = time.ctime() + " " + node_name.ljust(10) + " "
    for response in responses:
        value = response['return']
        if isinstance(value, str):
            s += value.ljust(16)
        else:
            value = value / 1e3
            if response['type'] == "idle_time" and value > 60:
                s += ('\033[91m' + str(value).ljust(16) + '\033[0m')
            else:
                s += str(value).ljust(16)

    print(s)


def log_activity(addr='http://127.0.0.1:8080'):
    """ MIDAS corporate activity logger. """
    try:
        while True:
            node_list = get_node_list(addr)
            for node in node_list:
                if (node_list[node]['status'] == 'online' and
                        node_list[node]['type'] == 'Activity'):
                    print_activity_metrics(addr, node)
            time.sleep(5)

    except KeyboardInterrupt:
        print("\nBye!")


if __name__ == '__main__':
    log_activity()
