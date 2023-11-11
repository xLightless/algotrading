import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from typing import List, Union
from algotrading.indicators import *

class TradingViewPlotter:
    def __init__(self, data):
        self.df = data

        # Dark mode color scheme
        self.background_color = '#1e1e1e'
        self.grid_color = '#2f3640'
        self.candlestick_colors = {'up': '#00ff00', 'down': '#F23645'}

        # Font settings
        self.title_font = dict(family='Arial', size=16, color='white')
        self.axis_font = dict(family='Arial', size=12, color='white')

        # Button text color
        self.button_text_color = 'white'

        # Click and drag functionality
        self.enable_click_and_drag = True

        # Range slider visibility
        self.rangeslider_visible = False

        # Border settings
        self.border_color = '#ffffff'  # Set to your desired border color
        self.border_width = 0  # Set to your desired border width

        # Legend text color
        self.legend_text_color = 'white'

        # Candlestick chart row height
        self.candlestick_row_height = 1

        # Volume chart row height
        self.volume_row_height = 0.2

        # Indicator chart row height
        self.indicator_row_height = 0.5

        # Hovermode as a boolean attribute
        self.hovermode = True

    def apply_tradingview_style(self, fig):
        # Apply dark mode background color
        fig.update_layout(
            plot_bgcolor=self.background_color,
            paper_bgcolor=self.background_color,
            margin=dict(l=10, r=10, t=30, b=10)  # Adjust margins for border
        )

        # Apply grid color
        fig.update_xaxes(gridcolor=self.grid_color)
        fig.update_yaxes(gridcolor=self.grid_color)

        # Apply title font
        fig.update_layout(
            title_font=dict(family=self.title_font['family'], size=self.title_font['size'], color=self.title_font['color'])
        )

        # Apply axis font
        fig.update_layout(
            xaxis=dict(title_font=self.axis_font, tickfont=self.axis_font, rangeslider=dict(visible=self.rangeslider_visible)),
            yaxis=dict(title_font=self.axis_font, tickfont=self.axis_font),
        )

        # Apply candlestick colors
        fig.update_traces(
            increasing_line_color=self.candlestick_colors['up'],
            decreasing_line_color=self.candlestick_colors['down'],
            selector=dict(type='candlestick')
        )

        # Apply border
        fig.update_layout(
            xaxis=dict(linecolor=self.border_color, linewidth=self.border_width),
            yaxis=dict(linecolor=self.border_color, linewidth=self.border_width),
            xaxis2=dict(linecolor=self.border_color, linewidth=self.border_width),
            yaxis2=dict(linecolor=self.border_color, linewidth=self.border_width),
            showlegend=True,  # Display legend
            legend=dict(orientation='h', y=1.1, font=dict(color=self.legend_text_color))  # Position the legend above the chart
        )

        if self.hovermode:
            fig.update_layout(hovermode='x unified')

        # Disable candlestick border
        fig.update_traces(line=dict(width=0), selector=dict(type='candlestick'))

        return fig
    
    # def toggle_candlestick_border(self, _, fig, candlestick_trace):
    #     # Toggle the candlestick border visibility
    #     self.show_candlestick_border = not self.show_candlestick_border
    #     fig.update_traces(
    #         line=dict(width=1) if self.show_candlestick_border else dict(width=0),
    #         selector=dict(type='candlestick')
    #     )

class IndicatorPlotter:
    def __init__(self, data: pd.DataFrame):
        self.df = data
        
    def plot_indicator_chart(
        self,
        indicator_traces: List[List[go.Scatter]] = [],  # List of lists for each indicator
        candlestick_data: Union[None, pd.DataFrame] = None,
        volume_data: Union[None, pd.DataFrame] = None,
        num_candles_buttons: List[int] = [50, 100, 200],
    ):
        df = self.df

        # Create an instance of TradingViewPlotter with click and drag functionality disabled
        tradingview_style = TradingViewPlotter(df)
        tradingview_style.enable_click_and_drag = False

        # Create subplots with dynamic number of rows based on the number of indicators and additional traces
        num_rows = len(indicator_traces) + 2  # 1 for candlestick, 1 for volume
        row_heights = [
            tradingview_style.candlestick_row_height,
            tradingview_style.volume_row_height,
        ] + [tradingview_style.indicator_row_height] * len(indicator_traces)

        # Ensure that the length of row_heights is 2 if there are no indicator traces
        row_heights += [0.2] * (2 - len(row_heights))

        # Set margin to reduce space between charts
        margin = dict(l=10, r=10, t=30, b=10, pad=0)

        # Create subplots with adjusted margin
        fig = make_subplots(
            rows=num_rows, cols=1, shared_xaxes=True, row_heights=row_heights,
            vertical_spacing=0.02, subplot_titles=[None] * num_rows, row_titles=[None] * num_rows
        )

        # Candlestick chart (default to using df if not specified)
        candlestick_data = df if candlestick_data is None else candlestick_data
        candlestick_trace = go.Candlestick(
            x=candlestick_data['ctmString'],
            open=candlestick_data['open'],
            high=candlestick_data['high'],
            low=candlestick_data['low'],
            close=candlestick_data['close'],
            name='Price Chart',  # Set the name for the candlestick chart
        )
        fig.add_trace(candlestick_trace, row=1, col=1)

        # Apply TradingView style
        fig = tradingview_style.apply_tradingview_style(fig)

        # Add indicator traces to the chart
        for i, indicator_trace_list in enumerate(indicator_traces, start=2):
            for indicator_trace in indicator_trace_list:
                fig.add_trace(indicator_trace, row=i, col=1)

        # Volume bars (default to using df if not specified). Plots at the end of num_rows since enumeration ends at indicator_traces-1.
        volume_data = df if volume_data is None else volume_data
        volume_trace = go.Bar(x=volume_data['ctmString'], y=volume_data['volume'], marker_color='blue', name='Volume Chart')
        fig.add_trace(volume_trace, row=num_rows, col=1)

        # Add buttons for different numbers of candles with text color option
        buttons = [
            dict(label=f'{num} Candles', method='relayout', args=[{'xaxis.range': [df['ctmString'].iloc[max(0, -num)], df['ctmString'].iloc[-1]]}])
            for num in num_candles_buttons
        ]

        # Add click and drag functionality
        if tradingview_style.enable_click_and_drag:
            fig.update_layout(dragmode='pan')

        # Update layout margin
        fig.update_layout(margin=margin)

        # Show the plot
        fig.show()

        
    # def calculate_close_diff(self, close_data):
    #     close_diff = close_data.diff().shift(-1)  # Calculate the difference between the current close and the next close
    #     close_diff_str = close_diff.apply(lambda x: f'Close Diff: {x:.2f}' if not pd.isnull(x) else '')  # Convert to string format
    #     return close_diff_str
        
        
        

# EXAMPLE CODE FOR PLOTTING
# class IndicatorPlotter:
#     def __init__(self, data: pd.DataFrame):
#         self.df = data
        
#     def plot_indicator_chart(
#         self,
#         indicator_traces: List[go.Scatter] = [],
#         candlestick_data: Union[None, pd.DataFrame] = None,
#         volume_data: Union[None, pd.DataFrame] = None,
#         num_candles_buttons: List[int] = [50, 100, 200],
#     ):
#         df = self.df

#         # Create an instance of TradingViewPlotter with click and drag functionality disabled
#         tradingview_style = TradingViewPlotter(df)
#         tradingview_style.enable_click_and_drag = False

#         # Create subplots with dynamic number of rows based on the number of indicators
#         num_rows = len(indicator_traces) + 2  # 1 for candlestick, 1 for volume
#         row_heights = [
#             tradingview_style.candlestick_row_height,
#             tradingview_style.volume_row_height,
#         ] + [tradingview_style.indicator_row_height] * len(indicator_traces)

#         # Ensure that the length of row_heights is 2 if there are no indicator traces
#         row_heights += [0.2] * (2 - len(row_heights))

#         # Set margin to reduce space between charts
#         margin = dict(l=10, r=10, t=30, b=10, pad=0)

#         # Create subplots with adjusted margin
#         fig = make_subplots(
#             rows=num_rows, cols=1, shared_xaxes=True, row_heights=row_heights,
#             vertical_spacing=0.02, subplot_titles=[None] * num_rows, row_titles=[None] * num_rows
#         )

#         # Candlestick chart (default to using df if not specified)
#         candlestick_data = df if candlestick_data is None else candlestick_data
#         candlestick_trace = go.Candlestick(
#             x=candlestick_data['ctmString'],
#             open=candlestick_data['open'],
#             high=candlestick_data['high'],
#             low=candlestick_data['low'],
#             close=candlestick_data['close'],
#             name='Price Chart',  # Set the name for the candlestick chart
#         )
#         fig.add_trace(candlestick_trace, row=1, col=1)

#         # Apply TradingView style
#         fig = tradingview_style.apply_tradingview_style(fig)

#         # Add indicator traces to the chart
#         for i, indicator_trace in enumerate(indicator_traces, start=2):
#             fig.add_trace(indicator_trace, row=i, col=1)

#         # Volume bars (default to using df if not specified)
#         volume_data = df if volume_data is None else volume_data
#         volume_trace = go.Bar(x=volume_data['ctmString'], y=volume_data['volume'], marker_color='blue', name='Volume Chart')
#         fig.add_trace(volume_trace, row=num_rows, col=1)

#         # Add buttons for different number of candles with text color option
#         buttons = [
#             dict(label=f'{num} Candles', method='relayout', args=[{'xaxis.range': [df['ctmString'].iloc[max(0, -num)], df['ctmString'].iloc[-1]]}])
#             for num in num_candles_buttons
#         ]

#         # Add click and drag functionality
#         if tradingview_style.enable_click_and_drag:
#             fig.update_layout(dragmode='pan')

#         # Update layout margin
#         fig.update_layout(margin=margin)

#         # Show the plot
#         fig.show()