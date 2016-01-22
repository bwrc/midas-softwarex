#!/usr/bin/env python

# Andreas Henelius <andreas.henelius@ttl.fi>,
# Finnish Institute of Occupational Health
# Copyright 2015
#
# This code is released under the MIT license
# http://opensource.org/licenses/mit-license.php
#
# Please see the file LICENSE for details


import scipy
import scipy.signal
import numpy

# -----------------------------------------------------------------------------
# Time domain analysis functions for IBI series
# -----------------------------------------------------------------------------


def hrv_mean_ibi(ibi):
    """ average interbeat interval length """
    return numpy.mean(ibi)


def hrv_mean_hr(ibi):
    """ average heart rate """
    return 6e4 / numpy.mean(ibi)


def hrv_rmssd(ibi):
    """ root mean square of successive differences """
    return scipy.sqrt(scipy.sum(scipy.diff(ibi)**2) / (len(ibi) - 1))


def hrv_var(ibi):
    """ variance of the interbeat interval lengths """
    return scipy.var(ibi)


def hrv_std(ibi):
    """ standard deviation of the interbeat interval lengths """
    return scipy.std(ibi)


def hrv_pnnx(ibi, p=50):
    """ percentage of normal-to-normal intervals exceeding x milliseconds """
    return 100 * scipy.sum(abs(scipy.diff(ibi)) >= float(p)) / len(ibi)

# -----------------------------------------------------------------------------
# Frequency domain analysis functions for IBI series
# -----------------------------------------------------------------------------


def bandpower(f, Pxx, fmin, fmax):
    """ integrate the power spectral density between fmin and fmax
        using the trapezoidal method
    """
    ind_min = scipy.argmax(f > fmin) - 1
    ind_max = scipy.argmax(f > fmax) - 1
    return scipy.trapz(Pxx[ind_min: ind_max], f[ind_min: ind_max])


def hrv_lomb(ibi, fmin, fmax):
    """ Calculate the power in the given frequency band using the Lomb-Scargle
        periodogram.

    Args:
          ibi: the IBI series
        fmin : lower frequency of the band being considered
        fmax : upper frequency of the band being considered
    """

    ibi = scipy.array(ibi)
    ibi_t = scipy.concatenate([[0], scipy.cumsum(ibi[:-1])])

    N = 512.0
    f = scipy.linspace(1.0 / N, 40.0, N)
    p = scipy.signal.lombscargle(ibi_t, ibi, f)
    return bandpower(f, p, fmin, fmax)

# -----------------------------------------------------------------------------
# R-peak detection from an ECG signal
# -----------------------------------------------------------------------------


def moving_average(ecg, n=10):
    return numpy.convolve(ecg, numpy.ones((n,)) / n, mode='valid')


def detect_r_peaks(ecg, fs=500):
    """ Calculate peak stuff from ecg stuff. """

    def adjust_indices(ind_start, ind_stop):
        if (ind_stop[0] <= ind_start[0]):
            ind_stop = ind_stop[1:]

        n_min = numpy.min([len(ind_start), len(ind_stop)])
        ind_start = ind_start[:n_min]
        ind_stop = ind_stop[:n_min]

        return ind_start, ind_stop

    def find_r_peak(ecg, ind_rise, ind_fall):
        r_peak_height = []
        r_peak_position = []

        for rise, fall in zip(ind_rise, ind_fall):
            peak_region = ecg[rise:fall]
            if peak_region.size:
                r_peak_height.append(max(peak_region))
                r_peak_position.append(numpy.argmax(peak_region) + rise - 1)
        return r_peak_height, r_peak_position

    ecg_orig = numpy.copy(ecg)
    tmp = scipy.signal.medfilt(ecg, 31)
    ecg = ecg - tmp

    thr = 0.70 * numpy.max(ecg)

    # Make the signal binary
    ecg[ecg < thr] = 0
    ecg[ecg >= thr] = 1

    # Find rising and falling edges used to window the R-peak
    ind_rising = numpy.where(numpy.diff(ecg) == 1)[0]
    ind_falling = numpy.where(numpy.diff(ecg) == -1)[0]

    ind_rising, ind_falling = adjust_indices(ind_rising, ind_falling)

    ind_rising = [(i - round(fs/4)) for i in ind_rising]
    ind_falling = [(i - round(fs/4)) for i in ind_falling]

    # Determine the R-peak for each pair of rising and falling edges
    peak_height, peak_position = find_r_peak(ecg_orig, ind_rising, ind_falling)

    rr = 1000 * (numpy.diff(peak_position) / fs)
    return rr


# -----------------------------------------------------------------------------
