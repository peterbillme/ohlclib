import pandas as pd
from yahoo_fin.stock_info import get_data


def hammer(data: pd.DataFrame):
    """
    hammer
    Positives are long, Negatives are short
    For machine learning convenience, a floating point number should be returned to indicate the strength of the engulfing,
    in preparation for the final Machine Learning normalization.
    """

    def cal(ser):
        result = 0
        if abs(ser.open - ser.close) > abs(ser.high - max(ser.open, ser.close)):
            # 上影线比实体短，可能为多方
            rr = (min(ser.open, ser.close) - ser.low) / abs(ser.close - ser.open)
            result = rr if rr > 1 else 0
        elif abs(ser.open - ser.close) > abs(ser.low - min(ser.open, ser.close)):
            # 下影线比实体短，可能为空方
            rr = abs(ser.high - max(ser.open, ser.close)) / abs(ser.close - ser.open)
            result = -rr if rr > 1 else 0

        return result

    data["hammer"] = data.apply(cal, axis=1)


if __name__ == '__main__':
    pd.options.display.max_rows = 800
    pd.options.display.max_columns = 200
    pd.set_option('max_colwidth', 120)
    pd.options.display.width = 2080

    _hist_data = get_data('msft', interval="1d")
    hammer(data=_hist_data)

    print(_hist_data.tail(40))
