# %% Package imports

from datetime import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd
import MetaTrader5 as mt5
from rate_transformation import convert_rate_tuple
from connections import connect, disconnect
from pytz import timezone
utc_tz = timezone('UTC')


# %% connect and set params

connect()

currencies = ['USDCHF', 'EURUSD', 'GBPUSD', 'USDJPY']


# %% testers

def rates_to_dataframe(currency='', timeframe=0, periods=0):
    """Convert the ndarray received from copy_rates to a dataframe

    Params:
        currency (str): currency pair string
        timeframe (int): pass an mt5.TIMEFRAME_XX integer
        periods (int): number of timeframes into the past
    
    Returns:
        pandas.core.frame.DataFrame
    """

    # Use the copy_rates
    x = mt5.copy_rates_from_pos(currency, timeframe, 0, periods)

    df = pd.DataFrame(x)

    # Localize to UTC from ns-epoch
    df.time = df.time.apply(datetime.fromtimestamp).dt.tz_localize(utc_tz)

    # Resets the index for calculations
    df.set_index('time', inplace=True)

    return df


# %%

df = rates_to_dataframe('EURUSD', mt5.TIMEFRAME_D1, 2000)

