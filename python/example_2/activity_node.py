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
import activity_utils


# ------------------------------------------------------------------------------
# Create an Activity Node based on the Base Node
# ------------------------------------------------------------------------------
class ActivityNode(BaseNode):
    """ MIDAS Activity Node """

    def __init__(self, *args):
        """ Initialize example node. """
        super().__init__(*args)
        self.metric_functions.append(activity_utils.current_app)
        self.metric_functions.append(activity_utils.idle_time)
        self.metric_functions.append(activity_utils.net_stat_sent)
        self.metric_functions.append(activity_utils.net_stat_recv)
        self.metric_functions.append(activity_utils.system_info)

# ------------------------------------------------------------------------------
# Run the node if started from the command line
# ------------------------------------------------------------------------------
if __name__ == '__main__':
    node = mu.midas_parse_config(ActivityNode, sys.argv)
    if node is not None:
        node.start()
        node.show_ui()
# ------------------------------------------------------------------------------
# EOF
# ------------------------------------------------------------------------------
