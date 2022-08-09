import pandas as pd
import talib
from yahoo_fin.stock_info import get_data


def rsi(data, period=14, apply_to="close"):
    data[f"rsi_{period}"] = talib.RSI(data[apply_to], timeperiod=period)


if __name__ == '__main__':
    pd.options.display.max_rows = 2000
    pd.options.display.max_columns = 200
    pd.set_option('max_colwidth', 120)
    pd.options.display.width = 2080

    data = get_data('tsla', interval="1d")
    hist_data = data.tail(300).copy()
    rsi(data=hist_data, period=14)
    # macd(data=hist_data)

    print(hist_data)
