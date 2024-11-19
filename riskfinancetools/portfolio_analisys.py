
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
        currentYear = start[:4]

    riskFreeRate = quotation(currentYear)
    print(riskFreeRate)

    print("BAIXANDO DADOS MERCADO")
    dataMarket = yf.download(market, start=start, end=end)

    for stock in wallet:
        print(f"BAIXANDO DADOS AÇÃO {stock}")

        if ".SA" not in str(stock):
            stock = stock + '.SA'
        
        dataStock = yf.download(stock, start=start, end=end)

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
        data.to_csv('CSV/stocksData.csv', index=False)

    return data

if __name__ == '__main__':
    wallet = ['VALE3.SA', 'PETR4.SA', 'ITUB4.SA', 'BBDC4.SA', 'ABEV3.SA', 'MGLU3.SA', 
           'WEGE3.SA', 'JBSS3.SA', 'SUZB3.SA', 'TAEE11.SA', 'PRIO3.SA']
    market = '^BVSP'
    startDate = '2022-01-01'
    endDate = '2024-09-01'

    wallet = walletAnalisys(wallet, market, startDate, endDate)

    print(wallet)
    # VALE3 - Vale S.A. (Mineração)
    # PETR4 - Petrobras (Petróleo e Gás)
    # ITUB4 - Itaú Unibanco (Bancos)
    # BBDC4 - Bradesco (Bancos)
    # ABEV3 - Ambev (Bebidas)
    # MGLU3 - Magazine Luiza (Varejo)
    # WEGE3 - WEG (Máquinas e Equipamentos)
    # JBSS3 - JBS (Alimentos)
    # SUZB3 - Suzano (Papel e Celulose)
    # TAEE11 - Taesa (Energia Elétrica)