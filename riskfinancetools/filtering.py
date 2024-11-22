import pandas as pd
import yfinance as yf

def ticketsMaiorLiquidez(dados):
    tickets = dados['TICKER']

    ticketsNoNumber = set()
    for emp in tickets:
        ticketsNoNumber.add(emp[0:4])

    ticketsMaisLiquidos = []
    for j in ticketsNoNumber:
        ticketsMaisLiquidos.append(dados[dados['TICKER'].str.contains(j)].sort_values(by=[' LIQUIDEZ MEDIA DIARIA'], ascending=False)['TICKER'].iloc[0])

    return dados[dados.TICKER.isin(ticketsMaisLiquidos)]

def isOld(dados, year=None, startDate=None, endDate=None):

    acoesInclusas = []

    for ticket in dados['TICKER']:
        ticker_data = yf.Ticker(ticket + '.sa')

        if year is not None:
            start = f"{year}-01-01"
            end = f"{year}-12-31"
        else:
            start = startDate
            end = endDate
        
        if len(ticker_data.history()) > 0 and len(ticker_data.history(start=start, end=end)) > 0:
            acoesInclusas.append(ticket)

    return dados[dados['TICKER'].isin(acoesInclusas)]

def filtering(pathCsv, year=None, startDate=None, endDate=None):

    dados = pd.read_csv(pathCsv, delimiter=';', decimal=',', thousands=".").fillna(0)

    dados.drop(dados[dados[' LIQUIDEZ MEDIA DIARIA'] < 1000000].index, inplace=True)
    dados.drop(dados[dados['MARGEM EBIT'] > 40].index, inplace=True)
    dados.drop(dados[dados['MARGEM EBIT'] < 0].index, inplace=True)
    dados.drop(dados[dados['P/L'] <= 1].index, inplace=True)
    dados.drop(dados[dados['P/L'] > 20].index, inplace=True)
    dados.drop(dados[dados['P/VP'] < 0].index, inplace=True)
    dados.drop(dados[dados['EV/EBIT'] <= 1].index, inplace=True)
    dados.drop(dados[dados['EV/EBIT'] > 20].index, inplace=True)
    dados.drop(dados[dados['ROE'] > 70].index, inplace=True)
    dados.drop(dados[dados['ROE'] < 0].index, inplace=True)
    dados.drop(dados[dados['ROIC'] < 0].index, inplace=True)
    dados.drop(dados[dados['PRECO'] == 0].index, inplace=True)
    dados.drop(dados[dados['DIVIDA LIQUIDA / EBIT'] < 0].index, inplace=True)
    dados.drop(dados[dados['DIVIDA LIQUIDA / EBIT'] > 5].index, inplace=True)

    dados.reset_index(drop=True);

    dados = ticketsMaiorLiquidez(dados)

    if year is not None:
        dados = isOld(dados, year=year)
    else:
        dados = isOld(dados, startDate=startDate, endDate=endDate)
        
    dados.drop( columns=[ 'PRECO', 'P/L', 'P/VP', 'P/ATIVOS', 'MARGEM BRUTA',
            'P/EBIT', 'EV/EBIT','ROIC',
        'MARGEM EBIT', 'DIV. LIQ. / PATRI.', 'PSR', 'P/CAP. GIRO',
        'P. AT CIR. LIQ.', 'LIQ. CORRENTE',  'ROA',
        'PATRIMONIO / ATIVOS', 'PASSIVOS / ATIVOS', 'GIRO ATIVOS',
        'CAGR RECEITAS 5 ANOS', 'CAGR LUCROS 5 ANOS', ' LIQUIDEZ MEDIA DIARIA',
        ' VPA', ' LPA', ' PEG Ratio', ' VALOR DE MERCADO'], inplace=True)
    
    dados.to_csv('data/acoes_filtradas.csv', index=False)
    
    return dados