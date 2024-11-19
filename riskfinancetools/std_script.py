import numpy as np

def standardDerivation(data):
  data['returns'] = data['Adj Close'].pct_change()
  stdTickerStock = np.std(data['returns'])

  return stdTickerStock