#!/bin/bash
echo "folderpath: $1";
echo "livetime: $2";
echo "filename: $3";
echo "function: $4";
sudo `which python3` /mnt/c/Users/XCF/Desktop/CrisPy/onWsl/sddMeasure.py -path $1 -time $2 -name $3 -function $4
echo  $4 >> /mnt/c/Users/XCF/Desktop/CrisPy/onWsl/logbook.txt;
echo  $1 >> /mnt/c/Users/XCF/Desktop/CrisPy/onWsl/logbook.txt;
echo  $2 >> /mnt/c/Users/XCF/Desktop/CrisPy/onWsl/logbook.txt;
echo  $3 >> /mnt/c/Users/XCF/Desktop/CrisPy/onWsl/logbook.txt;
