import numpy as np
import ctypes
from numpy.ctypeslib import ndpointer

def test():
    x = np.zeros(5000)
    ihcout = np.zeros(5000)
    sim_ihc_zbc2014(x, 1e3, 1, 1/100e3, len(x), 1.0, 1.0, 1, ihcout)
    return ihcout

def sim_ihc_zbc2014(px, cf, nrep, tdres, totalstim, cohc, cihc, species, ihcout):
    # Open library, fetch IHCAN function, declare input types for call
    lib = ctypes.cdll.LoadLibrary("./model/libzbc2014.so")
    fun = lib.IHCAN
    fun.argtypes = [
        ndpointer(ctypes.c_double),
        ctypes.c_double,
        ctypes.c_int,
        ctypes.c_double,
        ctypes.c_int,
        ctypes.c_double,
        ctypes.c_double,
        ctypes.c_int,
        ndpointer(ctypes.c_double),
    ]

    # Place function call and return IHC output waveform
    fun(px, cf, nrep, tdres, totalstim, cohc, cihc, species, ihcout)
    return ihcout