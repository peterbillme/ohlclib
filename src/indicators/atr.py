import pandas as pd
import talib
from yahoo_fin.stock_info import get_data


def atr(data: pd.DataFrame, period: int, factor=1):
    data[f"atr_{period}"] = talib.ATR(data["high"], data["low"], data["close"], timeperiod=period) * factor


def tr(data: pd.DataFrame, factor=1):
    data["tr"] = talib.TRANGE(data["high"], data["low"], data["close"]) * factor


if __name__ == '__main__':
    pd.options.display.max_rows = 2000
    pd.options.display.max_columns = 200
    pd.set_option('max_colwidth', 120)
    pd.options.display.width = 2080

    _hist_data = get_data('tsla', interval="1d")

    atr(data=_hist_data, period=21, factor=1)
    # tr(data=_hist_data, factor=1)

    print(_hist_data.tail(10))
