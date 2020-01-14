#%% Package imports

from MetaTrader5 import MT5Initialize, MT5WaitForTerminal, MT5TerminalInfo, MT5Version, MT5Shutdown


#%% Connection functions

def connect():
    """Connect and print relevant connection information to terminal

    Args:
        None

    Return:
        None
    """

    # Expected return true for both functions
    MT5Initialize()
    MT5WaitForTerminal()

    # request connection status and parameters as a tuple
    terminal_info = MT5TerminalInfo()

    if terminal_info[0] == 2:
        print('the terminal has connected to the trade server')
    elif terminal_info[0] == 0:
        print('no connection')
    elif terminal_info[0] == 1:
        print('the terminal has connected, but the trading environment has not yet been synchronized')

    print('Trade server name: ' + terminal_info[1])

    print('Trading account (login) index: ' + terminal_info[2])

    # get data on MetaTrader 5 version
    version = MT5Version()

    print('MetaTrader 5 terminal version: ' + str(version[0]))
    print('Build: ' + str(version[1]))
    print('Build release date: ' + str(version[2]))


def disconnect():
    """Disconnect from server, returns True

    Args:
        None

    Returns:
        None
    """

    MT5Shutdown()
    print('Disconnected from server')

    pass

#%%
