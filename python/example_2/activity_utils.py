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


import Xlib.display
import psutil
import ctypes
import os
import netifaces
from midas import utilities as mu


def get_netiface():
    """ Get the current active network interface. """
    ip = mu.get_ip()
    for interface in netifaces.interfaces():
        addrs = netifaces.ifaddresses(interface)
        if netifaces.AF_INET in addrs.keys():
            i_addr = addrs[netifaces.AF_INET][0]['addr']
            if i_addr == ip:
                return interface

    # Return None if no interface found
    return None


# --------------------------------------------------
# Get the application currently in use
# --------------------------------------------------
def current_app(x):
    """ Metric function for MIDAS that returns the
        app currently in focus
    """
    try:
        display = Xlib.display.Display()
        window = display.get_input_focus().focus
        wmclass = window.get_wm_class()

        if wmclass is None:
            window = window.query_tree().parent
            wmclass = window.get_wm_class()

        display.close()
        del display

        if wmclass:
            return(wmclass[1])
        else:
            return('UNKNOWN')
    except:
        return('ERROR!')


def net_stat_sent(x, interface=None):
    """ Get the number of bytes sent."""
    if not interface:
        interface = get_netiface()

    if interface:
        return psutil.net_io_counters(pernic=True)[interface].bytes_sent
    else:
        return 0


def net_stat_recv(x, interface=None):
    """ Get the number of bytes received. """
    if not interface:
        interface = get_netiface()
    if interface:
        return psutil.net_io_counters(pernic=True)[interface].bytes_recv
    else:
        return 0


def system_info(x):
    """ Get system info. """
    return list(os.uname())


# --------------------------------------------------
# Get the time that the user has been inactive
#
# Reference:
# http://thp.io/2007/09/x11-idle-time-and-focused-window-in.html
# --------------------------------------------------
class XScreenSaverInfo(ctypes.Structure):

    """ typedef struct { ... } XScreenSaverInfo; """
    _fields_ = [('window',      ctypes.c_ulong),  # screen saver window
                ('state',       ctypes.c_int),   # off, on, disabled
                ('kind',        ctypes.c_int),   # blanked,internal,external
                ('since',       ctypes.c_ulong),  # milliseconds
                ('idle',        ctypes.c_ulong),  # milliseconds
                ('event_mask',  ctypes.c_ulong)]  # events


# Return idle time in milliseconds
def idle_time(x):
    """ Metric function for MIDAS that returns the
        time that the user has been idle
    """

    libx11 = ctypes.cdll.LoadLibrary('libX11.so.6')
    display = libx11.XOpenDisplay(None)
    root = libx11.XDefaultRootWindow(display)
    libxss = ctypes.cdll.LoadLibrary('libXss.so.1')
    libxss.XScreenSaverAllocInfo.restype = ctypes.POINTER(XScreenSaverInfo)
    libxss_info = libxss.XScreenSaverAllocInfo()

    libxss.XScreenSaverQueryInfo(display, root, libxss_info)
    return libxss_info.contents.idle
