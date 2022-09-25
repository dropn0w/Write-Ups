#!/usr/bin/env bash

FLAG=$(file flag.txt)
XZ='XZ'
EMPTY='empty'
BZIP2='bzip2'
GZIP='gzip'
ZIP='Zip'
TEXT='text'


while [[ $FLAG != "flag.txt: ASCII text" ]]; do
    FLAG=$(file flag.txt)
    if grep -q "$XZ" <<< "$FLAG";then
        mv flag.txt flag.txt.xz; xz -d flag.txt.xz;
    elif grep -q "$EMPTY" <<< "$FLAG";then
        unzip -o flag.txt
    elif grep -q "$BZIP2" <<< "$FLAG";then
        mv flag.txt flag.txt.bz2; bzip2 -d flag.txt.bz2 
    elif grep -q "$GZIP" <<< "$FLAG";then
        mv flag.txt flag.txt.gz; gzip -d flag.txt.gz
    elif grep -q "$ZIP" <<< "$FLAG";then
        unzip -o flag.txt  
    else grep -q "$TEXT" <<< "$FLAG";
        cat flag.txt | base64 -d
    fi

done
