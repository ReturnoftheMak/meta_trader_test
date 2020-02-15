#%% Package imports

import MetaTrader5 as mt5


#%% Connection functions

def connect():
    """Connect and print relevant connection information to terminal

    Args:
        None

    Return:
        None
    """

    # Expected return true for both functions
    mt5.initialize()
    mt5.wait()

    # request connection status and parameters as a tuple
    terminal_info = mt5.terminal_info()
    """
    if terminal_info[0] == 2:
        print('the terminal has connected to the trade server')
    elif terminal_info[0] == 0:
        print('no connection')
    elif terminal_info[0] == 1:
        print('the terminal has connected, but the trading environment has not yet been synchronized')

    print('Trade server name: ' + str(terminal_info[1]))

    print('Trading account (login) index: ' + terminal_info[2])

    # get data on MetaTrader 5 version
    version = mt5.version()

    print('MetaTrader 5 terminal version: ' + str(version[0]))
    print('Build: ' + str(version[1]))
    print('Build release date: ' + str(version[2]))
    """

def disconnect():
    """Disconnect from server, returns True

    Args:
        None

    Returns:
        None
    """

    mt5.shutdown()
    print('Disconnected from server')

    pass

#%%
