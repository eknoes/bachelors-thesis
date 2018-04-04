obj-m+=macsec.o
MY_CFLAGS += -g -DDEBUG
ccflags-y += ${MY_CFLAGS}
CC += ${MY_CFLAGS}

all:
	make -C /usr/lib/modules/$(shell uname -r)/build M=$(PWD) modules

clean:
	make -C /usr/lib/modules/$(shell uname -r)/build M=$(PWD) clean

install:
	sudo modprobe -r macsec
	sudo insmod macsec.ko
	sudo macsec-conf.sh
