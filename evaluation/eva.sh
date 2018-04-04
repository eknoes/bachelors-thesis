#!/bin/bash

EVA_DIR=eva
FPREFIX=$(date +%s)
DEST_IP=1.1.1.2
REMOTE_IP=192.168.10.2
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

init() {
    if [ ! -d "$EVA_DIR" ]; then
        mkdir $EVA_DIR
    fi
    init_remote
}

init_remote() {
    echo -e "${GREEN}Init Remote${NC}"
    remote_cmd "killall -q iperf3"
    remote_cmd "nohup iperf3 -s > /dev/null 2>&1 &"
}

make_info() {
  echo -e "${GREEN}Write current info"
  INFO_FILE=$EVA_DIR/final-$FPREFIX-$1-$2.info

  tc qdisc > $INFO_FILE
	ip link show macsec0 >> $INFO_FILE
	ip link show eno1 >> $INFO_FILE
	ip macsec show >> $INFO_FILE
}

eva_iperf() {
    echo -e "${GREEN}Start Bandwith Evaluation of $2 with MTU $3${NC}"
    BANDWIDTH_FILE=$EVA_DIR/final-$FPREFIX-$2-$3-iperf.json

    echo -n "[" > $BANDWIDTH_FILE # Clear file

    for i in `seq 1 $1`; do
        echo -e "Start iperf3 #$i"
        timeout 20 iperf3 -Jc $4 >> $BANDWIDTH_FILE
        #iperf3 -c 1.1.1.1 -b 0
        if [ $? -ne 0 ]; then
            echo -e "${RED}iperf3 error${NC}"
            #exit 1
        fi

        if [ $1 -eq $i ]; then
            echo -ne "]" >> $BANDWIDTH_FILE
        else
            echo -ne "," >> $BANDWIDTH_FILE
        fi;
    done
}

eva_ping() {
  echo -e "${GREEN}Start RTT Evaluation of $1 with MTU $2${NC}"
  PING_FILE=$EVA_DIR/final-$FPREFIX-$1-$2-ping.txt

  timeout 360 ping -A $3 -c 50000 -s $((( $2 - 28 ))) > $PING_FILE
}

config() {
    echo -e "${GREEN}Configure local eno1 MTU $2${NC}"
    ip link set dev eno1 mtu $2

    if [ $? -ne 0 ]; then
        echo -e "${RED}Could not set MTU${NC}"
        exit 1
    fi

    echo -e "${GREEN}Configure local macsec MTU $1${NC}"
    /macsec-conf.sh
    ip link set dev macsec0 mtu $1

    if [ $? -ne 0 ]; then
        echo -e "${RED}Could not set MTU${NC}"
        exit 1
    fi

    echo -e "${GREEN}Configure remote MTU $2 / $1${NC}"
    remote_cmd "ip link set dev eno1 mtu $2; /macsec-conf.sh; ip link set dev macsec0 mtu $1"
}

load_orig() {
    echo -e "${GREEN}Load Original local${NC}"
    modprobe -r macsec
    modprobe macsec

    load_orig_remote
}

load_orig_remote() {
    echo -e "${GREEN}Load Original Remote${NC}"
    remote_cmd "modprobe -r macsec; modprobe macsec"
}

load_frag_macsec() {
    echo -e "${GREEN}Load Fragmentation local${NC}"
    modprobe -r macsec
    make
    insmod macsec.ko
    if [ $? -ne 0 ]; then
        echo -e "${RED}Could not insert macsec module${NC}"
        exit 1
    fi

    load_frag_macsec_remote
}

load_frag_macsec_remote() {
    echo -e "${GREEN}Load Fragmentation Remote${NC}"
    remote_cmd "modprobe -r macsec; cd /root/macsec; make; insmod macsec.ko;"
}

remote_cmd() {
    ssh root@$REMOTE_IP "$@"
}

eva() {
  config $3 $4

  if [[ $5 == m ]]; then
    IP=$DEST_IP
    make_info $2 $3
    eva_ping $2 $3 $IP
    eva_iperf $1 $2 $3 $IP

  else
    IP=$REMOTE_IP
    make_info $2 $4
    eva_ping $2 $4 $IP
    eva_iperf $1 $2 $4 $IP
  fi

}

init
load_orig
eva $1 "no-macsec" 1000 1468
eva $1 "no-macsec" 1000 1500
eva $1 "no-macsec" 1000 2936
eva $1 "orig" 1468 1500 m
eva $1 "orig-jumbo" 1500 9000 m
eva $1 "orig-jumbo" 2936 9000 m
load_frag_macsec
eva $1 "frag" 2936 1500 m
eva $1 "frag" 1500 1500 m
eva $1 "frag" 1468 1500 m

echo -e "${GREEN}FINISHED${NC} $FPREFIX"
