# Python module for downloading time series data
This repository gets data from the Alpha Vantage API: https://www.alphavantage.co/.
You need an API key in order to use the utilities in this repo. 

You can retrieve price data from many stocks traded in stock markets.

## Load Data
To use this module, you will need to have your own
Alpha Vantage API key.
```
from loaders import loader

data_loader = loader.LoaderAlphaV(symbol="AAPL", interval=1)

df = data_loader.ts_intraday()

df_ext = data_loader.ts_intraday_extended(interval='5min&slice=year1month5')
```

## Packaging
For details on packaging and folder structure, see the link https://packaging.python.org/en/latest/tutorials/packaging-projects/

On windows, install latest version of pip:
```
py -m pip install --ugrade pip
```
Create distribution package, make sure you have latest PyPA's build installed
```
py -m pip install --upgrade build
```
Build
```
py -m build
```
You need to have Twine installed:
```
py -m pip install --upgrade twine
```

To publish on PyPi do the following:
```
twine upload dist/*
```
Install your newly created packege with:
```
python3 -m pip install [your-package]
```


For publishing in Test PyPI do the following:
```
py -m pip install --index-url https://test.pypi.org/simple/ --no-deps example-package-YOUR-USERNAME-HERE
```


