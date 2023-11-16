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
import random

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
    
class RelativeStrengthIndex(Indicators):
    def __init__(self, data, column_name='close', periods=14, overbought=70, oversold=30):
        self.data = data.copy()  # Make a copy of the data
        self.column_name = column_name
        self.periods = periods
        self.overbought = overbought
        self.extended_overbought = 80
        self.extended_oversold = 20
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

    def add_rsi_to_dataframe(self) -> pd.DataFrame:
        rsi_column_name = f'rsi_{self.periods}'
        self.data[rsi_column_name] = self.calculate_rsi()
        return self.data

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
            line=dict(color='#787B86', width=1.25, dash='dot'),
            hoverinfo='none',
            showlegend=False
        )
        
        oversold_trace = go.Scatter(
            x=self.data['ctmString'],
            y=oversold_line,
            mode='lines',
            name='Oversold',
            line=dict(color='#787B86', width=1.25, dash='dot'),
            hoverinfo='none',
            showlegend=False
        )
        
        extended_overbought_trace = go.Scatter(
            x=self.data['ctmString'],
            y=np.full_like(self.data[self.column_name], self.extended_overbought),
            mode='lines',
            name='Extended Overbought',
            line=dict(color='#787B86', width=1.25, dash='dot'),
            hoverinfo='none',
            showlegend=False
        )
        extended_oversold_trace = go.Scatter(
            x=self.data['ctmString'],
            y=np.full_like(self.data[self.column_name], self.extended_oversold),
            mode='lines',
            name='Extended Oversold',
            line=dict(color='#787B86', width=1.25, dash='dot'),
            hoverinfo='none',
            showlegend=False
        )
        
        return rsi_trace, overbought_trace, oversold_trace, extended_overbought_trace, extended_oversold_trace
    
    def get_rsi_trend_traces(self):
        rsi_values = self.data[f'rsi_{self.periods}']
        rsi_trace_colors = self.get_rsi_trend_trace_color()

        rsi_traces = []

        start_index = 0
        current_color = rsi_trace_colors[0]

        for i in range(1, min(len(rsi_values), len(rsi_trace_colors))):  # Use min to avoid going out of bounds
            if rsi_trace_colors[i] != current_color:
                rsi_trace = go.Scatter(
                    x=self.data['ctmString'][start_index:i],
                    y=rsi_values[start_index:i],
                    mode='lines',
                    name='RSI',
                    line=dict(color=current_color, width=1.25),
                    showlegend=False,
                )
                rsi_traces.append(rsi_trace)
                start_index = i
                current_color = rsi_trace_colors[i]

        rsi_trace = go.Scatter(
            x=self.data['ctmString'][start_index:],
            y=rsi_values[start_index:],
            mode='lines',
            name='RSI',
            line=dict(color=current_color, width=1.25),
            showlegend=False,
        )
        rsi_traces.append(rsi_trace)

        overbought_line, oversold_line = self.get_overbought_oversold_lines()
        overbought_trace = go.Scatter(
            x=self.data['ctmString'],
            y=overbought_line,
            mode='lines',
            name='Overbought',
            line=dict(color='#787B86', width=1.25, dash='dash'),
            hoverinfo='none',
            showlegend=False
        )
        oversold_trace = go.Scatter(
            x=self.data['ctmString'],
            y=oversold_line,
            mode='lines',
            name='Oversold',
            line=dict(color='#787B86', width=1.25, dash='dash'),
            hoverinfo='none',
            showlegend=False
        )

        extended_overbought_trace = go.Scatter(
            x=self.data['ctmString'],
            y=np.full_like(self.data[self.column_name], self.extended_overbought),
            mode='lines',
            name='Extended Overbought',
            line=dict(color='#787B86', width=1.25, dash='dot'),
            hoverinfo='none',
            showlegend=False
        )
        extended_oversold_trace = go.Scatter(
            x=self.data['ctmString'],
            y=np.full_like(self.data[self.column_name], self.extended_oversold),
            mode='lines',
            name='Extended Oversold',
            line=dict(color='#787B86', width=1.25, dash='dot'),
            hoverinfo='none',
            showlegend=False
        )

        return rsi_traces + [overbought_trace, oversold_trace, extended_overbought_trace, extended_oversold_trace]

    def get_rsi_trend_trace_color(self):
        rsi_values = self.data[f'rsi_{self.periods}']
        colors = []

        trend_color = 'orange'  # Default color
        for rsi in rsi_values:
            if rsi > 70:
                trend_color = 'red'  # Bullish trend
            elif rsi < 30:
                trend_color = 'green'  # Bearish trend

            colors.append(trend_color)

        return colors
    
    def calculate_rsi_trendline_breaks(self):
        rsi_values = self.data[f'rsi_{self.periods}']
        trendline_breaks = self._calculate_rsi_trendline_breaks(rsi_values, len(rsi_values))
        return trendline_breaks

    # def _calculate_rsi_trendline_breaks(self, rsi_values):
    #     # Calculate RSI
    #     delta = np.diff(rsi_values)
    #     gain = np.where(delta > 0, delta, 0)
    #     loss = -np.where(delta < 0, delta, 0)
    #     avg_gain = np.convolve(gain, np.ones(self.periods) / self.periods, mode='valid')
    #     avg_loss = np.convolve(loss, np.ones(self.periods) / self.periods, mode='valid')
    #     rs = avg_gain / avg_loss
    #     rsi = 100 - (100 / (1 + rs))

    #     # Calculate RSI trendline
    #     trendline_period = 5  # You can adjust this if needed
    #     rsi_trendline = np.convolve(rsi, np.ones(trendline_period) / trendline_period, mode='same')

    #     # Identify RSI trendline breaks
    #     trendline_breaks = np.where(rsi > rsi_trendline, 1, np.where(rsi < rsi_trendline, -1, 0))

    #     return trendline_breaks
    
    def _calculate_rsi_trendline_breaks(self, rsi_values):
        # Calculate RSI
        delta = np.diff(rsi_values)
        gain = np.where(delta > 0, delta, 0)
        loss = -np.where(delta < 0, delta, 0)
        avg_gain = np.convolve(gain, np.ones(self.periods) / self.periods, mode='valid')
        avg_loss = np.convolve(loss, np.ones(self.periods) / self.periods, mode='valid')
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))

        # Calculate RSI trendline
        trendline_period = 5  # You can adjust this if needed
        rsi_trendline = np.convolve(rsi, np.ones(trendline_period) / trendline_period, mode='same')

        # Identify RSI trendline breaks
        trendline_breaks = np.where(rsi > rsi_trendline, 1, np.where(rsi < rsi_trendline, -1, 0))

        return trendline_breaks
        
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
    
    def __init__(self, data, window_size = random.randint(5, 20)):
        self.data = data
        self.window_size = window_size

    def calculate_sma(self):
        """
        Calculate the Simple Moving Average (SMA) for the given dataset.
        """
        if not isinstance(self.data, pd.Series):
            if isinstance(self.data, pd.DataFrame):
                if self.data.shape[1] == 1:
                    # If there's only one column, use that column for the SMA calculation
                    self.data = self.data.squeeze()
                else:
                    # If there are multiple columns, assume the first numeric column for the SMA calculation
                    numeric_columns = self.data.select_dtypes(include='number')
                    if not numeric_columns.empty:
                        self.data = numeric_columns.iloc[:, 0]
                    else:
                        raise ValueError("No numeric columns found in the DataFrame for SMA calculation.")
            else:
                self.data = pd.Series(self.data)

        # Calculate the moving average using the rolling function
        sma = self.data.rolling(window=self.window_size).mean()

        return sma

    def get_sma_traces(self):
        """
        Create traces for plotting SMA using Plotly.
        """
        sma = self.calculate_sma()

        trace_data = go.Scatter(
            x=self.data.index,
            y=self.data,
            mode='lines',
            name='Original Data',
            line=dict(color='blue')
        )

        trace_sma = go.Scatter(
            x=sma.index,
            y=sma,
            mode='lines',
            name=f'SMA ({self.window_size} periods)',
            line=dict(color='orange')
        )

        return trace_data, trace_sma
    

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
    
    
    
class BreakingTrendIndicator:
    TREND_BREAK_THRESHOLD = 0.10 # 0.05 percent is default.
    
    def __init__(self, data, enable_trendline=False, smoothing=True):
        """
        Initialize the BreakingTrendIndicator with a DataFrame.

        Parameters:
        - data (pd.DataFrame): DataFrame containing price data.
        """
        self.df = data
        self.enable_trendline = enable_trendline
        self.smoothing = smoothing

    def add_signals_to_dataframe(self):
        """
        Calculate potential buy and sell signals based on percentage change.
        """
        # Ensure 'close' column is numeric
        self.df['close'] = pd.to_numeric(self.df['close'], errors='coerce')

        # Set percentage change threshold values (adjust as needed)
        percent_change_threshold = self.TREND_BREAK_THRESHOLD

        # Calculate percentage change in 'close' column
        percent_change = self.df['close'].pct_change() * 100
        self.df['signal change'] = percent_change
        
        # Calculate buy and sell signals based on percentage change
        buy_signals = percent_change > percent_change_threshold
        sell_signals = percent_change < -percent_change_threshold

        # Add signals to the DataFrame
        self.df["buy_signal"] = buy_signals
        self.df["sell_signal"] = sell_signals
        return self.df    
    
    # def add_signals_to_dataframe(self):
    #     # Ensure 'close' column is numeric
    #     self.df['close'] = pd.to_numeric(self.df['close'], errors='coerce')

    #     # Calculate percentage change in 'close' column
    #     percent_change = self.df['close'].pct_change() * 100
    #     self.df['signal_change'] = percent_change

    #     # Calculate buy and sell signals based on percentage change
    #     buy_signals = percent_change > self.TREND_BREAK_THRESHOLD
    #     sell_signals = percent_change < -self.TREND_BREAK_THRESHOLD

    #     # Filter buy signals to include only the newest highest high
    #     newest_highest_high = self.df['high'].idxmax()
    #     buy_signals = buy_signals & (self.df.index == newest_highest_high)

    #     # Filter sell signals to include only the newest lowest low
    #     newest_lowest_low = self.df['low'].idxmin()
    #     sell_signals = sell_signals & (self.df.index == newest_lowest_low)

    #     # Add signals to the DataFrame
    #     self.df["buy_signal"] = buy_signals
    #     self.df["sell_signal"] = sell_signals

    #     return self.df
    
    def get_breaking_traces(self, candlestick_data=None):
        candlestick_data = self.df if candlestick_data is None else candlestick_data

        buy_signals = self.df[self.df["buy_signal"]]
        sell_signals = self.df[self.df["sell_signal"]]

        y_position = 0.2

        buy_trace = go.Scatter(
            x=candlestick_data['ctmString'][buy_signals.index],
            y=candlestick_data['low'][buy_signals.index] - y_position,
            mode='markers',
            marker=dict(color='green', size=12, symbol='triangle-up'),
            name='Buy Signal',
            hoverinfo='text',
            text='*** BUY ***'
        )

        sell_trace = go.Scatter(
            x=candlestick_data['ctmString'][sell_signals.index],
            y=candlestick_data['high'][sell_signals.index] + y_position,
            mode='markers',
            marker=dict(color='red', size=12, symbol='triangle-down'),
            name='Sell Signal',
            hoverinfo='text',
            text='*** SELL *** '
        )

        if self.enable_trendline == True:
            # Initialize line traces with empty lists
            consecutive_buy_line_trace = []
            consecutive_sell_line_trace = []

            # Identify consecutive buy signals and create a line trace
            consecutive_buy_indices = self.create_signal_trendline(self.df['buy_signal'], 'buy', 3)
            if consecutive_buy_indices:
                consecutive_buy_line_trace = [go.Scatter(
                    x=candlestick_data['ctmString'][consecutive_buy_indices],
                    y=candlestick_data['low'][consecutive_buy_indices] - y_position,
                    mode='lines',
                    line=dict(color='green', width=2),
                    name='Consecutive Buy Line',
                    hoverinfo='text',
                    text='*** Consecutive Buy Line ***'
                )]

            # Identify consecutive sell signals and create a line trace
            consecutive_sell_indices = self.create_signal_trendline(self.df['sell_signal'], 'sell', 3)
            if consecutive_sell_indices:
                consecutive_sell_line_trace = [go.Scatter(
                    x=candlestick_data['ctmString'][consecutive_sell_indices],
                    y=candlestick_data['high'][consecutive_sell_indices] + y_position,
                    mode='lines',
                    line=dict(color='red', width=2),
                    name='Consecutive Sell Line',
                    hoverinfo='text',
                    text='*** Consecutive Sell Line ***'
                )]

            # Concatenate all traces into a single list
            all_traces = [buy_trace, sell_trace] + consecutive_buy_line_trace + consecutive_sell_line_trace

            return all_traces
    
        return buy_trace, sell_trace


    
    def create_signal_trendline(self, signal_data, signal_type, connect_count):
        connected_indices = []
        trend_in_progress = False
        current_trend_type = None

        signal_indices = signal_data[signal_data].index

        for i, start_index in enumerate(signal_indices):
            end_index = start_index + connect_count - 1
            if end_index in signal_indices[i:]:
                consecutive_sequence = signal_indices[i:i + connect_count]

                # Check if all consecutive signals are of the same type
                if all(self.df[signal_type + '_signal'].iloc[x] for x in consecutive_sequence):
                    # If a trend is not in progress, start a new one
                    if not trend_in_progress or current_trend_type != signal_type:
                        connected_indices.append(start_index)
                        trend_in_progress = True
                        current_trend_type = signal_type
                    # Update the start_index to the last index of the consecutive sequence
                    start_index = consecutive_sequence[-1]
                    connected_indices.append(start_index)
                else:
                    # If a trend was in progress but the signal type changed, start a new one
                    if trend_in_progress:
                        trend_in_progress = False

        return connected_indices
    
    
    def smoothed_trendline(self, signal_data, signal_type, connect_count):
        """
        Connect consecutive signals of the same type until an opposite signal is discovered and create a trendline.

        Parameters:
        - signal_data (pd.Series): Signal data (True for signals, False for non-signals).
        - signal_type (str): Type of signal ('buy' or 'sell').
        - connect_count (int): Number of consecutive signals to connect.

        Returns:
        - list: List of indices representing connected signals.
        """
        connected_indices = []

        # Find indices where the signal of the given type is True
        signal_indices = signal_data[signal_data].index

        for i, start_index in enumerate(signal_indices):
            # Check if there are enough consecutive signals of the same type
            end_index = start_index + connect_count - 1
            if end_index in signal_indices[i:]:
                consecutive_sequence = signal_indices[i:i + connect_count]

                # Check if all consecutive signals are of the same type
                if all(self.df[signal_type + '_signal'].iloc[x] for x in consecutive_sequence):
                    # Calculate the average index for the connected signals
                    average_index = int(np.mean(consecutive_sequence))
                    connected_indices.append(average_index)
                else:
                    break  # Stop connecting if an opposite signal is discovered

        # Plot the trendline
        self.plot_trendline(signal_type, connected_indices)

        return connected_indices

    def plot_trendline(self, signal_type, connected_indices):
        """
        Plot a trendline based on the connected indices.

        Parameters:
        - signal_type (str): Type of signal ('buy' or 'sell').
        - connected_indices (list): List of indices representing connected signals.

        Returns:
        - go.Scatter: Plotly scatter trace for the trendline.
        """
        if not connected_indices:
            return None

        # Extract relevant data for plotting
        prices = self.df['high'] if signal_type == 'buy' else self.df['low']
        trendline_values = prices.iloc[connected_indices]

        # Create a Plotly scatter trace for the trendline
        trendline_trace = go.Scatter(
            x=connected_indices,
            y=trendline_values,
            mode='lines',
            name=f'{signal_type.capitalize()} Trendline',
            line=dict(color='green' if signal_type == 'buy' else 'red')
        )

        # Create a scatter trace for connected signals
        connected_signals_trace = go.Scatter(
            x=connected_indices,
            y=trendline_values,
            mode='markers',
            marker=dict(color='black', symbol='x'),
            name='Connected Signals'
        )

        return trendline_trace, connected_signals_trace