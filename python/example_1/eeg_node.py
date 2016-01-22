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
import numpy as np
import scipy.signal

from midas.node import BaseNode
from midas import utilities as mu


# EEG processing node
class EEGNode(BaseNode):

    def __init__(self, *args):
        """ Initialize EEG node. """
        super().__init__(*args)
        self.metric_functions.append(self.brainbeat)

    def brainbeat(self, x):
        """ Calculates the brainbeat index from the input channels.
            Note: Function assumes the first channel is Fz and the second Pz.
            Implementation based on:
                Holm, A., et. al. (2009).
                Estimating brain load from the EEG.
                The Scientific World Journal, 9, 639-651.
        """
        f, P = scipy.signal.welch(x['data'][0], fs=self.primary_sampling_rate)
        p_fz_theta = np.mean(P[np.bitwise_and(f >= 4.0, f <= 8.0)])

        f, P = scipy.signal.welch(x['data'][1], fs=self.primary_sampling_rate)
        p_pz_alpha = np.mean(P[np.bitwise_and(f >= 8.0, f <= 12.0)])

        return p_fz_theta / p_pz_alpha

# Run the node from command line
if __name__ == '__main__':
    node = mu.midas_parse_config(EEGNode, sys.argv)
    if node:
        node.start()
        node.show_ui()
