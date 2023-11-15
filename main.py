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

async def message_handler(queue):
    while True:
        message = await queue.get()
        if message is None:
            break
        client.logger.info(message)

async def run_xtb_client(**credentials):
    """Run the xtb websocket client. """
    
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
            trendline_break = BreakingTrendIndicator(df)
            df = trendline_break.add_signals_to_dataframe()
            df = df.head(BACKTESTING_CANDLES)
            print(df)
            df.to_csv("asd.csv")
            breakout, breakdown = trendline_break.get_breaking_traces()

            plotter = IndicatorPlotter(df)
            if PLOT_CANDLES == True:
                plotter.plot_indicator_chart(indicator_traces=[[breakout, breakdown]])
        
    while not client.disconnected:
        try:
            async with await xapi.connect(**credentials) as connector:
                if BACKTESTING == True:
                    await handle_backtesting(connector)
                    raise exceptions.ConnectionClosed

                is_market_open = await client.is_market_open(connector, client.symbol)
                if is_market_open:
                    
                    # Create an asyncio queue
                    message_queue = asyncio.Queue()

                    # Start the message handler coroutine
                    handler_task = asyncio.create_task(message_handler(message_queue))

                    # Start streaming candles
                    await connector.stream.getCandles(client.symbol)

                    # Asynchronously handle incoming messages
                    async for message in connector.stream.listen():
                        # Enqueue the message for processing
                        await message_queue.put(message)

                    # Signal the message handler to finish
                    await message_queue.put(None)
                    await handler_task

                # Other async tasks can be added here

        except asyncio.TimeoutError:
            if client.disconnected:
                await connector.disconnect()
                raise exceptions.ConnectionClosed
            else:
                client.logger.info("Connection lost: timed out. Reconnecting...")
                await asyncio.sleep(0.2)
                continue
        except exceptions.ConnectionClosed:
            await connector.disconnect()
            break
            
        # except exceptions.ConnectionClosed:
        #     break
    
if __name__ == '__main__':
    
    
    try:
        ## Run the clients in a future
        run_until_complete(run_xtb_client(
            **client.credentials
        ))
        
    except KeyboardInterrupt:
        pass