


# This is a command to see what things are running before you get the PID:
# top -l 1| grep Python
# Or replace Python with whatever command you want to run
# Or for linux:
# top -b -n 1 | grep python
PID=$1
FIRST=true
OUTPUT_FILE=top_output2.txt
SYS=LINUX
if [ $SYS = "MAC" ]; then
  TOPCMD=(top -pid $PID -l 1 -stats 'pid,command,cpu,mem,state')
  AWKCMD=(awk '{print $0}')
  NSKIP=12
elif [ $SYS = "LINUX" ]; then
  TOPCMD=(top -p $PID -b -n 1)
  AWKCMD=(awk '{print $1,$12,$9,$10}')
  NSKIP=7
fi



while true
do
    TAILCMD=(tail -n +$NSKIP)
    TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")
    SEDCMD=(sed "s/$/ $TIMESTAMP/")

    echo "${TOPCMD[@]}|${TAILCMD[@]}|${AWKCMD[@]}|${SEDCMD[@]} >> $OUTPUT_FILE"
    "${TOPCMD[@]}"|"${TAILCMD[@]}"|"${AWKCMD[@]}"|"${SEDCMD[@]}" >> $OUTPUT_FILE
    if [ "$FIRST" = true ]; then
        NSKIP=$(( NSKIP+1 ))
        FIRST=false
    fi
    sleep 60
done



# Run top command and store the output
top_output=$(top -n 1 -b)

# Print the top output with an additional column for timestamp
echo "$top_output | Timestamp"
echo "$top_output | $timestamp"


