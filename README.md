# Introduction
PyZBC2014 is a barebones Python wrapper around the Zilany, Bruce, and Carney (2014)
auditory-nerve model, which is written in C/Mex. It relies on copies of the original C code
that have been modified to remove Mex-specific components. Otherwise, it should behave in 
nearly identical ways to the original Mex wrappers, providing the model functions
`model_IHC` to simulate IHC responses and `model_Synapse` to simulate the auditory nerve.

# Install
To install PyZBC2014, first install this package with pip from GitHub. To do so, in any
terminal that can call your preferred copy of `pip`, run the following:

``` pip install pip@git+https://github.com/guestdaniel/PyZBC2014```

Next, compile the `.c` files that are bundled with the package by navigating to the `model`
folder and running the following code for GCC (or equivalent code, based on your C
compiler):

### Windows
```
gcc -c -Wall -fPIC -O3 complex.c 
gcc -c -Wall -fPIC -O3 model_IHC.c
gcc -c -Wall -fPIC -O3 model_Synapse.c
gcc -shared -o libzbc2014.so complex.o model_IHC.o model_Syanpse.o
```

### Mac
```
gcc -c -Wall -fPIC -O3 complex.c 
gcc -c -Wall -fPIC -O3 model_IHC.c
gcc -c -Wall -fPIC -O3 model_Synapse.c
gcc -shared -o libzbc2014.so complex.obj model_IHC.obj model_Syanpse.obj
```

# Build
If you want to modify the package itself, you will need to make your modifications and then
build the package from source by running the following in a shell with the current working 
directory set to this folder:

``py -m build``