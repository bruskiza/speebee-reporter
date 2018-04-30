import os
import sys
import datetime
import pandas
from beebotte import *
import json
import logging


class SpeeBeeReport:
    @staticmethod
    def report():
        if '_SPEEBEE_API' in os.environ:
            _hostname = os.environ['_SPEEBEE_API']
        else:
            _hostname = 'api.beebotte.com'

        if '_SPEEBEE_TOKEN' in os.environ:
            _token = os.environ['_SPEEBEE_TOKEN']
        else:
            print "No token specified. We cannot post to Beebotte without it."\
                  " Please set the _SPEEBEE_TOKEN environment variable."
            sys.exit()

        if '_SPEEBEE_CHANNEL' in os.environ:
            _channel = os.environ['_SPEEBEE_CHANNEL']
        else:
            _channel = 'speebee'

        bbt = BBT(token=_token, hostname=_hostname)

        records = bbt.read(_channel, "download", limit=2000)

        m = []
        for r in records:
            m.append([
                datetime.datetime.fromtimestamp(r['ts']/1000).strftime('%c'),
                r['data'],
                r['ts']
            ])

        # df['ts'] = pd.to_datetime(df['ts'], unit='ms')
        # weekly_summary = df.groupby(df.ts.dt.week).agg(['mean', 'max', 'min'])
        df = pandas.DataFrame(data=m)

        logging.warning(df.infer_objects())
        logging.warning(records)



        fastest = df.loc[df[1] == df[1].max(), :]
        slowest = df.loc[df[1] == df[1].min(), :]

        speed_mean = df[1].mean()
        speed_std = df[1].std()

        nine_quantile = df[1].quantile(0.9)
        eight_quantile = df[1].quantile(0.8)
        seven_quantile = df[1].quantile(0.7)
        six_quantile = df[1].quantile(0.6)
        five_quantile = df[1].quantile(0.5)
        four_quantile = df[1].quantile(0.4)
        three_quantile = df[1].quantile(0.3)
        two_quantile = df[1].quantile(0.2)
        one_quantile = df[1].quantile(0.1)

        fastest_date = fastest[0].tolist()[0]
        fastest_speed = fastest[1].tolist()[0]
        slowest_date = slowest[0].tolist()[0]
        slowest_speed = slowest[1].tolist()[0]

        samples = df.count().tolist()[0]

        return_data = {
            'records': records,
            'quantiles': {
                1: one_quantile,
                2: two_quantile,
                3: three_quantile,
                4: four_quantile,
                5: five_quantile,
                6: six_quantile,
                7: seven_quantile,
                8: eight_quantile,
                9: nine_quantile
            },
            'samples': samples,
            'mean': round(speed_mean, 2),
            'fastest': {
                'date': fastest_date,
                'speed': fastest_speed
            },
            'slowest': {
                'date': slowest_date,
                'speed': slowest_speed
            },
            'df': df,
            'm': m,
            'std': speed_mean,
            # 'weekly_summary': weekly_summary
        }

        return return_data
