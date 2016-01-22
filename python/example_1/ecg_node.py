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

import sys
import ecg_utilities

from midas.node import BaseNode
from midas import utilities as mu


# ECG processing node
class ECGNode(BaseNode):

    def __init__(self, *args):
        """ Initialize ECG node. """
        super().__init__(*args)

        # Append function handles to the metric_functions-list
        self.metric_functions.append(self.mean_hr)

    def mean_hr(self, x):
        """ Calculate the average heart rate
            from the raw ECG signal x by first
            obtaining the RR-intervals using
            R-peak detection.
        """
        rr = ecg_utilities.detect_r_peaks(x['data'][0],
                                          self.primary_sampling_rate)
        return ecg_utilities.hrv_mean_hr(rr)


# Run the node from command line
if __name__ == '__main__':
    node = mu.midas_parse_config(ECGNode, sys.argv)
    if node:
        node.start()
        node.show_ui()
