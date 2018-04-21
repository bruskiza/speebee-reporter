#!/bin/ash
while :
do
  DATE=`date +%F`
  
  # If not specified... set the timer to an hour.
  TIMER=${_SPEEBEE_TIMER:-3600}
  /app/bin/reporter.py
  echo -n `date`
  echo " Report completed... sleeping for $TIMER seconds..."
  sleep $TIMER
done
