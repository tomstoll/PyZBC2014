# Introduction
PyZBC2014 is a barebones Python wrapper around the Zilany, Bruce, and Carney (2014) auditory-nerve (AN) model, which is written in C/Mex. 

# Install
## Download
To install PyZBC2014, first install this package with pip from GitHub. To do so, in any
terminal that can call your preferred copy of `pip`, run the following:

``` pip install pip@git+https://github.com/guestdaniel/PyZBC2014```

## Compile model
Next, compile the `.c` files that are bundled with the package by navigating to the `model`
folder and running the following code for GCC (or equivalent code, based on your C
compiler):

### Windows (with gcc)
```
gcc -c -Wall -fPIC -O3 complex.c 
gcc -c -Wall -fPIC -O3 model_IHC.c
gcc -c -Wall -fPIC -O3 model_Synapse.c
gcc -shared -o libzbc2014.so complex.o model_IHC.o model_Syanpse.o
```
There may be some protests from the compiler about the `-fPIC` flag; send me the outputs of any failed compilation and I'll try to diagnose!

### Unix (with gcc)
```
gcc -c -Wall -fPIC -O3 complex.c 
gcc -c -Wall -fPIC -O3 model_IHC.c
gcc -c -Wall -fPIC -O3 model_Synapse.c
gcc -shared -o libzbc2014.so complex.o model_IHC.o model_Syanpse.o
```

### Other operating systems
Try and let me know?

## Modify paths
Finally, you will need to modify the paths defined in `pyzbc2014.py` accordingly.

# Usage
PyZBC2014 defines two function, `sim_ihc_zbc2014` and `sim_anrate_zbc2014`, to simulate inner-hair-cell (IHC) potentials from sound-pressure waveforms or AN instantaneous rates from IHC potentials, respectively.
Comparing to the origianl MATLAB/Mex implementation of the 2014 model, these behave similarly to the `IHCAN` and `Synapse` functions, respectively, with some small differences in behavior and some improvements in quality-of-life.

## Simulate IHC response
To simulate an IHC response, you need to provide a sound-pressure waveform in 1D Numpy vector format to the `sim_ihc_zbc2014` function; it will return an IHC potential waveform of exactly the same size and format.
Parameters can be modified by keyword arguments:
- `cf`: Characteristic frequency (Hz)
- `nrep`: Number of reps to generate (only a single rep is simulated, others are appended copies)
- `fs`: Sampling rate (Hz), should generally be at least 100 kHz, and higher for cat/very-high-CF simulations; note that your stimulus must be sampled at this frequency!
- `cohc`: Status of the outer hair cells, in range of [0, 1] with 1 being fully normal/healthy
- `cihc`: Status of the inner hair cells, in range of [0, 1] with 1 being fully normal/healthy
- `species`: String encoding species to use in [`"cat"`, `"human"`, `"human-glasberg"`]. In the MATLAB/Mex wrapper, `species=1` corresponds to `"cat"`, `species=2` corresponds to `"human"` (and indicates human with the sharp peripheral tuning suggested by Shera and Oxenham), and `species=3` corresponds to `"human-glasberg"` (and indicates broader peripheral tuning suggested by Glasberg and Moore)

The full function call using default keyword arguments is thus:
```
ihc_potential = sim_ihc_zbc2014(px, cf=1e3, nrep=1, fs=100e3, cohc=1.0, cihc=1.0, species=2)
```

## Simulate AN response
To simulate an AN response, you need to provide an IHC potential (from the output of `sim_ihc_zbc2014`) in 1D Numpy vector format to the `sim_anrate_zbc2014` function; it will return a prediction of instantaneous AN firing rate rate of exactly the same size and format.
Parameters can be modified by keyword arguments:
- `cf`: Characteristic frequency (Hz)
- `nrep`: Number of reps to simulate, should always match value used in `sim_ihc_zbc2014`
- `fs`: Sampling rate (Hz), should generally be at least 100 kHz, and higher for cat/very-high-CF simulations, should always match value used for `sim_ihc_zbc2014`
- `fibertype`: String encoding which fiber type to simulate in [`"hsr"`, `"msr"`, `"lsr"`]
- `powerlaw`: String encoding whether to use true powerlaw adaptation (`"true"`) or approximate powerlaw adaptation (`"approx"`). In the MATLAB/Mex wrapper, `implnt=1` corresponds to `"true"` and `implnt=0` corresponds to `"approx"`
- `noisetype`: String encoding whether to use no fractional Gaussian noise (`"none"`), frozen noise (`"frozen"`), or fresh noise (`"fresh"`). In the MATLAB/Mex wrapper, `noiseType=0` corresponds to `"frozen"` and `noiseType=1` corresponds to `"fresh"`

The full function call using default keyword arguments is thus:
```
anrate = sim_anrate_zbc2014(ihc, cf=1e3, nrep=1, fs=100e3, fibertype="hsr", powerlaw="approx", noisetype="fresh")
```
