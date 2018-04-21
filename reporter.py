#!/usr/bin/env python

import os
import sys
import datetime
import pandas
from beebotte import *

if '_SPEEBEE_API' in os.environ:
    _hostname = os.environ['_SPEEBEE_API']
else:
    _hostname = 'api.beebotte.com'

if '_SPEEBEE_TOKEN' in os.environ:
    _token = os.environ['_SPEEBEE_TOKEN']
else:
    print "No token specified. We cannot post to Beebotte without it. Please "\
          "set the _SPEEBEE_TOKEN environment variable."
    sys.exit()

if '_SPEEBEE_CHANNEL' in os.environ:
    _channel = os.environ['_SPEEBEE_CHANNEL']
else:
    _channel = 'speebee'

bbt = BBT(token=_token, hostname=_hostname)


records = bbt.read(_channel, "download", limit = 2000)

m = []
for r in records:
    m.append([datetime.datetime.fromtimestamp(r['ts']/1000).strftime('%c'), r['data']])

df = pandas.DataFrame(data = m)

fastest = df.loc[df[1] == df[1].max(), :]
slowest = df.loc[df[1] == df[1].min(), :]

speed_mean = df[1].mean()

nine_quantile = df[1].quantile(0.9)
eight_quantile = df[1].quantile(0.8)
seven_quantile = df[1].quantile(0.7)
six_quantile = df[1].quantile(0.6)
four_quantile = df[1].quantile(0.4)
three_quantile = df[1].quantile(0.3)
two_quantile = df[1].quantile(0.2)
one_quantile = df[1].quantile(0.1)

fastest_date = fastest[0].tolist()[0]
fastest_speed = fastest[1].tolist()[0]
slowest_date = slowest[0].tolist()[0]
slowest_speed = slowest[1].tolist()[0]

samples = df.count().tolist()[0]

report = "SPEEBEE WEATHER REPORT"
report +="\n----------------------\n"

report += "\nChannel: %s\n\n" % _channel

report += "WARNING! These stats have not been fully VERIFIED!\n"
report += "USE AT YOUR OWN RISK!\n"

report += "\nNumber of samples: %s" % samples
report += "\nThe FASTEST speed was on %s and it was %s " % (fastest_date, fastest_speed)
report += "\nThe SLOWEST speed was on %s and it was %s" % (slowest_date, slowest_speed)


report += "\n\nAverage speed: %s" % speed_mean

report += "\n\nStandard deviation: %s" % df[1].std()

report += "\n\n1/10 times we will go: %s or faster" % nine_quantile

report += "\n3/10 times we will go: %s or faster" % seven_quantile
report += "\n4/10 times we will go: %s or faster" % six_quantile
report += "\n6/10 times we will go: %s or faster" % four_quantile
report += "\n7/10 times we will go: %s or faster" % three_quantile
report += "\n8/10 times we will go: %s or faster" % two_quantile
report += "\n9/10 times we will go: %s or faster" % one_quantile

print report

report_five = "\n"
report_five += "\n1/5 times we will go: %s or faster" % eight_quantile
report_five += "\n3/5 times we will go: %s or faster" % four_quantile
report_five += "\n4/5 times we will go: %s or faster" % two_quantile

print report_five
