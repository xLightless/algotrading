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

async def run_xtb_client(**credentials):
    """Run the xtb websocket client. """
    
    while not client.disconnected:
        try:
            async with await xapi.connect(**credentials) as connector:
                if BACKTESTING == True:
                    
                    ## Request backtesting data if needed
                    if BACKTEST_NEW_DATA == True:
                        historical_data = await client.get_last_request_data(
                            connector,
                            symbol=client.symbol,
                            period=TRADE_PERIOD,
                            multiplier=1,
                            timeframe='YEARS'
                        )
                        
                        # print(historical_data)
                    
                        # Write new data locally if enabled
                        client.write_backtest_ohlcv_data(historical_data)
                    
                    ## Get DataFrame
                    df = await client.get_backtest_ohlcv_data()
                    rsi = RelativeStrengthIndex(data=df)
                    df = rsi.add_rsi_to_dataframe()
                    df.head(BACKTEST_CANDLES)
                    
                    # df.to_csv("datatest.csv")
                    # print(df)
                    
                    ## Get indicators and plot them.
                    rsi = rsi.get_rsi_traces()
                    plotter = IndicatorPlotter(df)
                    plotter.plot_indicator_chart(
                        indicator_traces=[[i for i in rsi]]
                    )
                    
                    
                    raise exceptions.ConnectionClosed

                ## If backtesting is false then must be using the api in real time.
                is_market_open = await client.is_market_open(connector, client.symbol)
                if is_market_open:
                    print(is_market_open)
                    
                    
                # await client.get_candles(connector, client.symbol)
                
                
                # async for message in connector.stream.listen():
                #     client.logger.info(message)
            
            
            
        except asyncio.TimeoutError:
            if client.disconnected:
                await connector.disconnect()
                raise exceptions.ConnectionClosed
            else:
                client.logger.info("Connection lost: timed out. Reconnecting...")
                asyncio.sleep(0.2)
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