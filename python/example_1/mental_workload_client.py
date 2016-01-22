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
import sys


def print_physiological_state(bb_thr, rr_thr, start_time):
    """ Retrive and print activity metrics of ECG and EEG nodes. """
    # Format the metric requests
    addr = 'http://127.0.0.1:8080'
    bb_request = ('/eegnode/metric/'
                  '{"type":"brainbeat",'
                  '"channels":["Fz", "Pz"],'
                  '"time_window":[15]}')

    rr_request = ('/ecgnode/metric/'
                  '{"type":"mean_hr",'
                  '"channels":["ch0"],'
                  '"time_window":[15]}')

    # Perform requests
    bb = requests.get(addr + bb_request).json()[0]['return']
    rr = requests.get(addr + rr_request).json()[0]['return']

    # Get classification
    mwl_class = int(bb > bb_thr and rr > rr_thr)
    time_stamp = time.time() - start_time

    # Print results
    print('{3:06.1f} {0:06.2f} {1:06.2f} {2:3d}'.format(bb, rr, mwl_class, time_stamp))


def log_physiological_state(bb_thr=1.5, rr_thr=65):
    """ MIDAS physiological state logger. """
    try:
        print(' TIME    BB     HR    CLS')
        start_time = time.time()
        while True:
            print_physiological_state(bb_thr, rr_thr, start_time)
            time.sleep(5)
    except KeyboardInterrupt:
        print("\nBye!")


if __name__ == '__main__':
    if len(sys.argv) == 3:
        log_physiological_state(float(sys.argv[1]), float(sys.argv[2]))
    else:
        log_physiological_state()
