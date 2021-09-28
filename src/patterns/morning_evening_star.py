import pandas as pd
from yahoo_fin.stock_info import get_data


def morning_evening_star(data: pd.DataFrame):
    """
    Morning star or Evening star
    Please note, this my morning and evening star, quite different to common concept, but I feel it is much better!
    Positive values are morning stars, negative values are evening stars, 0 means nothing.
    Rule: bar[0],bar[1],bar[2] are combined, calculate whether they are hammers
    """
    # Calculate highest and lowest for recent 3 candles
    __data = data.copy()
    __data["high3"] = __data.high.rolling(window=3).apply(lambda ser: max(ser))
    __data["low3"] = __data.low.rolling(window=3).apply(lambda ser: min(ser))
    __data["open3"] = __data.open.rolling(window=3).apply(lambda ser: ser[0])

    def cal(ser):
        result = 0
        delta = abs(ser.open3 - ser.close)
        upper_shadow = ser.high3 - max(ser.open3, ser.close)
        lower_shadow = min(ser.open3, ser.close) - ser.low3
        if upper_shadow > 0 and delta > 0 and ser.close > ser.open3 and ser.close > ser.open:
            if lower_shadow/upper_shadow > 2:
                # Lower shadow is twice to upper shadow，possibly long
                rr = lower_shadow / delta
                result = rr if rr > 1 else 0
        if lower_shadow > 0 and delta > 0 and ser.close < ser.open3 and ser.close < ser.open:
            if upper_shadow/lower_shadow > 2:
                # short
                rr = upper_shadow / delta
                result = -rr if rr > 1 else 0

        # example: msft, 1d, march 22, 2021
        # if ser.close > ser.open3:
        #     result = 1
        # if ser.close < ser.open3:
        #     result = -1

        return result

    data["morning_evening_star"] = __data.apply(cal, axis=1)


if __name__ == '__main__':
    pd.options.display.max_rows = 800
    pd.options.display.max_columns = 200
    pd.set_option('max_colwidth', 120)
    pd.options.display.width = 2080

    _hist_data = get_data('msft', interval="1d")
    morning_evening_star(data=_hist_data)

    print(_hist_data.tail(800))
