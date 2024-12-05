import dataAnalise as da
import json
import pandas as pd
import time
import yfinance as yf
import dao
import pathlib
from datetime import datetime
from riskfinancetools.filtering import filtering

#print(pathlib.Path('data/statusinvest-busca-avancada.csv').resolve())

#da.calcularRiscoRetJanelasTemp('minhas').to_pickle('data/riscoRetornoMinhas.pkl')
#da.calcularRiscoRetJanelasTemp('all').to_pickle('data/riscoRetornoAll.pkl')
#start = '2020-01-01'
#currentDate = datetime.now()
#end = f'{str(currentDate.year)}-{str(currentDate.month)}-{str(currentDate.day)}'
#filtering('data/statusinvest-busca-avancada.csv', startDate=start, endDate=end)

# import yfinance as yf
# tickers = ["GOLL4.SA", "AZUL4.SA", "RAIL3.SA"]
# for ticker in tickers:
#     data = yf.download(ticker, start="2022-01-01", end="2024-11-19")
#     print(f"{ticker}: {data.shape}")

#dados = da.gerarcorrelacaoindividual('bbas3', 'selic')
#print(dados[0])

#da.gerarCorrelacoesCarteiraXindMacro(dao.getAcoesListadas()).to_pickle('data/correlacoesIndMacroAll.pkl')

#da.gerarrankingdividendos(dao.getMinhasEmpresasListadas()).to_pickle('data/rankingdividendosMinhas.pkl')
#da.gerarrankingdividendos(dao.getEmpresasListadasAntigas()).to_pickle('data/rankingdividendosAll.pkl')
#print(da.readRankingDividendos('all'))
#print(da.readRankingDividendos('minhas'))

def filtrar_acoes():
    dados = pd.read_csv('data//statusinvest-busca-avancada.csv', decimal=",", delimiter=";", thousands=".")
    dados = dados.fillna(0)

    dados.drop(dados[dados['PRECO'] <= 0].index, inplace=True)
    dados.drop(dados[dados[' LIQUIDEZ MEDIA DIARIA'] < 500000].index, inplace=True)
    acoesInclusas = []

    for ticket in dados['TICKER']:
        if len(yf.Ticker(ticket + '.sa').history()) > 0:
            acoesInclusas.append(ticket)
    return acoesInclusas

#dataCorr = pd.read_pickle('data/correlacoesIndMacroAll.pkl')
#print(dataCorr[dataCorr.index.isin(dao.getMinhasEmpresasListadas())])

#da.processarAnalise().to_pickle('data/filtragem_acoes.pkl')


