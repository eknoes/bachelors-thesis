# Test environment for MACsec implementation

While developing, I used this test environment to easily build virtual machines and automatically configure MACsec.
Therefore, [Vagrant](https://vagrantup.com) is used.

Two virtual machines `vbox1`and `vbox2` are built, each gets an additional virtual network interface for the secure communication.

Each has the current implementation available in the `/vagrant/macsec` folder, which is linked to the folder of the implementation.

A script which configures a MACsec interface with a Secure Association to the other VM is generated and put into `/macsec-conf.sh`

A script to install [KEDR](https://github.com/euspectre/kedr), a tool to detect memory leaks while developing kernel modules, can be added to the provisioning easily.

## Dependencies
* [vagrant-reload](https://github.com/aidanns/vagrant-reload) Plugin to have a reboot as a provisioning step
