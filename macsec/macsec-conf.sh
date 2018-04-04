ip link show | grep macsec0 > /dev/null

if [ $? -eq  0 ]
then
  ip link delete macsec0
fi

# Create the MACsec device on top of the physical one
ip link add link eno1 macsec0 type macsec

# Configure the Transmit SA and keys
ip macsec add macsec0 tx sa 0 pn 100 on key 01 11111111111111111111111111111111

# Configure the Receive Channel and SA:
# MAC address of the peer
# port number, packet number and key
ip macsec add macsec0 rx address ec:b1:d7:4b:bd:01 port 1
ip macsec add macsec0 rx address ec:b1:d7:4b:bd:01 port 1 sa 0 pn 100 on key 02 22222222222222222222222222222222

# Bring up the interface
ip link set dev eno1 up
ip link set dev macsec0 up

# Configure an IP address on it for connectivity between the hosts
ip addr add 1.1.1.1/24 dev macsec0
