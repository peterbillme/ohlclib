"""
Functions to calculate stochastic.
"""

import pandas as pd
import talib


def kd(data: pd.DataFrame, column_name_prefix=None, shift_periods=0, discrete=True,
       fastk_period=5, slowk_period=3, slowd_period=3, slowk_matype=0, slowd_matype=0):
    """
    Attach stochastic columns.
    slowk_matype:
        Simple = 0
        Exponential = 1
        Smoothed = 2
        Linear_Weighted = 3
    :param data:
    :param column_name_prefix:
    :param shift_periods:
    :param discrete:
    :param fastk_period:
    :param slowk_period:
    :param slowd_period:
    :param slowk_matype:
    :param slowd_matype:
    :return:
    """
    _data = data.copy()
    k_column = f"{column_name_prefix}_k" if column_name_prefix is not None else "k"
    d_column = f"{column_name_prefix}_d" if column_name_prefix is not None else "d"

    _data[k_column], _data[d_column] = talib.STOCH(_data.high,
                                                   _data.low,
                                                   _data.close,
                                                   fastk_period=fastk_period,
                                                   slowk_period=slowk_period,
                                                   slowk_matype=slowk_matype,
                                                   slowd_period=slowd_period,
                                                   slowd_matype=slowd_matype)
    if shift_periods != 0:
        if discrete:
            data[k_column] = _data[k_column].shift(shift_periods).fillna(0).astype(int)
            data[d_column] = _data[d_column].shift(shift_periods).fillna(0).astype(int)
        else:
            data[k_column] = _data[k_column].shift(shift_periods)
            data[d_column] = _data[d_column].shift(shift_periods)
    else:
        if discrete:
            data[k_column] = _data[k_column].fillna(0).astype(int)
            data[d_column] = _data[d_column].fillna(0).astype(int)
        else:
            data[k_column] = _data[k_column]
            data[d_column] = _data[d_column]
