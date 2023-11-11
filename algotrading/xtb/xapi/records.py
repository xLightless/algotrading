from dataclasses import dataclass
from .enums import *
from .request import *
from typing import Optional
import datetime

@dataclass
class SymbolRecord:
    def __init__(
        self,
        ask: float,                  # Ask price in base currency
        bid: float,                  # Bid price in base currency
        categoryName: str,           # Category name
        contractSize: int,           # Size of 1 lot
        currency: str,               # Currency
        currencyPair: bool,          # Indicates whether the symbol represents a currency pair
        currencyProfit: str,         # The currency of calculated profit
        description: str,            # Description
        groupName: str,              # Symbol group name
        high: float,                 # The highest price of the day in base currency
        initialMargin: int,          # Initial margin for 1 lot order used for profit/margin calculation
        instantMaxVolume: int,       # Maximum instant volume multiplied by 100 (in lots)
        leverage: float,             # Symbol leverage
        longOnly: bool,              # Long only
        lotMax: float,               # Maximum size of trade
        lotMin: float,               # Minimum size of trade
        lotStep: float,              # A value of minimum step by which the size of trade can be changed (within lotMin - lotMax range)
        low: float,                  # The lowest price of the day in base currency
        marginHedged: int,           # Used for profit calculation
        marginHedgedStrong: bool,    # For margin calculation
        marginMaintenance: int,      # For margin calculation null if not applicable
        marginMode: MarginMode,      # For margin calculation
        percentage: float,           # Percentage
        pipsPrecision: int,          # Number of symbol's pip decimal places
        precision: int,              # Number of symbol's price decimal places
        profitMode: ProfitMode,      # For profit calculation
        quoteId: QuoteId,            # Source of price
        quoteIdCross: int,
        shortSelling: bool,          # Indicates whether short selling is allowed on the instrument
        spreadRaw: float,            # The difference between raw ask and bid prices
        spreadTable: float,          # Spread representation
        stepRuleId: int,             # Appropriate step rule ID from getStepRules  command response
        stopsLevel: int,             # Minimal distance (in pips) from the current price where the stopLoss/takeProfit can be set
        swap_rollover3days: int,     # Time when additional swap is accounted for weekend
        swapEnable: bool,            # Indicates whether swap value is added to position on end of day
        swapLong: float,             # Swap value for long positions in pips
        swapShort: float,            # Swap value for short positions in pips
        swapType: int,               # Type of swap calculated
        symbol: str,                 # Symbol name
        timeString: str,             # Time in string
        trailingEnabled: bool,       # Indicates whether trailing stop (offset) is applicable to the instrument.
        type: int,                   # Instrument class number
        exemode:int,                 # Mode of execution
        
        expiration: Optional[datetime.datetime] = None,  # Null if not applicable
        starting: Optional[datetime.datetime] = None,    # Null if not applicable
        tickSize: Optional[float] = None,                # Smallest possible price change, used for profit/margin calculation, null if not applicable
        tickValue: Optional[float] = None,               # Value of smallest possible price change (in base currency), used for profit/margin calculation, null if not applicable
        time: int = None                                # Ask & bid tick time. 13 long unixtime integer.
    ):
        self.ask = float = ask
        self.bid = bid
        self.categoryName = categoryName
        self.contractSize = contractSize
        self.currency = currency
        self.currencyPair = currencyPair
        self.currencyProfit = currencyProfit
        self.description = description
        self.groupName = groupName
        self.high = high
        self.initialMargin = initialMargin
        self.instantMaxVolume = instantMaxVolume
        self.leverage = leverage
        self.longOnly = longOnly
        self.lotMax = lotMax
        self.lotMin = lotMin
        self.lotStep = lotStep
        self.low = low
        self.marginHedged = marginHedged
        self.marginHedgedStrong = marginHedgedStrong
        self.marginMaintenance = marginMaintenance
        self.marginMode = marginMode
        self.percentage = percentage
        self.pipsPrecision = pipsPrecision
        self.precision = precision
        self.profitMode = profitMode
        self.quoteId = quoteId 
        self.quoteIdCross = quoteIdCross
        self.shortSelling = shortSelling
        self.spreadRaw = float
        self.spreadTable = float
        self.stepRuleId = stepRuleId
        self.stopsLevel = stopsLevel
        self.swap_rollover3days = swap_rollover3days
        self.swapEnable = swapEnable
        self.swapLong = swapLong
        self.swapShort = swapShort
        self.swapType = swapType
        self.symbol = symbol
        self.timeString = timeString
        self.trailingEnabled = trailingEnabled
        self.type = type
        self.exemode = exemode
        
        self.expiration: Optional[datetime.datetime] = expiration
        self.starting: Optional[datetime.datetime] = starting
        self.tickSize: Optional[float] = tickSize
        self.tickValue: Optional[float] = tickValue
        self.time: int = time
    
    
@dataclass
class CalenderRecord:
    country: str                    # Two letter country code
    current: str                    # Market value (current), empty before time of release of this value (time from "time" record)
    forecast: str                   # Forecasted value
    impact: str                     # Impact on market
    period: str                     # Information period
    previous: str                   # Value from previous information release
    time: datetime.datetime         # Time, when the information will be released (in this time empty "current" value should be changed with exact released value)
    title: str                      # Name of the indicator for which values will be released
    
@dataclass
class RateInfoRecord:
    close: float                        # Value of close price (shift from open price)
    ctm: int                            # Candle start time in CET / CEST time zone (see Daylight Saving Time, DST)
    ctmString: str                      # String representation of the 'ctm' field
    high: float                         # Highest value in a given period (shift from open price)
    low: float                          # Lowest value in the given period (shift from open price)
    open: float                         # Open price (in base currency * 10 to the power of digits)
    vol: float                          # Volume in lots.

# class RateInfoRecord:
#     def __init__(self, close, ctm, ctmString, high, low, open, vol):
#         self.close = close
#         self.ctm = ctm
#         self.ctm_string = ctmString
#         self.high = high
#         self.low = low
#         self.open = open
#         self.vol = vol
    
@dataclass
class IBRecord:
    closePrice: float	                # IB close price or null if not allowed to view
    login: str 	                        # IB user login or null if not allowed to view
    nominal: float	                    # IB nominal or null if not allowed to view
    openPrice: float	                # IB open price or null if not allowed to view
    side: int                           # Operation code or null if not allowed to view
    surname: str                        # IB user surname or null if not allowed to view
    symbol: str                         # Symbol or null if not allowed to view
    timestamp: datetime.datetime        # Time the record was created or null if not allowed to view
    volume: float                       # Volume in lots or null if not allowed to view
    

@dataclass
class NewsTopicRecord:
    body: str                       # Body (typically some html body)
    bodylen: int                    # Body length
    key: str                        # News key
    time: datetime.datetime         # Time
    timeString: str                 # Time string
    title: str                      # News title
    
    
@dataclass
class StepRuleRecord:
    id: int                         # Step rule ID
    name: str                       # Step rule name
    steps: list[StepRecord]         # Array of StepRecord
    
    
@dataclass
class QuotesRecord:
    day: TradeDay                       # Day of week
    fromT: Optional[datetime.datetime]  # Start time in ms from 00:00 CET / CEST time zone (see Daylight Saving Time, DST)
    toT: Optional[datetime.datetime]    # End time in ms from 00:00 CET / CEST time zone (see Daylight Saving Time, DST)    
    
    
@dataclass
class TickRecord:
    ask: float                      # Ask price in base currency
    askVolume: int                  # Number of available lots to buy at given price or null if not applicable
    bid: float                      # Bid price in base currency
    bidVolume: int                  # Number of available lots to buy at given price or null if not applicable
    high: float                     # The highest price of the day in base currency
    level: PriceLevel               # Price level
    low: float                      # The lowest price of the day in base currency
    spreadRaw: float                # The difference between raw ask and bid prices
    spreadTable: float              # Spread representation
    symbol: str                     # Symbol
    timestamp: datetime.datetime    # Timestamp
    
    
    
@dataclass
class TradeRecord:
    close_price: float	            # Close price in base currency
    close_time: datetime.datetime   # Null if order is not closed
    close_timeString: str           # Null if order is not closed
    closed: bool                    # Closed
    cmd: TradeCmd                   # Operation code
    comment: str                    # Comment
    commission: str                 # Commission in account currency, null if not applicable
    customComment: str              # The value the customer may provide in order to retrieve it later.
    digits: int                     # Number of decimal places
    expiration: datetime.datetime   # Null if order is not closed
    expirationString: str           # Null if order is not closed
    margin_rate: float              # Margin rate
    offset: int                     # Trailing offset
    open_price: float               # Open price in base currency
    open_time: datetime.datetime    # Open time
    open_timeString: str            # Open time string
    order: int                      # Order number for opened transaction
    order2: int	                    # Order number for closed transaction
    position: int                   # Order number common both for opened and closed transaction
    profit: float                   # Profit in account currency
    sl: float                       # Zero if stop loss is not set (in base currency)
    storage: float                  # Order swaps in account currency
    symbol: str	                    # symbol name or null for deposit/withdrawal operations
    timestamp: datetime.datetime    # Timestamp
    tp: float                       # Zero if take profit is not set (in base currency)
    volume: float                   # Volume in lots

@dataclass
class TradingRecord:
    day: TradeDay               # Day of week
    fromT: datetime.datetime    # Start time in ms from 00:00 CET / CEST time zone (see Daylight Saving Time, DST)
    toT: datetime.datetime      # End time in ms from 00:00 CET / CEST time zone (see Daylight Saving Time, DST)

    
@dataclass
class TradeHoursRecord:
    quotes: list[QuotesRecord]      # Array of QuotesRecord
    symbol: str                     # Symbol
    trading: list[TradingRecord]    # Array of TradingRecord
    

@dataclass
class StreamingBalanceRecord:
    balance: float          # balance in account currency
    credit: float           # credit in account currency
    equity: float           # sum of balance and all profits in account currency
    margin: float           # margin requirements
    marginFree: float       # free margin
    marginLevel: float      # margin level percentage


@dataclass
class StreamingCandleRecord:
    close: float                        # Close price in base currency
    ctm: Optional[datetime.datetime]    # Candle start time in CET time zone (Central European Time)
    ctmString: str                      # String representation of the 'ctm' field
    high: float                         # Highest value in the given period in base currency
    low: float                          # Lowest value in the given period in base currency
    open: float                         # Open price in base currency
    quoteId: QuoteId                    # Source of price
    symbol: str                         # Symbol
    vol: float                          # Volume in lots.
    
    
@dataclass
class StreamingKeepAliveRecord:
    timestamp: int              # Current timestamp
    

@dataclass
class StreamingNewsRecord:
    body: str                       # Body (typically some html body)
    key: str                        # News key
    time: datetime.datetime         # Time
    title: str                      # News title
    

@dataclass
class StreamingProfitRecord:
    order: int      # Order number
    order2: int     # Transaction ID
    position: int   # Position number
    profit: float   # Profit in account currency
    
@dataclass
class StreamTickRecord:
    ask: float                      # Ask price in base currency
    askVolume: int                  # Number of available lots to buy at given price or null if not applicable
    bid: float                      # Bid price in base currency
    bidVolume: int                  # Number of available lots to buy at given price or null if not applicable
    high: float                     # The highest price of the day in base currency
    level: PriceLevel               # Price level
    low: float                      # The lowest price of the day in base currency
    quoteId: QuoteId                # Source of price, detailed description below
    spreadRaw: float                # The difference between raw ask and bid prices
    spreadTable: float              # Spread representation
    symbol: str                     # Symbol
    timestamp: datetime.datetime    # Timestamp
    
    
@dataclass
class StreamingTradeRecord:
    close_price: float	            # Close price in base currency
    close_time: datetime.datetime   # Null if order is not closed
    closed: bool                    # Closed
    cmd: TradeCmd                   # Operation code
    comment: str                    # Comment
    commission: str                 # Commission in account currency, null if not applicable
    customComment: str              # The value the customer may provide in order to retrieve it later.
    digits: int                     # Number of decimal places
    expiration: datetime.datetime   # Null if order is not closed
    margin_rate: float              # Margin rate
    offset: int                     # Trailing offset
    open_price: float               # Open price in base currency
    open_time: datetime.datetime    # Open time
    order: int                      # Order number for opened transaction
    order2: int	                    # Order number for closed transaction
    position: int                   # Order number common both for opened and closed transaction
    profit: float                   # Profit in account currency
    sl: float                       # Zero if stop loss is not set (in base currency)
    state: str                      # Trade state, should be used for detecting pending order's cancellation
    storage: float                  # Order swaps in account currency
    symbol: str	                    # symbol name or null for deposit/withdrawal operations
    tp: float                       # Zero if take profit is not set (in base currency)
    type: float                     # type
    volume: float                   # Volume in lots
    
    
@dataclass
class StreamingTradeStatusRecord:
    customComment: str          # The value the customer may provide in order to retrieve it later.
    message: str                # Can be null
    order: int                  # Unique order number
    price: float                # Price in base currency
    requestStatus: TradeStatus  # Request status code, described below
    
    
class ResponseStatus:
    """ Parser for response status and stream session id. """
    def __init__(self, status: bool, streamSessionId:int):
        self.status = status
        self.stream_session_id = streamSessionId