#%% Package imports

from datetime import datetime
from MetaTrader5 import MT5CopyRatesFromPos, MT5_TIMEFRAME_D1
from pytz import timezone
from rate_transformation import convert_rate_tuple
utc_tz = timezone('UTC')


#%% Looking at 4 Majors

# Our trigger for the higher timeframe is the current price being higher
# than the price 3 months ago and 6 months ago

def high_timeframe_check(currency):
    """Checks the condition using D1 candles for given currency.
    The condition in this case is the current price being higher 
    than both 3 and 6 months prior.
    """

    x = MT5CopyRatesFromPos(currency, MT5_TIMEFRAME_D1, 0, 200)

    df = convert_rate_tuple(x)

usdchf_rates = high_timeframe_check("USDCHF")

usdjpy_rates = high_timeframe_check("USDJPY")

eurusd_rates = high_timeframe_check("EURUSD")

gbpusd_rates = high_timeframe_check("GBPUSD")


#%% 