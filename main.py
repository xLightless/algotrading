import asyncio
import logging
import pandas as pd
import ta

from algotrading.xtb.xapi import xapi, exceptions
from algotrading.xtb.xapi.records import *
from algotrading.xtb.client import Client
from algotrading.constants import *
from algotrading.indicators import *
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
                    if GET_NEW_HISTORICAL_DATA == True:
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
                    # date_range = pd.date_range(start="2023-10-10", end="2023-11-10", freq='15T') ## freq is 15 minutes.
                    df = await client.get_backtest_ohlcv_data()
                    # df = df.head(BACKTEST_CANDLES)
                    # df = df.drop(columns={'Volume'})
                    # df['Close Price'] = df.apply(lambda row: row['Open'] + max(0, row['Close']), axis=1)
                    print(df)
                    # rsi = RSIDivergence(df)
                    
                    # rsi.add_rsi_divergence()
                    # rsi.plot_rsi_divergence()
                    
                    
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