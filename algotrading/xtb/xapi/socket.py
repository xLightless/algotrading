from pipes import quote
from .connection import Connection
from .enums import TradeCmd, TradeType, PeriodCode

from typing import List

from .records import QuotesRecord, SymbolRecord, TradingRecord, TradeHoursRecord

class Socket(Connection):

    async def login(self, accountId: str, password: str):
        """
        In order to perform any action client application have to perform login process.
        No functionality is available before proper login process.
        After initial login, a new session is created and all commands are executed for a logged user until he/she logs out or drops the connection.
        """
        
        return await self._transaction({
            "command": "login",
            "arguments": {
                "userId": accountId,
                "password": password
            }
        })

    async def logout(self):
        """No returnData field in output. Only logout status message is sent."""
        
        return await self._transaction({
            "command": "logout"
        })

    async def getAllSymbols(self):
        """Returns array of all symbols available for the user."""
        
        return await self._transaction({
            "command": "getAllSymbols"
        })

    async def getCalendar(self):
        """Returns calendar with market events."""
        
        return await self._transaction({
            "command": "getCalendar"
        })

    async def getChartLastRequest(self, symbol: str, start: int, period: PeriodCode):
        """
        Returns chart info, from start date to the current time. If the chosen period of CHART_LAST_INFO_RECORD  is greater than 1 minute, the last candle returned by the API can change until the end of the period (the candle is being automatically updated every minute).

        Limitations: there are limitations in charts data availability. Detailed ranges for charts data, what can be accessed with specific period, are as follows:

        - PERIOD_M1 --- <0-1) month, i.e. one month time
        - PERIOD_M30 --- <1-7) month, six months time
        - PERIOD_H4 --- <7-13) month, six months time
        - PERIOD_D1 --- 13 month, and earlier on

        Note, that specific PERIOD_ is the lowest (i.e. the most detailed) period, accessible in listed range. For instance, in months range <1-7) you can access periods: PERIOD_M30, PERIOD_H1, PERIOD_H4, PERIOD_D1, PERIOD_W1, PERIOD_MN1. Specific data ranges availability is guaranteed, however those ranges may be wider, e.g.: PERIOD_M1 may be accessible for 1.5 months back from now, where 1.0 months is guaranteed.

        Example scenario:

        request charts of 5 minutes period, for 3 months time span, back from now;
        response: you are guaranteed to get 1 month of 5 minutes charts; because, 5 minutes period charts are not accessible 2 months and 3 months back from now.
        """
        
        return await self._transaction({
            "command": "getChartLastRequest",
            "arguments": {
                "info": {
                    "period": period.value,
                    "start": start,
                    "symbol": symbol
                }
            }
        })

    async def getChartRangeRequest(self, symbol: str, start: int, end: int, period: PeriodCode, ticks: int):
        """
        Returns chart info with data between given start and end dates.

        Limitations: there are limitations in charts data availability. Detailed ranges for charts data, what can be accessed with specific period, are as follows:

        - PERIOD_M1 --- <0-1) month, i.e. one month time
        - PERIOD_M30 --- <1-7) month, six months time
        - PERIOD_H4 --- <7-13) month, six months time
        - PERIOD_D1 --- 13 month, and earlier on

        Note, that specific PERIOD_ is the lowest (i.e. the most detailed) period, accessible in listed range. For instance, in months range <1-7) you can access periods: PERIOD_M30, PERIOD_H1, PERIOD_H4, PERIOD_D1, PERIOD_W1, PERIOD_MN1. Specific data ranges availability is guaranteed, however those ranges may be wider, e.g.: PERIOD_M1 may be accessible for 1.5 months back from now, where 1.0 months is guaranteed.
        """
        
        return await self._transaction({
            "command": "getChartRangeRequest",
            "arguments": {
                "info": {
                    "end": end,
                    "period": period.value,
                    "start": start,
                    "symbol": symbol,
                    "ticks": ticks
                }
            }
        })

    async def getCommissionDef(self, symbol: str, volume: float):
        """Returns calculation of commission and rate of exchange. The value is calculated as expected value, and therefore might not be perfectly accurate."""
        
        return await self._transaction({
            "command": "getCommissionDef",
            "arguments": {
                "symbol": symbol,
                "volume": volume
            }
        })

    async def getCurrentUserData(self):
        """Returns information about account currency, and account leverage."""
        
        return await self._transaction({
            "command": "getCurrentUserData"
        })

    async def getIbsHistory(self, start: int, end: int):
        """Returns IBs data from the given time range."""
        
        return await self._transaction({
            "command": "getIbsHistory",
            "arguments": {
                "end": end,
                "start": start
            }
        })

    async def getMarginLevel(self):
        """Returns various account indicators."""
        
        return await self._transaction({
            "command": "getMarginLevel"
        })

    async def getMarginTrade(self, symbol: str, volume: float):
        """
        Returns expected margin for given instrument and volume.
        The value is calculated as expected margin value, and therefore might not be perfectly accurate.
        """
        
        return await self._transaction({
            "command": "getMarginTrade",
            "arguments": {
                "symbol": symbol,
                "volume": volume
            }
        })

    async def getNews(self, start: int, end: int):
        """Returns news from trading server which were sent within specified period of time."""
        
        return await self._transaction({
            "command": "getNews",
            "arguments": {
                "end": end,
                "start": start
            }
        })

    async def getProfitCalculation(self, symbol: str, cmd: int, openPrice: float, closePrice: float, volume: float):
        """
        Calculates estimated profit for given deal data Should be used for calculator-like apps only.
        Profit for opened transactions should be taken from server, due to higher precision of server calculation.
        """
        
        return await self._transaction({
            "command": "getProfitCalculation",
            "arguments": {
                "closePrice": closePrice,
                "cmd": cmd,
                "openPrice": openPrice,
                "symbol": symbol,
                "volume": volume
            }
        })

    async def getServerTime(self):
        """Returns current time on trading server."""
        
        return await self._transaction({
            "command": "getServerTime"
        })

    async def getStepRules(self):
        """Returns a list of step rules for DMAs."""
        
        return await self._transaction({
            "command": "getStepRules"
        })

    async def getSymbol(self, symbol: str):
        """Returns information about symbol available for the user."""
        return await self._transaction({
            "command": "getSymbol",
            "arguments": {
                "symbol": symbol
            }
        })

    async def getTickPrices(self, symbols: List[str], timestamp: int, level: int = 0 ):
        """
        Returns array of current quotations for given symbols, only quotations that changed from given timestamp are returned.
        New timestamp obtained from output will be used as an argument of the next call of this command.
        """
        
        return await self._transaction({
            "command": "getTickPrices",
            "arguments": {
                "level": level,
                "symbols": symbols,
                "timestamp": timestamp
            }
        })

    async def getTradeRecords(self, orders: List[int]):
        """Returns array of trades listed in 'orders' argument."""
        
        return await self._transaction({
            "command": "getTradeRecords",
            "arguments": {
                "orders": orders
            }
        })

    async def getTrades(self, openedOnly: bool = True):
        """Returns array of user's trades."""
        
        return await self._transaction({
            "command": "getTrades",
            "arguments": {
                "openedOnly": openedOnly
            }
        })

    async def getTradesHistory(self, start: int, end: int = 0):
        """Returns array of user's trades which were closed within specified period of time."""
        
        return await self._transaction({
            "command": "getTradesHistory",
            "arguments": {
                "end": end,
                "start": start
            }
        })

    async def getTradingHours(self, symbols: List[str]) -> TradeHoursRecord:
        """Returns quotes and trading times."""
        
        response = await self._transaction({
            "command": "getTradingHours",
            "arguments": {
                "symbols": symbols
            }
        })
        response = response.get('returnData')[0]
        return TradeHoursRecord(**response)

    async def getVersion(self):
        """Returns the current API version."""
        
        return await self._transaction({
            "command": "getVersion"
        })

    async def ping(self):
        """
        Regularly calling this function is enough to refresh the internal state of all the components in the system.
        It is recommended that any application that does not execute other commands, should call this command at least once every 10 minutes.
        Please note that the streaming counterpart of this function is combination of 'ping' and 'getKeepAlive'.
        """
        
        return await self._transaction({
            "command": "ping"
        })

    async def tradeTransaction(self, symbol: str, cmd: TradeCmd, type: TradeType, price: float, volume: float,
                               sl: float = 0, tp: float = 0, order: int = 0, expiration: int = 0,
                               offset: int = 0, customComment: str = str()):
        """Starts trade transaction. 'tradeTransaction' sends main transaction information to the server."""
        
        if self.safe == True:
            return {
                "status": False,
                'errorCode': 'N/A',
                'errorDescr': 'Trading is disabled when safe=True'
            }

        return await self._transaction({
            "command": "tradeTransaction",
            "arguments": {
                "tradeTransInfo": {
                    "cmd": cmd.value,
                    "customComment": customComment,
                    "expiration": expiration,
                    "offset": offset,
                    "order": order,
                    "price": price,
                    "sl": sl,
                    "symbol": symbol,
                    "tp":   tp,
                    "type": type.value,
                    "volume": volume
                }
            }
        })

    async def tradeTransactionStatus(self, order: int):
        """
        Returns current transaction status.
        At any time of transaction processing client might check the status of transaction on server side.
        In order to do that client must provide unique order taken from 'tradeTransaction' invocation.
        """
        
        return await self._transaction({
            "command": "tradeTransactionStatus",
            "arguments": {
                "order": order
            }
        })
