"""
Recognize Bullish/Bearish Engulfing Pattern
"""
import pandas as pd
from yahoo_fin.stock_info import get_data


def engulfing(data: pd.DataFrame):
    """
    engulfing
    Positive numbers are multi-side, negative numbers are short-side
    0 is abnormal, meaning that the ratio of the absolute value of the current Candle up or down to the previous one is more than 10 times.
    For machine learning convenience, a floating point number should be returned to indicate the strength of the engulfing,
    in preparation for the final Machine Learning normalization.
    """

    def cal(ser):
        result = 0
        if ser.raise_0 > 0 >= ser.raise_1 and ser.open <= ser.close_1 and ser.close >= ser.open_1:
            # Current candle is going up，long
            rr = abs(ser.raise_0) / abs(ser.raise_1) if 0 > ser.raise_1 else ser.raise_0/ser.avg_5_change_abs
            result = rr if rr > 1 else 0
        elif ser.raise_0 < 0 < ser.raise_1 and ser.open >= ser.close_1 and ser.close <= ser.open_1:
            # Current candle is going down, short
            rr = abs(ser.raise_0) / abs(ser.raise_1) if 0 < ser.raise_1 else ser.raise_0/ser.avg_5_change_abs
            result = -rr if rr > 1 else 0

        return result

    data_copy = data.copy()
    data_copy["raise_0"] = data_copy["close"] - data_copy["open"]
    data_copy["raise_1"] = data_copy["raise_0"].shift(1)
    data_copy["open_1"] = data_copy["open"].shift(1)
    data_copy["close_1"] = data_copy["close"].shift(1)
    # get recent 5 average price change, in order to calculate if prev day price is zero change, we still won't miss it
    data_copy["avg_5_change_abs"] = data_copy.raise_0.rolling(window=5).apply(lambda ser: ser.abs().mean())

    data_copy["engulfing"] = data_copy[["raise_0", "raise_1", "open", "open_1", "close", "close_1", "avg_5_change_abs"]].apply(cal, axis=1)
    # print(data_copy.query("raise_1==0").tail(20))
    data["engulfing"] = data_copy["engulfing"]


if __name__ == '__main__':
    pd.options.display.max_rows = 200
    pd.options.display.max_columns = 200
    pd.set_option('max_colwidth', 120)
    pd.options.display.width = 2080

    _hist_data = get_data('msft', interval="1d")
    engulfing(data=_hist_data)

    print(_hist_data.tail(20))
