
#%% Package imports and timezone set

from datetime import datetime
from MetaTrader5 import *
from pytz import timezone
import matplotlib.pyplot as plt
utc_tz = timezone('UTC')


#%% Connect

MT5Initialize()
MT5WaitForTerminal()

# request connection status and parameters
print(MT5TerminalInfo())
# get data on MetaTrader 5 version
print(MT5Version())


#%% Get data

# request 1000 ticks from EURAUD 
euraud_ticks = MT5CopyTicksFrom("EURAUD",
                                datetime(2019, 4, 1, 0),
                                1000,
                                MT5_COPY_TICKS_ALL)

# request ticks from AUDUSD within 2019.04.01 13:00 - 2019.04.02 13:00 
audusd_ticks = MT5CopyTicksRange("AUDUSD",
                                 datetime(2019, 4, 1, 13),
                                 datetime(2019, 4, 2, 13),
                                 MT5_COPY_TICKS_ALL)


#%% Get Bars

# get bars from different symbols in a number of ways
eurusd_rates = MT5CopyRatesFrom("EURUSD",
                                MT5_TIMEFRAME_M1,
                                datetime(2019, 4, 5, 15),
                                1000)

gbpusd_rates = MT5CopyRatesFromPos("GBPUSD",
                                   MT5_TIMEFRAME_M1,
                                   0,
                                   1000)

eurjpy_rates = MT5CopyRatesRange("EURJPY",
                                 MT5_TIMEFRAME_M1,
                                 datetime(2019, 4, 1, 13),
                                 datetime(2019, 4, 2, 13))

#%% Disconnect

MT5Shutdown()


#%% Plotting

x_time = [x.time.astimezone(utc_tz) for x in euraud_ticks]
# prepare Bid and Ask arrays
bid = [y.bid for y in euraud_ticks]
ask = [y.ask for y in euraud_ticks]


#%% Draw ticks on the chart

plt.plot(x_time, ask,'r-', label='ask')
plt.plot(x_time, bid,'g-', label='bid')
# display legends 
plt.legend(loc='upper left')
# display header 
plt.title('EURAUD ticks')
# display the chart
plt.show()


#%%
