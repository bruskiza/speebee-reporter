#!/bin/ash
while :
do
  DATE=`date +%F`

  # If not specified... set the timer to an hour.
  cd /app/
  export FLASK_APP=reporter.py
  export FLASK_ENVIRONMENT=development
  flask run --host=0.0.0.0
done
