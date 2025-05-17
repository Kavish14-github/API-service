#!/bin/bash
SCRIPT_PATH=$1

NSJAIL_BIN="/usr/sbin/nsjail"
NSJAIL_CFG="/etc/nsjail.cfg"

$NSJAIL_BIN --config $NSJAIL_CFG -- /bin/python3 /tmp/script_runner.py "$SCRIPT_PATH"
