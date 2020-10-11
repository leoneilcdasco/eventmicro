#!/bin/bash

if [ -n "$VIRTUAL_ENV" ]; then
  echo "Please deactivate virtual environment first and re-run script."
  exit 1
fi

case "$1" in
start)
   echo "Starting web service..."
   systemctl start gunicorn.socket
   ;;
stop)
   echo "Stopping web service..."
   systemctl stop gunicorn.socket
   ;;
restart)
   systemctl daemon-reload
   $0 stop
   $0 start
   ;;
status)
   sudo systemctl status gunicorn.socket
   echo "-----------------"
   file /run/gunicorn.sock
   ;;
*)
   echo "Usage: $0 {start|stop|status|restart}"
esac

exit 0