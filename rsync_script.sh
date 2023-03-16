#!/bin/bash
# piliangkaobei
# Set source and destination directories
SRC_DIR="/path/to/source"
DST_DIR="/path/to/destination"

# Set rsync options
RSYNC_OPTS="-avh --checksum --ignore-existing"

# Set log file path
LOG_FILE="/path/to/rsync.log"


# Run rsync command
rsync $RSYNC_OPTS $SRC_DIR $DST_DIR >> $LOG_FILE 2>&1

# Sleep for 5 seconds
sleep 5

