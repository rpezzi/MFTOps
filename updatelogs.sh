updatelogs () {
rsync -a mftcom1:mft-ru-cru/software/testbench/logs mftcom1/ && echo mftcom1 OK || echo mftcom1 failed
rsync -a mftcom2:mft-ru-cru/software/testbench/logs mftcom2/ && echo mftcom2 OK || echo mftcom2 failed
rsync -a mftcom3:mft-ru-cru/software/testbench/logs mftcom3/ && echo mftcom3 OK || echo mftcom3 failed
rsync -a mftcom4:mft-ru-cru/software/testbench/logs mftcom4/ && echo mftcom4 OK || echo mftcom4 failed
rsync -a mftcom5:mft-ru-cru/software/testbench/logs mftcom5/ && echo mftcom5 OK || echo mftcom5 failed
}

updatelogs
