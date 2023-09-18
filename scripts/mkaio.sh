ls -d modlets/a-la-carte/donovan-* >aio-modlist.txt
python3 scripts/mkbundle.py -vCb modlets/donovan-aio -m aio-modlist.txt
