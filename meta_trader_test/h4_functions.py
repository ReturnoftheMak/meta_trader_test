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


# %% Conversion function

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
    rates = mt5.copy_rates_from_pos(currency, timeframe, 0, periods)

    df = pd.DataFrame(rates)

    # Localize to UTC from ns-epoch
    df.time = df.time.apply(datetime.fromtimestamp).dt.tz_localize(utc_tz)

    # Resets the index for calculations
    df.set_index('time', inplace=True)

    return df


# %% Get df

df = rates_to_dataframe('EURUSD', mt5.TIMEFRAME_D1, 2000)



# %% What we actually need is to give a date and return info about that day
# For a given day, a function for the 3/6 month prior date or closest
# Get the D1 timeframe data for that given day

# We do need to check if there is any data for the date we check,
# but that doesn't need to be done by the first function
# Can implement a relativedelta function with recursion to get the date we want

# Thankfully selecting a weekend date simply returns the latest D1 data, 
# So we'll keep this behaviour

def get_preceding_weekday(date, n):
    """Get the date for the relevant day n months prior

    Params:
        date (pandas._libs.tslibs.timestamps.Timestamp): date in question
        n (int): number of months
    
    Returns:
        date to pass (pandas._libs.tslibs.timestamps.Timestamp)
    """

    check_date = date + relativedelta(months=-n)

    return check_date


def daily_timeframe_data(currency, date):
    """Returns a single days data
    """

    rates = mt5.copy_rates_from(currency, mt5.TIMEFRAME_D1, date, 1)

    df = pd.DataFrame(rates)
    df.time = df.time.apply(datetime.fromtimestamp).dt.tz_localize(utc_tz)

    df.set_index('time', inplace=True)

    return df


# %%

rate_dict_3 = daily_timeframe_data('EURUSD', get_preceding_weekday(df.index[-1], 3))
rate_dict_6 = daily_timeframe_data('EURUSD', get_preceding_weekday(df.index[-1], 6))


# %% Write func to get tick data for a given day

def get_ticks_for_day(currency, date):
    """Get all the ticks for a given day
    """

    to_date = date + relativedelta(days=1)

    ticks = mt5.copy_ticks_range(currency, date, to_date, mt5.COPY_TICKS_ALL)

    df = pd.DataFrame(ticks)
    df.time = df.time.apply(datetime.fromtimestamp).dt.tz_localize(utc_tz)

    df.set_index('time', inplace=True)

    return df


# %% Backtesting

