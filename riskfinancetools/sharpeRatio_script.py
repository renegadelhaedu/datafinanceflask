import numpy as np

def sharpeRatioIndicator(data, riskFreeRate):
    data['returns'] = data['Close'].pct_change()
    returns = data['returns'].dropna()
    meanTickerStock = np.mean(returns)
    
    risk_free_rate = riskFreeRate / 100
    returnRiskFreePerDay = (1 + risk_free_rate) ** (1 / 252) - 1

    stdTickerStock = np.std(returns) 

    sharpeRatioStock = ((meanTickerStock - returnRiskFreePerDay) / stdTickerStock) * np.sqrt(252)
    return sharpeRatioStock