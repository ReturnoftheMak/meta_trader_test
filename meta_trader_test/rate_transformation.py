#%% Package imports

from datetime import datetime
import pandas as pd
from pytz import timezone
utc_tz = timezone('UTC')


#%% Convert rates tuple to DataFrame

def convert_rate_tuple(rates):
    """Converts the tuple received from server into a dataframe
    """

    data = {'time':[x.time.astimezone(utc_tz) for x in rates],
            'open':[x.open for x in rates],
            'close':[x.close for x in rates],
            'high':[x.high for x in rates],
            'low':[x.low for x in rates],
            'tick_volume':[x.tick_volume for x in rates],
            'spread':[x.spread for x in rates],
            'real_volume':[x.real_volume for x in rates]
            }

    df = pd.DataFrame(data)

    df.set_index('time', inplace=True)

    return df


#%%
