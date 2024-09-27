import numpy as np
import ctypes
from numpy.ctypeslib import ndpointer
import warnings

def test():
    t = np.arange(0.0, 1.0, 1/100e3)
    x = np.sin(2 * np.pi * 1e3 * t)
    x = 20e-6 * 10**(50.0/20.0) * np.sqrt(2) * x
    ihcout = sim_ihc_zbc2014(x, cf=1e3, nrep=1, fs=100e3, cohc=1.0, cihc=1.0, species=1)
    return ihcout


def sim_ihc_zbc2014(
        px, 
        cf=1e3, 
        nrep=1, 
        fs=100e3, 
        cohc=1.0, 
        cihc=1.0, 
        species=1, 
        extratime=0.0
):
    """ Simulates inner-hair-cell response to sound-pressure waveform.

    Performs some basic input checking and then passes sound-pressure-waveform and 
    pre-allocated output array to the C IHCAN function via the ctypes library. 

    Args:
      px:
        Sound pressure waveform (1D vector of floats, units of Pa)
      cf:
        Characteristic frequency (Hz)
      nrep:
        Number of reps to generate (only a single rep is simulated, others are appended copies)
      fs:
        Sampling rate (Hz)
      cohc:
        Status of the outer hair cells, in range of [0, 1] with 1 being fully normal/healthy
      cihc:
        Status of the inner hair cells, in range of [0, 1] with 1 being fully normal/healthy
      species:
        Integer, encoding species (1 == cat, 2 == Human [Shera], 3 == Human [Glasberg])
      extratime:
        How many extra samples to simulate after nominal stimulus offset, expressed as decimal fraction of total duration 
    
    """
    # First, enforce assumptions about inputs
    assert np.ndim(px) == 1  # input is 1D vector
    assert nrep >= 1  # number of reps is geq 1
    assert 0 <= cohc <= 1  # C_OHC is between zero and one
    assert 0 <= cihc <= 1  # C_IHC is between zero and one
    assert species in [1, 2, 3]  # species is one of available options
    if species == 1:
        assert .125e3 <= cf <= 40e3  # for cat, CF must be between 0.125 and 40 kHz
    else:
        assert .125e3 <= cf <= 20e3  # for human, CF must be between 0.125 and 20 kHz

    # Emit warnings
    if fs < 100e3:
        warnings.warn("Note, time-domain resolution is less than recommended (sampling rate > 100 kHz, sampling period < 1e-5 s)")

    # Allocate empty storage for output
    totalstim = len(px) + round(len(px)/fs*extratime)  # totalstim is number of samples in stim plus number of samples in extratime*dur
    ihcout = np.zeros(totalstim*nrep)

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
    fun(px, cf, nrep, 1/fs, totalstim, cohc, cihc, species, ihcout)
    return ihcout