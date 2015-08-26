#!/bin/bash
set -e

# set env variables
if [ -n "$NSQLOOKUPD_PORT_4161_TCP_ADDR" ] && [ -n "$NSQLOOKUPD_PORT_4161_TCP_PORT" ]; then
  export LOOKUPD_ADDRESSES="http://${NSQLOOKUPD_PORT_4161_TCP_ADDR}:${NSQLOOKUPD_PORT_4161_TCP_PORT}"
fi

echo "LOOKUPD ADDRESSES: ${LOOKUPD_ADDRESSES}"

# execute python application in unbuffered mode
exec python -u email_service.py
