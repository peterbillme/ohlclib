"""
This module is made for convenience to get quotes using yahoo_fin.
"""
import time
from concurrent import futures

import pandas as pd
from yahoo_fin.stock_info import get_data, tickers_sp500
from utils.paths import get_pickle_file_name


def load_quotes(symbol, interval):
    """
    :param symbol:
    :param interval:
    :return:
    first element is the regular OHLC series, second element is adjusted OHLC series.
    """
    _df = pd.read_pickle(get_pickle_file_name(symbol, interval))
    _df_adj = _df[["ticker", "adjopen", "adjhigh", "adjlow", "adjclose"]]
    _df_adj.columns = ["ticker", "open", "high", "low", "close"]
    return _df[["ticker", "open", "high", "low", "close"]].dropna(), _df_adj.dropna()


def update_quotes_pickle(symbol, interval):
    print(f"Fetching {symbol}({interval}) ...")
    hist_data = get_data(symbol, interval=interval)
    print(f"Fetching {symbol}({interval}) Done.\n")
    hist_data["adj_ratio"] = hist_data["adjclose"] / hist_data["close"]
    hist_data["adjopen"] = hist_data["open"] * hist_data["adj_ratio"]
    hist_data["adjhigh"] = hist_data["high"] * hist_data["adj_ratio"]
    hist_data["adjlow"] = hist_data["low"] * hist_data["adj_ratio"]

    _df: pd.DataFrame = hist_data[
        ['ticker', 'open', 'high', 'low', 'close', 'adjopen', 'adjhigh', 'adjlow', 'adjclose', 'volume']]

    _df.to_pickle(get_pickle_file_name(symbol, interval))


def update_quotes_spx500():
    _spx500_tickers = tickers_sp500(True)["Symbol"].tolist()

    # Retrieve a single page and report the URL and contents
    def update_quotes(symbol):
        _result = ""
        ok = False
        while not ok:
            try:
                update_quotes_pickle(symbol, '1d')
                update_quotes_pickle(symbol, '1wk')
                update_quotes_pickle(symbol, '1mo')
                _result = f"{symbol} quotes downloaded!"
            except Exception as _exc:
                _result = f"Error({symbol}): generated an exception: {_exc}, will try again in 1 second."
                time.sleep(1)
            else:
                ok = True

        return _result

    # We can use a with statement to ensure threads are cleaned up promptly
    with futures.ThreadPoolExecutor(max_workers=5) as executor:
        update_results = {executor.submit(update_quotes, symbol): symbol for symbol in _spx500_tickers}
        for future in futures.as_completed(update_results):
            result = update_results[future]
            try:
                data = future.result()
            except Exception as exc:
                print('%r generated an exception: %s' % (result, exc))
            else:
                print('%r : %s' % (result, data))
