cd /tmp
git clone https://github.com/euspectre/kedr.git
cd kedr
cmake sources/ -DKEDR_TRACE=OFF
make && make install
