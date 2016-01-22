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

import pylsl
import time


def read_data(fname):
    data = open(fname, "r").readlines()
    data = [float(i.strip()) for i in data]
    return data


# read the data
d_iot = read_data("../../data/data_iot.csv")


# create outlets
fs = 10
info_iot = pylsl.StreamInfo('iot', 'luminance', 1, fs, 'float32', 'iot-data')
outlet_iot = pylsl.StreamOutlet(info_iot)

# stream the data
print("Streaming data...")
try:
    i = 0
    while True:
        outlet_iot.push_sample([d_iot[i]])
        time.sleep(1.0 / fs)
        if i == len(d_iot) - 1:
            i = 0
        else:
            i += 1
except KeyboardInterrupt:
    print('Stopping stream')
