from enum import IntEnum, Enum

class TradeCmd(IntEnum):
    BUY = 0             # buy
    SELL = 1            # sell
    BUY_LIMIT = 2       # buy limit
    SELL_LIMIT = 3      # sell limit
    BUY_STOP = 4        # buy stop
    SELL_STOP = 5       # sell stop
    BALANCE = 6         # Read only. Used in getTradesHistory for manager's deposit/withdrawal operations (profit>0 for deposit, profit<0 for withdrawal).
    CREDIT = 7          # Read only

class TradeType(IntEnum):
    OPEN = 0            # order open, used for opening orders
    PENDING = 1         # order pending, only used in the streaming getTrades command
    CLOSE = 2           # order close
    MODIFY = 3          # order modify, only used in the tradeTransaction command
    DELETE = 4          # order delete, only used in the tradeTransaction command

class TradeStatus(IntEnum):
    """ requestStatus """
    ERROR = 0           # error
    PENDING = 1         # pending
    ACCEPTED = 3        # The transaction has been executed successfully
    REJECTED = 4        # The transaction has been rejected
    
class TradeState(Enum):
    MODIFIED = "Modified"   # modified
    DELETED = "Deleted"     # deleted
    
class TradeDay(IntEnum):
    MONDAY = 1
    TUESDAY = 2
    WEDNESDAY = 3
    THURSDAY = 4
    FRIDAY = 5
    SATURDAY = 6
    SUNDAY = 7

class PriceLevel(IntEnum):
    ALL_AVAILABLE_LEVELS = -1 # -1 All available levels
    BASE_LEVEL = 0 # 0 Base level bid and ask price for instrument
    SPECIFIED_LEVEL = 1 # >0 Specified level

class PeriodCode(IntEnum):
    PERIOD_M1 = 1       # 1 minute
    PERIOD_M5 = 5       # 5 minutes
    PERIOD_M15 = 15     # 15 minutes
    PERIOD_M30 = 30     # 30 minutes
    PERIOD_H1 = 60      # 60 minutes (1 hour)
    PERIOD_H4 = 240     # 240 minutes (4 hours)
    PERIOD_D1 = 1440    # 1440 minutes (1 day)
    PERIOD_W1 = 10080   # 10080 minutes (1 week)
    PERIOD_MN1 = 43200  # 43200 minutes (30 days)

class QuoteId(Enum):
    Fixed = 1           # Fixed
    Float = 2           # Float
    Depth = 3           # Depth
    Cross = 4           # Cross
    Unknown_5 = 5
    Unknown_6 = 6
    
class MarginMode(Enum):
    Forex = 101
    CFD_Leveraged = 102
    CFD = 103
    Unknown = 104
    
class ProfitMode(Enum):
    Forex = 5
    CFD = 6
    
    
class TimeInt(IntEnum):
    HOURS = 3600000
    DAYS  = 86400000
    WEEKS = 604800000
    MONTHS = 2629743000
    YEARS = 31556926000