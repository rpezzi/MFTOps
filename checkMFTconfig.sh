# Use
# * For logfiles located in folder ./mftcom1/logs ; ./mftcom2/logs ; ...   use
# $0 hx-dx
#     example: $0 h0-d4
#
# * To seach for the latest corrurent of a patter on a given folder use
# $0 pattern -d path_name
#
# By default the script will use the most recent file containing the provided pattern.
# Older occurences can be spotted by using option -c. Example
# $0 h0-d4 -c 4
#


PATTERN=$1
shift 1
COUNT=1
FOLDER=""

while [ $# -gt 0 ] ; do
    case $1 in
	-d)
	    FOLDER="$2";
	    shift 2
	    ;;
	-c)
  	    COUNT="$2";
	    shift 2
	    ;;
    esac
done





getLogForHalfDisk () {
    SELECTEDFILE=""
    COUNT=${COUNT:-1}

    if ! [ -z ${FOLDER+x} ]; then
    case $1 in
	h0-d0|h1-d4)
	    FOLDER="mftcom1/logs";
	    ;;
	h0-d1|h1-d3)
	    FOLDER="mftcom2/logs";
	    ;;
	h0-d2|h1-d2)
	    FOLDER="mftcom3/logs";
	    ;;
	h0-d3|h1-d1)
	    FOLDER="mftcom4/logs";
	    ;;
	h0-d4|h1-d0)
	    FOLDER="mftcom5/logs";
	    ;;
    esac
    fi

#echo $FOLDER
    for FILE in `ls -t ${FOLDER}/*.log`
    do
	if [[ `grep $PATTERN ${FILE}` != "" ]]
	then
 	    ((COUNT--))


	    if [ $COUNT -eq 0 ];
	    then
		SELECTEDFILE=$FILE
		echo ${SELECTEDFILE}
		break
	    fi
	fi
    done
}



showWarningsErrors () {
RED='\033[0;31m'
ORANGE='\033[0;33m'
PURPLE='\033[0;35m'
GREEN='\033[0m' # No Color
NC='\033[0m' # No Color

if [[ ${1} != "" ]]
then
  grep --color -E "ERROR|WARNING|CRITICAL|Set Clocks"  ${1} > .tempMSG
  grep --color -E -A 2 "xcku FAILED"  ${1} >> .tempMSG

  cat .tempMSG | \
  grep -v "Failed to connect to session ecs"  | \
  grep -v "Mismatch in GBT packers TRIGGER_READ:"  | \
  grep -v "Found no HB Accepted"  | \
	sed "s/WARNING/$(printf "${ORANGE}WARNING${NC}")/g" | \
	sed "s/ERROR/$(printf "${RED}ERROR${NC}")/g" | \
	sed "s/Set Clocks/$(printf "${GREEN}Set Clocks{NC}")/g" | \
	sed "s/CRITICAL/$(printf "${PURPLE}CRITICAL${NC}")/g" | \
  sort |
	uniq
fi
}


LOGFILE=`getLogForHalfDisk $PATTERN $COUNT`
echo -e "\n\n $PATTERN    ====>   Configuration for $PATTERN on ${LOGFILE}\n"
showWarningsErrors ${LOGFILE}
