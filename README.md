# ohlc-technical
This project offers technical functions based on OHLC data for any time series price candle stick data.

I decide to gradually migrate my private quantum functions to public!

# requirements
- ta-lib
> This project uses a lot of ta-lib functions to calculate indicators.  
> I prepared a convenient script for you to install ta-lib.   
> It will first install numpy and then followed by a series of command to install ta-lib.  
> Please run scripts/install_talib.sh to install talib for your convenience.
- yahoo_fin
> [Official documentation](http://theautomatic.net/yahoo_fin-documentation/)

# License
> [MIT License](LICENSE)

# Features:
- Indicators
- [x] Bias
- [x] Ema
- [x] Stochastic(kd)
- [x] macd

- Patterns
- [x] Engulfing
- [x] Hammer
- [x] Morning and Evening star

- Automation
- [ ] Find a solution to store OHLC data for US stock market
- [ ] Pipeline to update OHLC daily to database
- [ ] Pipeline to update Indicators
- [ ] Pipeline to update Patterns

- Machine learning
- [ ] Random forest algorithm to predict future price

- MISC
- [ ] Release in pypi
