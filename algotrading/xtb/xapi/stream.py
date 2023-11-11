from .connection import Connection


class Stream(Connection):

    def __init__(self):
        super().__init__()
        self.streamSessionId = str()

    async def getBalance(self):
        """Allows to get actual account indicators values in real-time, as soon as they are available in the system."""
        
        return await self._request({
            "command": "getBalance",
            "streamSessionId": self.streamSessionId
        })

    async def stopBalance(self):
        """Unsubscribe from balance requests. """
        
        return await self._request({
            "command": "stopBalance"
        })

    async def getCandles(self, symbol: str):
        """Subscribes for API chart candles. The interval of every candle is 1 minute. A new candle arrives every minute."""
        
        return await self._request({
            "command": "getCandles",
            "streamSessionId": self.streamSessionId,
            "symbol": symbol
        })

    async def stopCandles(self, symbol: str):
        """Unsubscribe from candle requests. """
        
        return await self._request({
            "command": "stopCandles",
            "symbol": symbol
        })

    async def getKeepAlive(self):
        """Subscribes for 'keep alive' messages. A new 'keep alive' message is sent by the API every 3 seconds."""
        
        return await self._request({
            "command": "getKeepAlive",
            "streamSessionId": self.streamSessionId
        })

    async def stopKeepAlive(self):
        """Unsubscribe from keepAlive requests."""
        return await self._request({
            "command": "stopKeepAlive"
        })

    async def getNews(self):
        """Subscribes for news requests."""
        
        return await self._request({
            "command": "getNews",
            "streamSessionId": self.streamSessionId
        })

    async def stopNews(self):
        """Unsubscribe from news requests. """
        
        return await self._request({
            "command": "stopNews"
        }
        )

    async def getProfits(self):
        """Subscibes for profit requests. """
        
        return await self._request({
            "command": "getProfits",
            "streamSessionId": self.streamSessionId
        })

    async def stopProfits(self):
        """Unsubscribes from profit requests. """
        
        return await self._request({
            "command": "stopProfits"
        })

    async def getTickPrices(self, symbol: str, minArrivalTime: int = 0, maxLevel: int = 2):
        """
        Establishes subscription for quotations and allows to obtain the relevant information in real-time, as soon as it is available in the system.
        The getTickPrices  command can be invoked many times for the same symbol, but only one subscription for a given symbol will be created.
        Please beware that when multiple records are available, the order in which they are received is not guaranteed.
        """
        
        return await self._request({
            "command": "getTickPrices",
            "streamSessionId": self.streamSessionId,
            "symbol": symbol,
            "minArrivalTime": minArrivalTime,
            "maxLevel": maxLevel
        })

    async def stopTickPrices(self, symbol: str):
        """Unsubscribe from tick price requests. """
        
        return await self._request({
            "command": "stopTickPrices",
            "symbol": symbol
        })

    async def getTrades(self):
        """
        Establishes subscription for user trade status data and allows to obtain the relevant information in real-time, as soon as it is available in the system.
        Please beware that when multiple records are available, the order in which they are received is not guaranteed."""
        
        return await self._request({
            "command": "getTrades",
            "streamSessionId": self.streamSessionId
        })

    async def stopTrades(self):
        """Unsubscribes from trade requests. """
        
        return await self._request({
            "command": "stopTrades"
        })

    async def getTradeStatus(self):
        """
        Allows to get status for sent trade requests in real-time, as soon as it is available in the system.
        Please beware that when multiple records are available, the order in which they are received is not guaranteed.
        """
        
        return await self._request({
            "command": "getTradeStatus",
            "streamSessionId": self.streamSessionId
        })

    async def stopTradeStatus(self):
        """Unsubscribe from trade status requests. """
        
        return await self._request({
            "command": "stopTradeStatus"
        })

    async def ping(self):
        """
        Regularly calling this function is enough to refresh the internal state of all the components in the system.
        Streaming connection, when any command is not sent by client in the session, generates only one way network traffic.
        It is recommended that any application that does not execute other commands, should call this command at least once every 10 minutes.
        """
        
        return await self._request({
            "command": "ping",
            "streamSessionId": self.streamSessionId
        })
