import os


def get_script_path():
    return os.getcwd()


def get_pickle_file_name(symbol, interval):
    _script_folder = get_script_path()
    _pickle_folder = os.path.join(_script_folder, "pickle", "quotes")
    os.makedirs(_pickle_folder, exist_ok=True)
    _pickle_file = os.path.join(_pickle_folder, f"{symbol}_{interval}.pkl")

    return _pickle_file
