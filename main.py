import asyncio
import logging
import pandas as pd
import ta

from algotrading.xtb.xapi import xapi, exceptions
from algotrading.xtb.xapi.records import *
from algotrading.xtb.client import Client
from algotrading.constants import *
from algotrading.indicators import *
from algotrading.graphing import *
from credentials import XTB_ACCOUNT_ID, XTB_PASSWORD

# Short hand asyncio calls
loop = asyncio.get_event_loop()
run_until_complete = loop.run_until_complete

    
## Initialize the clients
client = Client(
    XTB_ACCOUNT_ID,
    XTB_PASSWORD,
    symbol="GBPJPY"
)

async def handle_backtesting(connector):
    if (BACKTESTING == True) and (BACKTEST_NEW_DATA == True):
        historical_data = await client.get_last_request_data(
            connector,
            symbol=client.symbol,
            period=TRADE_PERIOD,
            multiplier=1,
            timeframe='YEARS'
        )
        client.write_backtest_ohlcv_data(historical_data)

    elif (BACKTESTING == True) and (BACKTEST_NEW_DATA == False):
        df = await client.get_backtest_ohlcv_data()
        df = df.head(BACKTESTING_CANDLES)
        # print(df)
        # df.to_csv("asd.csv")
        
        ## Add indicators after changing dataframe size

        plotter = IndicatorPlotter(df)
        # df.to_csv('signal_data.csv')
        if PLOT_CANDLES:
            
            ## Forward fill missing data before passing dataframe
            rsi = RelativeStrengthIndex(df)
            rsi.add_rsi_to_dataframe()
            x = rsi.get_rsi_traces()
            plotter.plot_indicator_chart(row2_indicator_traces=[x])


async def subscribe_and_process_candles(connector:xapi.XAPI, symbol):
    # Subscribe to streaming candles
    await connector.stream.getCandles(symbol)

    # Asynchronously handle incoming messages
    async for message in connector.stream.listen():
        client.logger.info(message)


async def run_xtb_client(**credentials):
    try:
        async with await xapi.connect(**credentials) as connector:
            if BACKTESTING:
                await handle_backtesting(connector)
            else:
                is_market_open = await client.is_market_open(connector, client.symbol)
                if is_market_open:
                    # Run candle subscription and message processing concurrently
                    tasks = [
                        subscribe_and_process_candles(connector, client.symbol),
                        # Add other async tasks here
                    ]
                    await asyncio.gather(*tasks)

    except asyncio.TimeoutError:
        if client.disconnected:
            await connector.disconnect()
            raise exceptions.ConnectionClosed
        else:
            client.logger.info("Connection lost: timed out. Reconnecting...")
            await asyncio.sleep(0.2)
    except exceptions.ConnectionClosed:
        await connector.disconnect()


if __name__ == '__main__':
    try:
        # Run the clients in a future
        asyncio.run(run_xtb_client(**client.credentials))

    except KeyboardInterrupt:
        pass