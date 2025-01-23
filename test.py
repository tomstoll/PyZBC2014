import numpy as np
import pyzbc2014 as zbc
import matplotlib.pyplot as plt 

# Synthesize sinusoid; 1 kHz, 50 dB SPL
t = np.arange(0.0, 1.0, 1/100e3)
x = np.sin(2 * np.pi * 1e3 * t)
x = 20e-6 * 10**(50.0/20.0) * np.sqrt(2) * x

# Simulate IHC waveform and AN waveform, plot result
ihcout = zbc.sim_ihc_zbc2014(x, cf=1e3)
anout = zbc.sim_anrate_zbc2014(ihcout, cf=1e3)
plt.plot(anout)
plt.show()

# Simulate population response to pure tone
cfs = np.exp(np.linspace(np.log(0.5e3), np.log(2e3), 21))
rates = np.zeros(cfs.size)
for i in range(cfs.size):
    ihcout = zbc.sim_ihc_zbc2014(x, cf=cfs[i])
    anout = zbc.sim_anrate_zbc2014(ihcout, cf=cfs[i])
    rates[i] = np.mean(anout)

plt.plot(cfs, rates)
plt.show()