import dataAnalise as da
import json
import pandas as pd
import time
import yfinance as yf
import dao
import pathlib
from datetime import datetime
from riskfinancetools.filtering import filtering

print(pathlib.Path('data/statusinvest-busca-avancada.csv').resolve())

#da.calcularRiscoRetJanelasTemp('minhas').to_pickle('data/riscoRetornoMinhas.pkl')
#da.calcularRiscoRetJanelasTemp('all').to_pickle('data/riscoRetornoAll.pkl')
start = '2020-01-01'
currentDate = datetime.now()
end = f'{str(currentDate.year)}-{str(currentDate.month)}-{str(currentDate.day)}'
filtering('data/statusinvest-busca-avancada.csv', startDate=start, endDate=end)

# import yfinance as yf
# tickers = ["GOLL4.SA", "AZUL4.SA", "RAIL3.SA"]
# for ticker in tickers:
#     data = yf.download(ticker, start="2022-01-01", end="2024-11-19")
#     print(f"{ticker}: {data.shape}")

#dados = da.gerarcorrelacaoindividual('bbas3', 'selic')
#print(dados[0])

#da.gerarCorrelaAll('all').to_pickle('data/correlacoesIndAll3D.pkl')

#da.gerarrankingdividendos(dao.getMinhasEmpresasListadas()).to_pickle('data/rankingdividendosMinhas.pkl')
#da.gerarrankingdividendos(dao.getEmpresasListadasAntigas()).to_pickle('data/rankingdividendosAll.pkl')
#print(da.readRankingDividendos('all'))
#print(da.readRankingDividendos('minhas'))

