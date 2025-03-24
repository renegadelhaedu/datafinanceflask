import numpy as np

def betaIndicator(dataStock, dataMarket, logReturns=True):

    if not logReturns:
      dataStock['RETURNS'] = dataStock['Close'].pct_change()
      dataMarket['RETURNS'] = dataMarket['Close'].pct_change()
    else:
      dataStock['RETURNS'] = np.log(dataStock['Close'] / dataStock['Close'].shift(1))
      dataMarket['RETURNS'] = np.log(dataMarket['Close'] / dataMarket['Close'].shift(1))

    stock_returns, market_returns = dataStock.align(dataMarket, join='inner')

    cor_stock_market = np.cov(stock_returns['RETURNS'].dropna(), market_returns['RETURNS'].dropna(), ddof=1)

    beta = cor_stock_market[0, 1] / cor_stock_market[1, 1]

    return beta