import pandas as pd
import yfinance as yf
from dao import *

def gerarPercentuais():
    cart = getCarteira()
    tikers = list(map(lambda x: x + '.SA', list(cart.keys())))

    data = yf.download(tikers)
    data.ffill(inplace=True)

    qtdeTik = pd.DataFrame.from_dict(cart, orient='index', columns=['qtde'])
    qtdeTik.sort_index(inplace=True)
    todayCot = pd.DataFrame(data['Adj Close'].iloc[-1])
    todayCot.columns = ['cota']

    qtdeTik['valor'] = qtdeTik['qtde'].values * todayCot['cota'].values
    total = qtdeTik['valor'].sum()
    qtdeTik['perc'] = round((qtdeTik['valor'] / total) * 100, 1)
    qtdeTik.sort_values(by=['perc'], ascending=False, inplace=True)

#    cotChg = [round(x, 2) for x in list((data['Adj Close'].pct_change() * 100).iloc[-1])]
#    cotAtual = [round(x, 2) for x in list(data['Adj Close'].iloc[-1])]
#    tickers = [x.replace('.SA', '') for x in list(data['Adj Close'].columns)]

    grid = pd.concat([(data['Adj Close'].pct_change() * 100).iloc[-1], data['Adj Close'].iloc[-1]], axis=1)
    grid.index = grid.index.str.replace('.SA', '', regex=False)
    grid.reset_index(inplace=True)
    grid = grid.round(2)

    return qtdeTik.to_dict()['perc'], grid.values.tolist()