#!/bin/bash

# install build-essential
sudo apt install build-essential

# install numpy
pip install numpy

# install ta-lib
wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz
tar xzvf ta-lib-0.4.0-src.tar.gz
cd ta-lib || exit 0
./configure --prefix=/usr
make
sudo make install
cd ..
rm -rf ta-lib*

wget https://files.pythonhosted.org/packages/90/05/d4c6a778d7a7de0be366bc4a850b4ffaeac2abad927f95fa8ba6f355a082/TA-Lib-0.4.17.tar.gz
tar xvf TA-Lib-0.4.17.tar.gz
cd TA-Lib-0.4.17 || exit 0
python setup.py install
cd ..
rm -rf TA-Lib-0.4.17*

# check install
python -c "import talib; print(talib.__version__)"