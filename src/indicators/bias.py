import pandas as pd
from yahoo_fin.stock_info import get_data

from indicators.ema import ema


def bias(data: pd.DataFrame, base_column, relative_column, bias_name):
    data[bias_name] = 100 * (data[base_column] - data[relative_column]) / data[relative_column]


if __name__ == '__main__':
    pd.options.display.max_rows = 200
    pd.options.display.max_columns = 200
    pd.set_option('max_colwidth', 120)
    pd.options.display.width = 2080

    _hist_data = get_data('tsla', interval="1d")

    ema(data=_hist_data, periods=[20, 60, 120])

    bias(data=_hist_data, base_column='close', relative_column='ema_20_close', bias_name='bias_close_20')
    bias(data=_hist_data, base_column='ema_20_close', relative_column='ema_60_close', bias_name='bias_20_60')
    bias(data=_hist_data, base_column='ema_60_close', relative_column='ema_120_close', bias_name='bias_60_120')

    print(_hist_data)
