from algotrading.constants import *
from talipp.indicators import BB
from plotly.subplots import make_subplots

import plotly.graph_objects as go
import mplfinance as mpf
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pandas_ta as ta
import json

"""
Most of the information provided is from Investopedia and has all been factually corrected.
For more information on investments and trading visit here: https://www.investopedia.com.
"""


class Indicators():
    """
    Indicators provide an insight into real-time or historical market data by backtesting some methodology on price data to output the type of market trend.
    There are different forms of technical indicators and while many are oscillating ones that generally are considered 'lagging', there are also
    a select few which are not. For more information on types of indiciators, check out the link below:
    
    https://www.investopedia.com/articles/active-trading/041814/four-most-commonlyused-indicators-trend-trading.asp
    """

# class RSIDivergence(Indicators):
#     """Added an EMA RSI smoothing divergence indicator. """
#     def __init__(self, data, period=14, overbought=70, oversold=30):
#         self.data = data
#         self.period = period
#         self.overbought = overbought
#         self.oversold = oversold
        
#     def calculate_rsi(self, data=None, column_name='close', period=14):
        
#         if data == None:
#             data = self.data
#         # Calculate RSI using the provided function
#         df = data.copy()

#         # Calculate price changes specific to the 'close' column
#         df['price_change'] = df[column_name].diff()
    
#         # Calculate gains and losses
#         df['gain'] = df['price_change'].apply(lambda x: x if x > 0 else 0)
#         df['loss'] = df['price_change'].apply(lambda x: -x if x < 0 else 0)

#         # Calculate average gains and losses over the specified period
#         avg_gain = df['gain'].rolling(window=period, min_periods=5).mean()
#         avg_loss = df['loss'].rolling(window=period, min_periods=5).mean()

#         # Calculate relative strength (RS)
#         rs = avg_gain / avg_loss

#         # Calculate RSI
#         rsi = 100 - (100 / (1 + rs))

#         return rsi

#     def add_rsi_divergence(self):
#         # Calculate RSI on the DataFrame
#         self.data.ta.rsi(length=self.period, append=True)

#         # Identify overbought and oversold conditions
#         self.data['overbought'] = 0
#         self.data['oversold'] = 0
#         self.data.loc[self.data[f'RSI_{self.period}'] > self.overbought, 'overbought'] = 1
#         self.data.loc[self.data[f'RSI_{self.period}'] < self.oversold, 'oversold'] = 1

#         # Identify potential divergence
#         self.data['price_high_divergence'] = 0
#         self.data['price_low_divergence'] = 0

#         # Look for divergence in overbought conditions
#         self.data.loc[(self.data['close'].shift(1) > self.data['close']) & (self.data['RSI_14'].shift(1) <= self.overbought) & (self.data['RSI_14'] > self.overbought), 'price_high_divergence'] = 1

#         # Look for divergence in oversold conditions
#         self.data.loc[(self.data['close'].shift(1) < self.data['close']) & (self.data['RSI_14'].shift(1) >= self.oversold) & (self.data['RSI_14'] < self.oversold), 'price_low_divergence'] = 1
        
#         return self.data

#     # def plot_rsi_divergence(self):
#     #     # Create candlestick trace
#     #     candlestick = go.Candlestick(x=self.data.index,
#     #                                  open=self.data['open'],
#     #                                  high=self.data['high'],
#     #                                  low=self.data['low'],
#     #                                  close=self.data['close'],
#     #                                  name='Candlesticks')

#     #     # Create RSI trace
#     #     rsi_trace = go.Scatter(x=self.data.index, y=self.data[f'RSI_{self.period}'], mode='lines', name='RSI', yaxis='y2')

#     #     # Create buy and sell signal traces
#     #     signals_buy = self.data[self.data['price_low_divergence'] == 1]
#     #     signals_sell = self.data[self.data['price_high_divergence'] == 1]

#     #     buy_signal_trace = go.Scatter(x=signals_buy.index, y=signals_buy['low'], mode='markers', marker=dict(symbol='triangle-up', size=8, color='green'), name='Buy Signal', yaxis='y1')
#     #     sell_signal_trace = go.Scatter(x=signals_sell.index, y=signals_sell['high'], mode='markers', marker=dict(symbol='triangle-down', size=8, color='red'), name='Sell Signal', yaxis='y1')

#     #     # # Create layout
#     #     layout = go.Layout(title='RSI Overbought and Oversold Divergence',
#     #                        xaxis=dict(title='Date'),
#     #                        yaxis=dict(title='Price', domain=[0.3, 0.25]),
#     #                        yaxis2=dict(title='RSI', overlaying='y', side='right', showgrid=False, domain=[0,1]),
#     #                        showlegend=True)
#     #     # Create layout
#     #     # layout = go.Layout(title='RSI Overbought and Oversold Divergence',
#     #     #                    xaxis=dict(title='Date'),
#     #     #                    yaxis=dict(title='Price', domain=[0.3, 0.25]),
#     #     #                    showlegend=True)

#     #     # Create figure
#     #     fig = go.Figure(data=[candlestick, rsi_trace, buy_signal_trace, sell_signal_trace], layout=layout)
#     #     # # fig = go.Figure(data=[candlestick], layout=layout)
#     #     # # fig.update_layout()
#     #     # # Show the plot
#     #     # fig.show()
        
#     def plot_rsi_divergence(self):
#         # Create candlestick trace
#         candlestick = go.Candlestick(x=self.data.index,
#                                      open=self.data['open'],
#                                      high=self.data['high'],
#                                      low=self.data['low'],
#                                      close=self.data['close'],
#                                      name='Candlesticks')

#         # Create RSI trace
#         rsi_trace = go.Scatter(x=self.data.index, y=self.data[f'RSI_{self.period}'], mode='lines', name='RSI', yaxis='y2')

#         # Create layout for the first graph (Price and Time)
#         layout_price_time = go.Layout(title='Price and Time',
#                                       xaxis=dict(title='Date'),
#                                       yaxis=dict(title='Price', domain=[0.3, 0.25]),
#                                       showlegend=True)

#         # Create figure for the first graph (Price and Time)
#         fig_price_time = go.Figure(data=[candlestick], layout=layout_price_time)

#         # Show the plot for the first graph (Price and Time)
#         fig_price_time.show()

#         # Create buy and sell signal traces
#         signals_buy = self.data[self.data['price_low_divergence'] == 1]
#         signals_sell = self.data[self.data['price_high_divergence'] == 1]

#         buy_signal_trace = go.Scatter(x=signals_buy.index, y=signals_buy['low'], mode='markers', marker=dict(symbol='triangle-up', size=8, color='green'), name='Buy Signal', yaxis='y1')
#         sell_signal_trace = go.Scatter(x=signals_sell.index, y=signals_sell['high'], mode='markers', marker=dict(symbol='triangle-down', size=8, color='red'), name='Sell Signal', yaxis='y1')

#         # Create layout for the second graph (RSI)
#         layout_rsi = go.Layout(title='RSI',
#                                xaxis=dict(title='Date'),
#                                yaxis=dict(title='RSI', overlaying='y', side='right', showgrid=False, domain=[0,1]),
#                                showlegend=True)

#         # Create figure for the second graph (RSI)
#         fig_rsi = go.Figure(data=[rsi_trace, buy_signal_trace, sell_signal_trace], layout=layout_rsi)

#         # Show the plot for the second graph (RSI)
#         fig_rsi.show()


class RelativeStrengthIndex:
    def __init__(self, data, column_name='close', periods=14, overbought=70, oversold=30):
        self.data = data.copy()  # Make a copy of the data
        self.column_name = column_name
        self.periods = periods
        self.overbought = overbought
        self.oversold = oversold

    def calculate_rsi(self):
        delta = self.data[self.column_name].diff(1)
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)
        avg_gain = gain.rolling(window=self.periods, min_periods=1).mean()
        avg_loss = loss.rolling(window=self.periods, min_periods=1).mean()
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        return rsi

    def add_rsi_to_dataframe(self):
        rsi_column_name = f'rsi_{self.periods}'
        self.data[rsi_column_name] = self.calculate_rsi()
        return pd.DataFrame(self.data)

    def get_overbought_oversold_lines(self):
        overbought_line = np.full_like(self.data[self.column_name], self.overbought)
        oversold_line = np.full_like(self.data[self.column_name], self.oversold)
        return overbought_line, oversold_line
    
    def get_rsi_traces(self):
        rsi_trace = go.Scatter(
            x=self.data['ctmString'],
            y=self.data[f'rsi_{self.periods}'],
            mode='lines',
            name='RSI',
            line=dict(color='orange')
        )
        overbought_line, oversold_line = self.get_overbought_oversold_lines()
        overbought_trace = go.Scatter(
            x=self.data['ctmString'],
            y=overbought_line,
            mode='lines',
            name='Overbought',
            line=dict(color='red')
        )
        oversold_trace = go.Scatter(
            x=self.data['ctmString'],
            y=oversold_line,
            mode='lines',
            name='Oversold',
            line=dict(color='green')
        )
        return rsi_trace, overbought_trace, oversold_trace
        
class MACD(Indicators):
    """
    The moving average convergence divergence (MACD) is a kind of oscillating indicator.
    An oscillating indicator is a technical analysis indicator that varies over time within a band
    (above and below a centerline; the MACD fluctuates above and below zero).
    It is both a trend-following and momentum indicator.
    
    https://www.investopedia.com/trading/macd/
    """
        
        
class _MovingAverage(Indicators):
    """
    Moving average is a technical analysis tool that smooths out price data by creating a constantly updated average price.
    On a price chart, a moving average creates a single, flat line that effectively eliminates any variations due to random price
    fluctuations. There are other types of moving averages, including the exponential moving average (EMA) and the weighted moving average (WMA).
    
    https://www.investopedia.com/articles/active-trading/041814/four-most-commonlyused-indicators-trend-trading.asp#toc-moving-averages
    """
    
    
class SimpleMovingAverage(_MovingAverage):
    """
    A simple moving average (SMA) is an arithmetic moving average calculated by adding recent prices
    and then dividing that figure by the number of time periods in the calculation average.
    For example, one could add the closing price of a security for a number of time periods and then divide
    this total by that same number of periods. Short-term averages respond quickly to changes in the price of
    the underlying security, while long-term averages are slower to react.
    
    https://www.investopedia.com/terms/s/sma.asp
    """
    

class WeightedMovingAverage(_MovingAverage):
    """
    Weighted moving averages assign a heavier weighting to more current data points since they are more relevant
    than data points in the distant past. The sum of the weighting should add up to 1 (or 100%).
    In the case of the simple moving average, the weightings are equally distributed,
    which is why they are not shown in the table above. 
    
    https://www.investopedia.com/ask/answers/071414/whats-difference-between-moving-average-and-weighted-moving-average.asp#mntl-sc-block_1-0-25
    """
    
class ExponentialMovingAverage(_MovingAverage):
    """
    The exponential moving average (EMA) is a technical chart indicator that tracks the price of an investment
    (like a stock or commodity) over time. The EMA is a type of weighted moving average (WMA) that gives more weighting
    or importance to recent price data. Like the simple moving average (SMA), the EMA is used to see price trends over time,
    and watching several EMAs at the same time is easy to do with moving average ribbons.

    https://www.investopedia.com/ask/answers/122314/what-exponential-moving-average-ema-formula-and-how-ema-calculated.asp
    """
    
    
    
class BreakoutAndBreakdown(Indicators):
    """"""