import pandas as pd
import talib
from yahoo_fin.stock_info import get_data


def b_band(data, period=20, nbdevup=2.0, nbdevdn=2.0, column_name_prefix=None, matype=talib.MA_Type.SMA):
    column_upper = f'{column_name_prefix}_band_upper' if column_name_prefix is not None else 'band_upper'
    column_middle = f'{column_name_prefix}_band_middle' if column_name_prefix is not None else 'band_middle'
    column_lower = f'{column_name_prefix}_band_lower' if column_name_prefix is not None else 'band_lower'

    data[column_upper], data[column_middle], data[column_lower] = talib.BBANDS(
        data.close, timeperiod=period,
        nbdevup=nbdevup, nbdevdn=nbdevdn,
        matype=matype
    )


if __name__ == "__main__":
    pd.options.display.max_rows = 2000
    pd.options.display.max_columns = 200
    pd.set_option('max_colwidth', 120)
    pd.options.display.width = 2080

    data = get_data('tsla', interval="1d")
    hist_data = data.tail(500).copy()
    hist_data = hist_data.drop(columns=['close'])
    hist_data['close'] = hist_data['adjclose']
    b_band(data=hist_data)

    print(hist_data)