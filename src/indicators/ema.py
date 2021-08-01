import numpy as np
import pandas as pd
import talib


def ema(data: pd.DataFrame, periods: [] = None, apply_to="close", column_name_prefix=None):
    """
    Attach ema to given dataframe. Column names will be [column_name_prefix_]ema_[period]_[apply_to]
    :param data:
    :param periods:
    :param apply_to: Calculate ema on which which price. Example, if apply_to='open', then function will return new column named '[column_name_prefix]_ema_open'
    :param column_name_prefix:
    :return:
    """
    if periods is not None:
        for period in periods:
            col_name = f"{column_name_prefix}_ema_{period}_{apply_to}" \
                if column_name_prefix is not None else f"ema_{period}_{apply_to}"
            data[col_name] = talib.EMA(data[apply_to], timeperiod=period)


def ema_in_order(data: pd.DataFrame, periods: [] = None, apply_to="close", keep_ema=True, column_name_prefix=None):
    """
    Check if many ema lines are in order
    Going up, then return 1, going down then return -1 else return 0
    :param data: given data. has to include open, high, low, close columns.
    :param periods: given periods has to be in order of asc
    :param apply_to: which price to be applied
    :param keep_ema: does result dataframe keep ema data
    :param column_name_prefix:
    :return:
    """
    _data = data.copy()
    ema(data=_data, periods=periods, apply_to=apply_to, column_name_prefix=column_name_prefix)

    # condition 1 and 2
    cond_1 = True
    cond_2 = True
    for i in range(len(periods) - 1):
        ema_1 = f"{column_name_prefix}_ema_{periods[i]}_{apply_to}" \
            if column_name_prefix is not None else f"ema_{periods[i]}_{apply_to}"
        ema_2 = f"{column_name_prefix}_ema_{periods[i + 1]}_{apply_to}" \
            if column_name_prefix is not None else f"ema_{periods[i + 1]}_{apply_to}"
        cond_1 = cond_1 & (_data[ema_1] > _data[ema_2])
        cond_2 = cond_2 & (_data[ema_1] < _data[ema_2])

    conditions = [cond_1, cond_2]
    choices = [1, -1]
    if keep_ema:
        columns = []
        for period in periods:
            col_name = f"{column_name_prefix}_ema_{period}_{apply_to}" if column_name_prefix is not None else f"ema_{period}_{apply_to}"
            columns.append(col_name)
        data[columns] = _data[columns]
    column_name = f"{column_name_prefix}_ema_in_order" if column_name_prefix is not None else f"ema_in_order"
    data[column_name] = np.select(conditions, choices, default=0)
