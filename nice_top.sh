
PID=$1
FIRST=true
NSKIP=12
OUTPUT_FILE=top_output2.txt
while true
do

    echo "top -pid $PID -l 1|tail -n +$NSKIP >> $OUTPUT_FILE"
    TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")
    top -pid $PID -l 1 | tail -n +$NSKIP | sed "s/$/ $TIMESTAMP/" >> $OUTPUT_FILE

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