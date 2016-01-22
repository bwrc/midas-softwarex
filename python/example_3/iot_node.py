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
from midas.node import BaseNode
from midas import utilities as mu
import numpy as np


class IOTNode(BaseNode):

    def __init__(self, *args):
        """ Initialize example node. """
        super().__init__(*args)
        self.metric_functions.append(self.mean_luminance)

    def mean_luminance(self, x):
        """ Returns the average luminance """
        return np.mean(x['data'][0])


if __name__ == '__main__':
    node = mu.midas_parse_config(IOTNode, sys.argv)

    if node is not None:
        node.start()
        node.show_ui()
