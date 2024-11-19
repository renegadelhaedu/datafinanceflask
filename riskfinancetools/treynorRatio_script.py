from .betaIndicator_script import betaIndicator
import numpy as np

def treynorRatioIndicator(dataStock, beta, riskfreeRate):
    dataStock['RETURNS'] = dataStock['Adj Close'].pct_change().dropna()
    returns = dataStock['returns'].dropna()
    meanReturnStock = np.mean(returns)
    
    risk_free_rate = riskfreeRate / 100
    returnRiskFreePerDay = (1 + risk_free_rate) ** (1 / 252) - 1

    treynor_ratio = (((meanReturnStock * 100) - (returnRiskFreePerDay * 100)) / beta) * np.sqrt(252)
    return treynor_ratio

