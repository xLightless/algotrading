from algotrading.xtb.xapi.records import PeriodCode

## Trading Preferences
MIN_TRADING_INTRADAY_HOUR = 7 # 7am
MAX_TRADING_INTRADAY_HOUR = 20 # 8pm
OVERRIDE_TRADING_INTRADAY_RANGE = True
TRADE_PERIOD = PeriodCode.PERIOD_M15


## Backtesting
BACKTESTING = True
GET_NEW_HISTORICAL_DATA = False
BACKTEST_CANDLES = 30000


# The maximum spread we will allow for entering trades.
MAX_ENTRY_SPREAD = 5


## Indicators
TOGGLE_INDICATORS = True

## RSI SETTINGS
RSI_PERIOD = 14
RSI_UPPER_BAND = 70
RSI_LOWER_BAND = 30

## EMA
EMA_M15_CHART_PERIOD1 = 5
EMA_M15_CHART_PERIOD2 = 20
EMA_M15_CHART_PERIOD3 = 50



## Log verbose information to console.
VERBOSE = True
PURGE_BACKTESTING_DATA = False