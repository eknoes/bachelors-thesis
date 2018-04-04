# Implementation
This folder contains the implementation of the fragmentation scheme in MACsec.
The file `macsec.c` is the modified MACsec kernel module, which can be built with `make` and installed with `make install`.

The makefile tries to execute the configuration script `macsec-conf.sh` when installing the module.
