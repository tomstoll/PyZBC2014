# Step 1: Compile model.c, complex.c, with warnings (-Wall), position independent 
# code (-fPIC), and optimization level three (-O3)
gcc -c -Wall -fPIC -O3 complex.c 
gcc -c -Wall -fPIC -O3 model_IHC.c
gcc -c -Wall -fPIC -O3 model_Synapse.c

# Step 2: Compile resulting objects together into a shared library 
gcc -shared -o libzbc2014.so complex.o model_IHC.o model_Synapse.o