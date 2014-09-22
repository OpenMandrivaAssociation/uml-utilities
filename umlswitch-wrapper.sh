#!/bin/bash

exec /usr/bin/uml_switch ${TAP:+-tap $TAP} ${SOCKET:+-unix $SOCKET} ${OPTIONS} < /dev/null > /dev/null &
