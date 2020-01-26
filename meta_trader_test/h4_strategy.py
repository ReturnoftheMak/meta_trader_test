#%% Package imports

from datetime import datetime
from dateutil.relativedelta import relativedelta
from MetaTrader5 import MT5CopyRatesFromPos, MT5_TIMEFRAME_D1, MT5_TIMEFRAME_H4, MT5CopyTicksRange
from pytz import timezone
from rate_transformation import convert_rate_tuple
from connections import connect, disconnect
utc_tz = timezone('UTC')


#%% Looking at 4 Majors

# Our trigger for the higher timeframe is the current price being higher
# than the price 3 months ago and 6 months ago

def high_timeframe_check(currency):
    """Checks the condition using D1 candles for given currency.
    The condition in this case is the current price being lower/higher 
    than both 3 and 6 months prior.

    Args:
        currency (str): Name of the currency pair
    
    Returns:
        tuple of 2 booleans for condition passes, short and long
    """

    x = MT5CopyRatesFromPos(currency, MT5_TIMEFRAME_D1, 0, 200)

    df = convert_rate_tuple(x)

    latest_date = df.index.max()

    # This gives the latest date, from which we will find the timestamp
    # for 3 and 6 months prior, and use this to return the indices for
    # the required rows. It should be noted that weekday only trading
    # will mean we need to get to the weekday preceding the 3/6 month

    def get_preceding_weekday(latest_date, month_delta, df):
        """Get the date for the relevant day 6 months prior
        """

        check_date = latest_date + relativedelta(months=-month_delta)

        while len(df[str(check_date).split(' ')[0]]) < 1:
            check_date += relativedelta(days=-1)

        return check_date

    check_3_month = get_preceding_weekday(latest_date, 3, df)
    check_6_month = get_preceding_weekday(latest_date, 6, df)

    # Get the row using the timestamp with the index
    df_3month = df[str(check_3_month).split(' ')[0]]
    df_6month = df[str(check_6_month).split(' ')[0]]
    df_current = df[str(latest_date).split(' ')[0]]

    # Check the logic for this pair

    # Short entry
    low_3month = df_3month.low.min()
    low_6month = df_6month.low.min()
    current = df_current.close.min()

    short_condition = current < low_3month and current < low_6month

    # Long entry
    high_3month = df_3month.high.max()
    high_6month = df_6month.high.max()
    current = df_current.close.max()

    long_condition = current > high_3month and current > high_6month

    # How do I know there's a close on the current price?
    # Maybe use the ticks for latest

    return short_condition, long_condition


#%%

connect()

usdchf_rates_check = high_timeframe_check("USDCHF")

usdjpy_rates_check = high_timeframe_check("USDJPY")

eurusd_rates_check = high_timeframe_check("EURUSD")

gbpusd_rates_check = high_timeframe_check("GBPUSD")


#%% Now we need to look at the lower timeframe

# Two cases, one for long and one for short

def lower_time_frame_short(currency):
    """Evaluates a short condition for the H4 timeframe,
    whether the latest wick is the highest of the last 6

    Args:
        currency (str): Name of the currency pair
    
    Return:
        boolean whether condition is met
    """

    x = MT5CopyRatesFromPos(currency, MT5_TIMEFRAME_H4, 0, 6)

    df = convert_rate_tuple(x)

    latest_date = df.index.max()

    # condition - latest wick is highest of last 6

    highest_wick = df.high.max()

    latest_candle = df.loc[str(latest_date)]

    short_condition = latest_candle.high == highest_wick

    return short_condition, latest_candle


def lower_time_frame_long(currency):
    """Evaluates a long condition for the H4 timeframe,
    whether the latest wick is the lowest of the last 6

    Args:
        currency (str): Name of the currency pair
    
    Return:
        boolean whether condition is met
    """

    x = MT5CopyRatesFromPos(currency, MT5_TIMEFRAME_H4, 0, 6)

    df = convert_rate_tuple(x)

    latest_date = df.index.max()

    # condition - latest wick is lowest of last 6

    lowest_wick = df.low.min()

    latest_candle = df.loc[str(latest_date)]

    long_condition = latest_candle.low == lowest_wick

    return long_condition, latest_candle, latest_date


#%% Entry conditions, differ based on long/short

# For this we'll need tick data

def short_entry(currency, latest_candle, latest_date):
    """Docstring
    """

    date_start = latest_date + relativedelta(hours=4)
    date_end = latest_date + relativedelta(hours=8)

    ticks = MT5CopyTicksRange(currency,
                              datetime(date_start.year, date_start.month, date_start.day, date_start.hour),
                              datetime(date_end.year, date_end.month, date_end.day, date_end.hour),
                              MT5_COPY_TICKS_ALL)
    
    # get the

