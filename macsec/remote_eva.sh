scp macsec.c macsec1:macsec/macsec.c
scp macsec.c macsec2:macsec/macsec.c
ssh macsec1 "cd macsec; ./eva.sh $1"
