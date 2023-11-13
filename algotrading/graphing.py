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

        # Remove the border around the candlestick body
        fig.update_traces(line=dict(width=1.5), selector=dict(type='candlestick'))
        
        
        fig.update_layout(
            xaxis=dict(
                title_font=self.axis_font,
                tickfont=self.axis_font,
                rangeslider=dict(visible=self.rangeslider_visible),
                showticklabels=False  # Hide X-axis tick labels
            ),
            yaxis=dict(
                title_font=self.axis_font,
                tickfont=self.axis_font,
                showticklabels=True  # Hide Y-axis tick labels
            ),
        )

        return fig

class IndicatorPlotter:
    def __init__(self, data: pd.DataFrame):
        self.df = data

    def plot_indicator_chart(
        self,
        indicator_traces: List[List[go.Scatter]] = [],
        optional_indicators: List[List[go.Scatter]] = [],
        candlestick_data: Union[None, pd.DataFrame] = None,
        volume_data: Union[None, pd.DataFrame] = None,
        num_candles_buttons: List[int] = [50, 100, 200],
    ):
        df = self.df

        # Create an instance of TradingViewPlotter with click and drag functionality disabled
        tradingview_style = TradingViewPlotter(df)

        # Create subplots with dynamic number of rows based on the number of indicators and additional traces
        num_rows = len(indicator_traces) + 2  # 1 for candlestick, 1 for volume
        row_heights = [
            0.2,  # Height for candlestick with wicks
            0.2,  # Height for volume
        ] + [0.2] * len(indicator_traces)  # Height for indicators

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

        # Forward-fill missing data in candlestick_data
        candlestick_data = self.forward_fill_missing_data(df, candlestick_data, ['open', 'high', 'low', 'close'])

        # Check if 'open', 'high', 'low', and 'close' columns exist
        if all(col in candlestick_data.columns for col in ['open', 'high', 'low', 'close']):
            candlestick_trace = go.Candlestick(
                x=candlestick_data['ctmString'],
                open=candlestick_data['open'],
                high=candlestick_data['high'],
                low=candlestick_data['low'],
                close=candlestick_data['close'],
                name='Candlestick Chart',  # Set the name for the candlestick chart
            )

            # Add the candlestick trace to the figure
            fig.add_trace(candlestick_trace, row=1, col=1)
        else:
            raise KeyError("Columns 'open', 'high', 'low', 'close' not found in candlestick_data")

        # Apply TradingView style
        fig = tradingview_style.apply_tradingview_style(fig)

        # Add optional indicators to the chart (on top of candlestick)
        for i, optional_indicator_list in enumerate(optional_indicators, start=2):
            for j, optional_indicator_trace in enumerate(optional_indicator_list, start=1):
                # Trim the optional_indicator_trace if it's longer than the number of candles
                if len(optional_indicator_trace.x) > len(candlestick_data):
                    optional_indicator_trace.x = optional_indicator_trace.x[:len(candlestick_data)]
                    optional_indicator_trace.y = optional_indicator_trace.y[:len(candlestick_data)]

                fig.add_trace(optional_indicator_trace, row=1, col=1)

                # Add label for the number of items in each optional indicator trace only for the first item in each list
                if j == 1:
                    label_text = f'Number of Items in {optional_indicator_trace.name}: {len(optional_indicator_trace.x)}'
                    label_annotation = go.layout.Annotation(
                        text=label_text,
                        showarrow=False,
                        xref='paper',
                        yref='paper',
                        x=0.5,
                        y=1.05 - 0.1 * (i - 2),  # Adjust the vertical position of the label
                        xanchor='center',
                        yanchor='bottom',
                        font=dict(size=14, color='white'),  # Set color to white
                    )
                    fig.add_annotation(label_annotation, row=1, col=1)

        # Add indicator traces to the chart
        for i, indicator_trace_list in enumerate(indicator_traces, start=2):
            for j, indicator_trace in enumerate(indicator_trace_list, start=1):
                # Trim the indicator_trace if it's longer than the number of candles
                if len(indicator_trace.x) > len(candlestick_data):
                    indicator_trace.x = indicator_trace.x[:len(candlestick_data)]
                    indicator_trace.y = indicator_trace.y[:len(candlestick_data)]

                fig.add_trace(indicator_trace, row=i, col=1)

                # Add label for the number of items in each indicator trace only for the first item in each list
                if j == 1:
                    label_text = f'Number of Items in {indicator_trace.name}: {len(indicator_trace.x)}'
                    label_annotation = go.layout.Annotation(
                        text=label_text,
                        showarrow=False,
                        xref='paper',
                        yref='paper',
                        x=0.5,
                        y=1.05 - 0.1 * (i - 2),  # Adjust the vertical position of the label
                        xanchor='center',
                        yanchor='bottom',
                        font=dict(size=14, color='white'),  # Set color to white
                    )
                    fig.add_annotation(label_annotation, row=i, col=1)

        # Volume bars (default to using df if not specified). Plots at the end of num_rows since enumeration ends at indicator_traces-1.
        volume_data = df if volume_data is None else volume_data

        # Forward-fill missing data in volume_data
        volume_data = self.forward_fill_missing_data(df, volume_data, ['volume'])

        # Check if 'volume' column exists
        # if 'volume' in volume_data.columns:
        #     volume_trace = go.Bar(x=volume_data['ctmString'], y=volume_data['volume'], marker_color='blue', name='Volume Chart')
        #     fig.add_trace(volume_trace, row=num_rows, col=1)
        #     # fig.add_trace(volume_trace, row=num_rows, col=1)
        # else:
        #     raise KeyError("Column 'volume' not found in volume_data")

        # Add label for the number of candles above the candlestick chart
        label_text = f'Number of Candles: {len(candlestick_data)}'
        label_annotation = go.layout.Annotation(
            text=label_text,
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0.5,
            y=1.05,
            xanchor='center',
            yanchor='bottom',
            font=dict(size=14, color='white'),  # Adjust font size and color as needed
        )
        fig.add_annotation(label_annotation)

        # Add buttons for different numbers of candles with text color option
        buttons = [
            dict(label=f'{num} Candles', method='relayout', args=[{'xaxis.range': [df['ctmString'].iloc[max(0, -num)], df['ctmString'].iloc[-1]]}])
            for num in num_candles_buttons
        ]

        # Update layout margin
        fig.update_layout(margin=margin)

        # Set up callback for the toggle button
        fig.update_layout(updatemenus=[dict(type='buttons', showactive=False, buttons=buttons)])

        # Define the rangebreaks to remove gaps in the candlestick chart
        rangebreaks = [
            dict(bounds=['sat', 'mon']),  # Exclude weekends
        ]

        # Apply rangebreaks to x-axis
        fig.update_xaxes(
            type='category',
            rangebreaks=rangebreaks
        )

        # Show the plot
        fig.show()

    def forward_fill_missing_data(self, df, data, column_names):
        # Handle missing data by filling gaps with the next available row
        merged_data = df.merge(data, on='ctmString', how='left', suffixes=('_df', '_data'))

        # Forward-fill missing data
        for col in column_names:
            if f'{col}_data' in merged_data.columns:
                merged_data[f'{col}_data'].ffill(inplace=True)
                merged_data[col] = merged_data[f'{col}_data']
                merged_data.drop(columns=[f'{col}_data'], inplace=True)
            else:
                raise KeyError(f"Column '{col}' not found in the merged data")

        return merged_data


# class IndicatorPlotter:
#     def __init__(self, data):
#         self.data = data

#     def plot_indicator_chart(self):
#         fig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=['Candlestick Chart', 'Indicator'])

#         df = self.data
#         # Candlestick Chart
#         candlestick = go.Candlestick(x=df.index,
#                                      open=df['open'],
#                                      high=df['high'],
#                                      low=df['low'],
#                                      close=df['close'],
#                                      name='Candlesticks')

#         fig.add_trace(candlestick, row=1, col=1)

#         # You can add more indicators or customizations as needed

#         # Update layout
#         fig.update_layout(xaxis_rangeslider_visible=False, title='Candlestick Chart with Indicator')

#         # Show the plot
#         fig.show()