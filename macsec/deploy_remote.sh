scp macsec.c macsec1:macsec/macsec.c
scp macsec.c macsec2:macsec/macsec.c
ssh macsec1 "cd macsec; make && make install"
ssh macsec2 "cd macsec; make && make install"
