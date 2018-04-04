pacman -Syu --noconfirm
pacman -S git make gcc iperf3 gdb net-tools linux-lts linux-lts-headers --noconfirm
pacman -R linux
grub-mkconfig -o /boot/grub/grub.cfg
