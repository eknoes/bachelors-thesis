#!/usr/bin/env bash
# Check for macsec
echo "ip link show | grep macsec0 > /dev/null

if [ $? -eq  0 ]
then
  sudo ip link delete macsec0
fi

# Create the MACsec device on top of the physical one
sudo ip link add link eth1 macsec0 type macsec

# Configure the Transmit SA and keys
sudo ip macsec add macsec0 tx sa 0 pn 100 on key 01 $MY_KEY

# Configure the Receive Channel and SA:
# MAC address of the peer
# port number, packet number and key
sudo ip macsec add macsec0 rx address $PARTNER_MAC port 1
sudo ip macsec add macsec0 rx address $PARTNER_MAC port 1 sa 0 pn 100 on key 02 $PARTNER_KEY

# Set MAC address
sudo ip link set dev macsec0 address $MY_MAC

# Bring up the interface
sudo ip link set dev eth1 up
sudo ip link set dev macsec0 up

# Configure an IP address on it for connectivity between the hosts
sudo ip addr add $IP/24 dev macsec0

# Set Queue
sudo tc qdisc add dev macsec0 root pfifo" > /macsec-conf.sh
chmod +x /macsec-conf.sh
