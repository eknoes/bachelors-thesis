#  Evaluation
The scripts for the evaluation evolved over time, which can be noticed easily as there was no time for polishing in the end.
The raw measurements I made are available in `raw/encrypted`.

## Make measurements
Measurements are made with `eva.sh n`, n is the number of bandwidth tests that should be made.
The script runs on one machine and logs into the other machine for configuration via SSH, therefore exchanged SSH keys are needed.

`init` creates the directory to save the raw measurements and starts an iperf3 server on the remote machine.
`load_orig` and `load_frag_macsec` insert the "original" kernel module or the modified module on both machines.
`eva $1 "no-macsec" 1000 1468` The eva function takes 5 arguments.
The first one is the number of bandwidth tests that should be made.
Then the name of the configuration follows, under which the results are saved.
The next one is the MTU that should be set for the MACsec interface, after that the Ethernet MTU follows.
If the last one is "m", the MACsec interface is used for bandwidth testing, otherwise MACsec is not used.
Then bandwidth and RTT measurements are made for the configuration and an info file containing the current configuration is created.

Currently the script makes measurements for MTUs of 1468, 1500 and 2936 with Ethernet, MACsec and the modified MACsec.

## Draw Graphics & Stuff
Graphics can be generated with `eva.py` and `gen_rtt.py`.
Both scripts create graphics using [matplotlib]() which are really made for my results and my thesis, nothing fancy.

`eva.py` generates Boxplots for the CPU measurements during the bandwidth tests and the bandwidth test, `gen_rtt.py` for the round trip time.
