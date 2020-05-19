#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
gnpy.core.info
==============

This module contains classes for modelling :class:`SpectralInformation`.
'''


from collections import namedtuple
from gnpy.core.utils import lin2db
from gnpy.core.equipment import automatic_nch


class Power(namedtuple('Power', 'signal nli ase')):
    """carriers power in W"""


class Channel(namedtuple('Channel', 'channel_number frequency baud_rate roll_off power')):
    pass


class Pref(namedtuple('Pref', 'p_span0, p_spani, neq_ch ')):
    """noiseless reference power in dBm:
    p_span0: inital target carrier power
    p_spani: carrier power after element i
    neq_ch: equivalent channel count in dB"""


class SpectralInformation(namedtuple('SpectralInformation', 'pref carriers')):

    def __new__(cls, pref, carriers):
        return super().__new__(cls, pref, carriers)


def create_input_spectral_information(f_min, f_max, roll_off, baud_rate, power, spacing):
    # pref in dB : convert power lin into power in dB
    pref = lin2db(power * 1e3)
    nb_channel = automatic_nch(f_min, f_max, spacing)
    si = SpectralInformation(
        pref=Pref(pref, pref, lin2db(nb_channel)),
        carriers=[
            Channel(f, (f_min + spacing * f),
                    baud_rate, roll_off, Power(power, 0, 0)) for f in range(1, nb_channel + 1)
        ])
    return si
