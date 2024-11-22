
from .betaIndicator_script import betaIndicator
from .sharpeRatio_script import sharpeRatioIndicator
from .std_script import standardDerivation
from .treynorRatio_script import treynorRatioIndicator
from .taxa_selic import quotation
import pandas as pd
import yfinance as yf

def walletAnalisys(wallet, market, year=None, startDate=None, endDate=None, exportCsv=True):
    data = []

    if year is not None:
        start = f"{year}-01-01"
        end = f"{year}-12-31"
        currentYear = year
    else:
        start = startDate
        end = endDate
        currentYear = end[:4]

    riskFreeRate = quotation(currentYear)
    print(riskFreeRate)

    print("BAIXANDO DADOS MERCADO")
    dataMarket = yf.download(market, start=start, end=end)

    if isinstance(dataMarket.columns, pd.MultiIndex):
        dataMarket = dataMarket.loc[:, (slice(None), market)]
        dataMarket.columns = dataMarket.columns.droplevel(1)
    
    for stock in wallet:
        print(f"BAIXANDO DADOS AÇÃO {stock}")

        if ".SA" not in str(stock):
            stock = stock + '.SA'
        
        dataStock = yf.download(stock, start=start, end=end)

        if isinstance(dataStock.columns, pd.MultiIndex):
            dataStock = dataStock.loc[:, (slice(None), stock)]
            dataStock.columns = dataStock.columns.droplevel(1)
        
        try:
        
            std = standardDerivation(dataStock)
            beta = betaIndicator(dataStock, dataMarket)
            sharpe =sharpeRatioIndicator(dataStock, riskFreeRate)
            treynor =treynorRatioIndicator(dataStock, beta, riskFreeRate)
            
            data.append({
                'TICKER': stock,
                'STD': std,
                'BETA': beta,
                'SHARPE RATIO': sharpe,
                'TREYNOR RATIO': treynor
            })
        except Exception as e:
            print(f"Erro ao processar {stock}: {e}")

    data = pd.DataFrame(data)

    if exportCsv:
        data.to_csv('data/stocksData.csv', index=False)

    return data