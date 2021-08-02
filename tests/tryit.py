import os
import pathlib

from yahoo_fin.stock_info import get_data, tickers_sp500
import pandas as pd

from indicators.ema import ema_in_order
from indicators.kd import kd
from indicators.macd import macd, macd_increasing


def get_pickle_file_name(symbol, interval):
    _script_folder = pathlib.Path().absolute()
    _pickle_folder = os.path.join(_script_folder, "pickle", "quotes")
    os.makedirs(_pickle_folder, exist_ok=True)
    _pickle_file = os.path.join(_pickle_folder, f"{symbol}_{interval}.pkl")

    return _pickle_file


def load_quotes(symbol, interval):
    _df = pd.read_pickle(get_pickle_file_name(symbol, interval))
    _df_adj = _df[["ticker", "adjopen", "adjhigh", "adjlow", "adjclose"]]
    _df_adj.columns = ["ticker", "open", "high", "low", "close"]
    return _df[["ticker", "open", "high", "low", "close"]].dropna(), _df_adj.dropna()


def update_quotes_pickle(symbol, interval):
    hist_data = get_data(symbol, interval=interval)
    hist_data["adj_ratio"] = hist_data["adjclose"] / hist_data["close"]
    hist_data["adjopen"] = hist_data["open"] * hist_data["adj_ratio"]
    hist_data["adjhigh"] = hist_data["high"] * hist_data["adj_ratio"]
    hist_data["adjlow"] = hist_data["low"] * hist_data["adj_ratio"]

    df: pd.DataFrame = hist_data[
        ['ticker', 'open', 'high', 'low', 'close', 'adjopen', 'adjhigh', 'adjlow', 'adjclose', 'volume']]
    # target_path =
    df.to_pickle(get_pickle_file_name(symbol, interval))


def update_quotes_spx500():
    _spx500_tickers = tickers_sp500(True)
    _num_total = _spx500_tickers.shape[0]
    _i = 1
    for _row in _spx500_tickers.itertuples():
        print(f"Updating {_row.Symbol}({_i}/{_num_total}) ...")

        update_quotes_pickle(_row.Symbol, '1d')
        print("Interval 1d done.")
        update_quotes_pickle(_row.Symbol, '1wk')
        print("Interval 1wk done.")
        update_quotes_pickle(_row.Symbol, '1mo')
        print("Interval 1mo done.")

        print("**** All Done! ****\n")
        _i += 1


def filter_1wk():
    spx500_tickers = tickers_sp500(True)
    num_total = spx500_tickers.shape[0]
    i = 1
    result = []
    for _row in spx500_tickers.itertuples():
        print(f"\nChecking {_row.Symbol}({i}/{num_total}) ...")

        df, df_adj = load_quotes(_row.Symbol, '1wk')
        # ema_in_order(data=df_adj, periods=[60, 120, 288, 338, 420])
        kd(data=df_adj, discrete=False)
        macd(df_adj)
        macd_increasing(data=df_adj)
        dd = df_adj.iloc[-1, :]

        if dd.k >= 80 and dd.macd > 0 and dd.macd_increasing_2 == 1:
            # print(f"    {row.Symbol}: k: {dd.k}")
            result.append(_row.Symbol)
        i += 1

    return pd.DataFrame(result, columns=["symbol"])


def filter_1mo(symbols):
    num_total = len(symbols)
    i = 1
    result = []
    for s in symbols:
        print(f"\nChecking {s}({i}/{num_total}) ...")

        df, df_adj = load_quotes(s, '1mo')
        kd(data=df_adj, discrete=False)
        macd_increasing(data=df_adj)
        dd = df_adj.iloc[-1, :]

        if dd.k >= 60 and dd.macd_increasing_2 == 1:
            # print(f"    {s}: k: {dd.k}")
            result.append(s)
        i += 1

    return pd.DataFrame(result, columns=["symbol"]).dropna()


if __name__ == '__main__':
    pd.options.display.max_rows = 200
    pd.options.display.max_columns = 200
    pd.set_option('max_colwidth', 120)
    pd.options.display.width = 2080

    # update_quotes_spx500()
    # exit()

    print("checking 1wk ...")
    # wk_result = filter_1wk()
    # wk_result.to_pickle(get_pickle_file_name("result", "1wk"))
    wk_result = pd.read_pickle(get_pickle_file_name("result", "1wk"))
    print(wk_result)

    print("checking 1mo ...")
    mo_result = filter_1mo(wk_result["symbol"].tolist())

    print(mo_result)
    print(len(mo_result))

    # load 1wk in order to sort by kd
    result_final = []
    for row in mo_result.itertuples():
        df, df_adj = load_quotes(row.symbol, '1wk')
        kd(data=df_adj, discrete=False)
        result_final.append(df_adj.iloc[-1, :])

    df = pd.DataFrame(result_final).sort_values(by=["k"])
    print(df.to_excel("2021-08-01-spx500-results.xlsx"))

