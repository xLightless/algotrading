import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from typing import List, Union
from algotrading.indicators import *

class TradingViewPlotter:
    def __init__(self, data):
        self.df = data
        self.background_color = '#1e1e1e'
        self.grid_color = '#2f3640'
        self.candlestick_colors = {'up': '#00ff00', 'down': '#F23645'}
        self.title_font = dict(family='Arial', size=16, color='white')
        self.axis_font = dict(family='Arial', size=12, color='white')
        self.button_text_color = 'white'
        self.enable_click_and_drag = True
        self.rangeslider_visible = False
        self.border_color = '#ffffff'
        self.border_width = 0
        self.legend_text_color = 'white'
        self.candlestick_row_height = 1
        self.volume_row_height = 0.2
        self.indicator_row_height = 0.5
        self.hovermode = True

    def apply_tradingview_style(self, fig):
        fig.update_layout(
            plot_bgcolor=self.background_color,
            paper_bgcolor=self.background_color,
            margin=dict(l=10, r=10, t=30, b=10)
        )
        fig.update_xaxes(gridcolor=self.grid_color)
        fig.update_yaxes(gridcolor=self.grid_color)
        fig.update_layout(
            title_font=dict(family=self.title_font['family'], size=self.title_font['size'], color=self.title_font['color'])
        )
        fig.update_layout(
            xaxis=dict(title_font=self.axis_font, tickfont=self.axis_font, rangeslider=dict(visible=self.rangeslider_visible), showline=False),
            yaxis=dict(title_font=self.axis_font, tickfont=self.axis_font, showline=False),
        )
        fig.update_traces(
            increasing_line_color=self.candlestick_colors['up'],
            decreasing_line_color=self.candlestick_colors['down'],
            selector=dict(type='candlestick')
        )
        fig.update_layout(
            xaxis=dict(linecolor=self.border_color, linewidth=self.border_width),
            yaxis=dict(linecolor=self.border_color, linewidth=self.border_width),
            xaxis2=dict(linecolor=self.border_color, linewidth=self.border_width),
            yaxis2=dict(linecolor=self.border_color, linewidth=self.border_width),
            showlegend=True,
            legend=dict(orientation='h', y=1.1, font=dict(color=self.legend_text_color))
        )
        if self.hovermode:
            fig.update_layout(hovermode='x unified')
        fig.update_traces(line=dict(width=1.5), selector=dict(type='candlestick'))
        fig.update_layout(
            xaxis=dict(
                title_font=self.axis_font,
                tickfont=self.axis_font,
                rangeslider=dict(visible=self.rangeslider_visible),
                showticklabels=False,
                showline=False
            ),
            yaxis=dict(
                title_font=self.axis_font,
                tickfont=self.axis_font,
                showticklabels=True,
                showline=False
            ),
        )
        fig.update_xaxes(
            zeroline=False,
            gridcolor=self.grid_color
        )
        fig.update_yaxes(
            zeroline=False,
            gridcolor=self.grid_color
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
        tradingview_style = TradingViewPlotter(df)
        num_rows = len(indicator_traces) + 2
        row_heights = [
            0.2,
            0.2,
        ] + [0.2] * len(indicator_traces)
        row_heights += [0.2] * (2 - len(row_heights))
        margin = dict(l=10, r=10, t=30, b=10, pad=0)
        fig = make_subplots(
            rows=num_rows, cols=1, shared_xaxes=True, row_heights=row_heights,
            vertical_spacing=0.02, subplot_titles=[None] * num_rows, row_titles=[None] * num_rows
        )
        candlestick_data = df if candlestick_data is None else candlestick_data
        candlestick_data = self.forward_fill_missing_data(df, candlestick_data, ['open', 'high', 'low', 'close'])
        breaking_traces = BreakingTrendIndicator(df)
        breaking_traces = breaking_traces.get_breaking_traces()
        if all(col in candlestick_data.columns for col in ['open', 'high', 'low', 'close']):
            candlestick_trace = go.Candlestick(
                x=candlestick_data['ctmString'],
                open=candlestick_data['open'],
                high=candlestick_data['high'],
                low=candlestick_data['low'],
                close=candlestick_data['close'],
                name='Candlestick Chart',
            )
            fig.add_trace(candlestick_trace, row=1, col=1)
        else:
            raise KeyError("Columns 'open', 'high', 'low', 'close' not found in candlestick_data")
        fig = tradingview_style.apply_tradingview_style(fig)
        
        for i, optional_indicator_list in enumerate(optional_indicators, start=2):
            for j, optional_indicator_trace in enumerate(optional_indicator_list, start=1):
                if len(optional_indicator_trace.x) > len(candlestick_data):
                    optional_indicator_trace.x = optional_indicator_trace.x[:len(candlestick_data)]
                    optional_indicator_trace.y = optional_indicator_trace.y[:len(candlestick_data)]
                fig.add_trace(optional_indicator_trace, row=1, col=1)
                if j == 1:
                    label_text = f'Number of Items in {optional_indicator_trace.name}: {len(optional_indicator_trace.x)}'
                    label_annotation = go.layout.Annotation(
                        text=label_text,
                        showarrow=False,
                        xref='paper',
                        yref='paper',
                        x=0.5,
                        y=1.05 - 0.1 * (i - 2),
                        xanchor='center',
                        yanchor='bottom',
                        font=dict(size=14, color='white'),
                    )
                    fig.add_annotation(label_annotation, row=1, col=1)
            
            
        for i, indicator_trace_list in enumerate(indicator_traces, start=2):
            for j, indicator_trace in enumerate(indicator_trace_list, start=1):
                if not isinstance(indicator_trace, int):
                    if hasattr(indicator_trace, 'x') and hasattr(indicator_trace, 'y'):
                        if isinstance(indicator_trace.x, np.ndarray) and len(indicator_trace.x) > len(candlestick_data):
                            indicator_trace.x = indicator_trace.x[:len(candlestick_data)]
                            indicator_trace.y = indicator_trace.y[:len(candlestick_data)]
                        fig.add_trace(indicator_trace, row=i, col=1)
                if j == 1:
                    label_text = f'Number of Items in {indicator_trace.name}: {len(indicator_trace.x)}'
                    label_annotation = go.layout.Annotation(
                        text=label_text,
                        showarrow=False,
                        xref='paper',
                        yref='paper',
                        x=0.5,
                        y=1.05 - 0.1 * (i - 2),
                        xanchor='center',
                        yanchor='bottom',
                        font=dict(size=14, color='white'),
                    )
                    fig.add_annotation(label_annotation, row=i, col=1)
        fig.update_layout(
            xaxis=dict(showline=False, linewidth=0),
            yaxis=dict(showline=False, linewidth=0),
            xaxis2=dict(showline=False, linewidth=0),
            yaxis2=dict(showline=False, linewidth=0),
            showlegend=True,
            legend=dict(orientation='h', y=1.1, font=dict(color='white'))
        )
        volume_data = df if volume_data is None else volume_data
        volume_data = self.forward_fill_missing_data(df, volume_data, ['volume'])
        if 'volume' in volume_data.columns:
            volume_trace = go.Bar(x=volume_data['ctmString'], y=volume_data['volume'], marker_color='blue', name='Volume Chart')
            fig.add_trace(volume_trace, row=num_rows, col=1)
            fig.update_xaxes(showticklabels=False, row=num_rows, col=1)
        else:
            raise KeyError("Column 'volume' not found in volume_data")
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
            font=dict(size=14, color='white'),
        )
        fig.add_annotation(label_annotation)
        buttons = [
            dict(label=f'{num} Candles', method='relayout', args=[{'xaxis.range': [df['ctmString'].iloc[max(0, -num)], df['ctmString'].iloc[-1]]}])
            for num in num_candles_buttons
        ]
        fig.update_layout(margin=margin)
        fig.update_layout(updatemenus=[dict(type='buttons', showactive=False, buttons=buttons)])
        rangebreaks = [
            dict(bounds=['sat', 'mon']),
        ]
        fig.update_xaxes(
            type='category',
            rangebreaks=rangebreaks
        )
        fig.show()

    def forward_fill_missing_data(self, df, data, column_names):
        merged_data = df.merge(data, on='ctmString', how='left', suffixes=('_df', '_data'))
        for col in column_names:
            if f'{col}_data' in merged_data.columns:
                merged_data[f'{col}_data'].ffill(inplace=True)
                merged_data[col] = merged_data[f'{col}_data']
                merged_data.drop(columns=[f'{col}_data'], inplace=True)
            else:
                raise KeyError(f"Column '{col}' not found in the merged data")
        return merged_data