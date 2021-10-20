import pandas as pd


def price_breakthrough(data: pd.DataFrame, period=15):
    """
    Price change
    The ratio of the absolute value of the current candle price change to the average absolute value of the last N candles.
    Positive if the current candle is up, negative if it is down.
    Ideally normalize it while use in machine learning.
    :param period:
    :param data:
    :return:
    """

    def cal(ser):
        result = ser[-1] / ser.mean()
        return result

    c_name = f"breakthrough_{period}"
    # produce tmp DataFrame
    __data = data.copy()
    # calculate abs price change
    __data["tmp_r"] = abs(__data["close"] - __data["open"])
    __data["up_or_down"] = __data.apply(lambda ser: 1 if (ser.close - ser.open) > 0 else -1 if (ser.close - ser.open) < 0 else 0, axis=1)

    # copy result
    data[c_name] = __data.tmp_r.rolling(window=period, axis=0).apply(cal, raw=True) * __data.up_or_down
