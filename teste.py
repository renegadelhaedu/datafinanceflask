import dataAnalise as da
import json
import pandas as pd
import time
import yfinance as yf
import dao
import pathlib

print(pathlib.Path('data/statusinvest-busca-avancada.csv').resolve())

#da.calcularRiscoRetJanelasTemp('minhas').to_pickle('data/riscoRetornoMinhas.pkl')
#da.calcularRiscoRetJanelasTemp('all').to_pickle('data/riscoRetornoAll.pkl')


#dados = da.gerarcorrelacaoindividual('bbas3', 'selic')
#print(dados[0])

#da.gerarCorrelaAll('all').to_pickle('data/correlacoesIndAll3D.pkl')

#da.gerarrankingdividendos(dao.getMinhasEmpresasListadas()).to_pickle('data/rankingdividendosMinhas.pkl')
#da.gerarrankingdividendos(dao.getEmpresasListadasAntigas()).to_pickle('data/rankingdividendosAll.pkl')
#print(da.readRankingDividendos('all'))
#print(da.readRankingDividendos('minhas'))

