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


def equalize(x, n):
    return x[:(n-1)]

# read the data
d_ecg = read_data("../../data/data_ecg.csv")
d_fz = read_data("../../data/data_eeg_fz.csv")
d_pz = read_data("../../data/data_eeg_pz.csv")

# make the data equally long
dset = (d_ecg, d_fz, d_pz)
n = min(list(map(len, dset)))
d_ecg, d_fz, d_pz = [equalize(d, n) for d in dset]

# create outlets
fs = 100
info_ecg = pylsl.StreamInfo('ecg', 'ECG', 1, fs, 'float32', 'ecg-data')
info_eeg = pylsl.StreamInfo('eeg', 'EEG', 2, fs, 'float32', 'eeg-data')
outlet_ecg = pylsl.StreamOutlet(info_ecg)
outlet_eeg = pylsl.StreamOutlet(info_eeg)

# stream the data
print("Streaming data...")
try:
    i = 0
    while True:
        outlet_ecg.push_sample([d_ecg[i]])
        outlet_eeg.push_sample([d_fz[i], d_pz[i]])
        time.sleep(1.0 / fs)
        if i == len(d_ecg) - 1:
            i = 0
        else:
            i += 1
except KeyboardInterrupt:
    print('Stopping stream')
