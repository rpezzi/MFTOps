#!/bin/bash
if [ "$1" != "noupdate" ]; then
./updatelogs.sh
fi

checkLastConfig () {
HALFDISKS="h0-d0 h1-d4 h0-d1 h1-d3 h0-d2 h1-d2 h0-d3 h1-d1 h0-d4 h1-d0 "

for HALFDISK in $HALFDISKS
do
    ./checkMFTconfig.sh $HALFDISK
done
}
STAMP=`date +"%d.%m.%Y_%H:%M:%S_%Z"`
LOGFILE=ConfigSummary_${STAMP}.log
checkLastConfig  > $LOGFILE && less -r $LOGFILE
