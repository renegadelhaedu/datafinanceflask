import pandas as pd
import numpy as np
import yfinance as yf
from dao import *
import pathlib
import datetime as dt
import dao
import calendar

def pegarcotacoes():
    nomesAcoes = ['bbas3.sa', 'itsa4.sa','brsr6.sa','egie3.sa','alup11.sa', 'abcb4.sa']

    dados = yf.download(nomesAcoes)
    valores = [round(x, 2) for x in list(dados['Adj Close'].ffill().iloc[-1].values)]
    nomes = [y.replace('.SA', '') for y in list(dados['Adj Close'].columns.values)]

    pares = []
    for i in range(len(nomes)):
        pares.append([nomes[i], valores[i]])

    return pares

def gerarrankingdividendos(dados):
    dataf = []
    for empresa in dados:
        data = dyanalise(empresa)
        if 0 != data:
            dataf.append(data)

    df = pd.DataFrame(np.array(dataf), columns=['ticker', 'valorDividendo', 'mediana', 'media'])
    df = df.astype({"ticker": str, "valorDividendo": float, "mediana": float, "media": float})
    df.drop(df[df['mediana'] < 1].index, inplace=True)

    df = df.sort_values(by=['mediana'], ascending=False)
    df = df.reset_index()
    df = df.drop(columns=['index'])
    return df

def dyanalise(name):
    empresa = name + '.SA'
    comp = yf.Ticker(empresa)
    hist2 = comp.history(period='5y')
    if (len(hist2) == 0):
        return 0
    somaDiv = hist2['Dividends'].resample('Y').sum()
    meanPrice = hist2['Close'].resample('Y').median()
    result = somaDiv / meanPrice * 100

    return [name, float("{0:.2f}".format(somaDiv.median())), float("{0:.2f}".format(result.median())), float("{0:.2f}".format(result.mean()))]

def gerarcorrelacaoindividual(ticker, indicador):
    if indicador == 'selic':
        ind_df = consulta_bc(432)
    elif indicador == 'ibcbr':
        ind_df = consulta_bc(24364)
    elif indicador == 'ipca':
        ind_df = consulta_bc(433)
    data_inicio = '2014-01-01'

    cotaMensal = yf.Ticker(ticker + ".SA").history(start=data_inicio).resample('M')['Close'].mean().to_frame()

    ind_df = ind_df[ind_df.index >= data_inicio]
    ind_df = ind_df.resample('M').mean()


    if cotaMensal.size - ind_df.size > 0:
        cotaMensal.drop(cotaMensal.tail(cotaMensal.size - ind_df.size).index, inplace=True)

    cotaMensal.index = pd.to_datetime(cotaMensal.index.date)

    ind_stock = pd.concat([ind_df, cotaMensal], axis=1, ignore_index=True)

    df_norm = (ind_stock - ind_stock.min()) / (ind_stock.max() - ind_stock.min())
    df_norm.columns = ['indicador', 'stock']

    return round(float(df_norm.corr().iloc(0)[1][0]), 3), df_norm


#https://www3.bcb.gov.br/sgspub/localizarseries/localizarSeries.do?method=prepararTelaLocalizarSeries
def consulta_bc(codigo_bcb):
    url = 'http://api.bcb.gov.br/dados/serie/bcdata.sgs.{}/dados?formato=json'.format(codigo_bcb)
    df = pd.read_json(url)
    df['data'] = pd.to_datetime(df['data'], dayfirst=True)
    df.set_index('data', inplace=True)
    return df


def readRiscoRetornoFile(opcao):
    if opcao == 'all':
        return pd.read_pickle('data/riscoRetornoAll.pkl')
    else:
        return pd.read_pickle('data/riscoRetornoMinhas.pkl')

def readCorrelacoesIndicFile(opcao):
    if opcao == 'all':
        return pd.read_pickle('data/correlacoesIndAll3D.pkl')
    else:
        return pd.read_pickle('data/correlacoesIndMinhas3D.pkl')

def readRankingDividendos(opcao):
    if opcao == 'all':
        return pd.read_pickle('data/rankingdividendosAll.pkl')
    else:
        return pd.read_pickle('data/rankingdividendosMinhas.pkl')


def gerarCorrelaAll(opcao):

    if opcao == 'all':
        tickers = getEmpresasListadasAntigas()
    else:
        tickers = getMinhasEmpresasListadas()

    lista = []
    for ticker in tickers:
        ipca = gerarcorrelacaoindividual(ticker ,'ipca')
        selic = gerarcorrelacaoindividual(ticker , 'selic')
        ibcbr = gerarcorrelacaoindividual(ticker, 'ibcbr')

        lista.append([ipca[0], selic[0], ibcbr[0]])

    data = pd.DataFrame(lista, index=tickers,columns=['ipca','selic','ibcbr'])
    return data



def calcularRiscoRetJanelasTemp(opcao):

    if opcao == 'all':
        tickers = getEmpresasListadasAntigas()
    else:
        tickers = getMinhasEmpresasListadas()

    comps = [x + '.sa' for x in tickers]

    dataProbGanho = pd.DataFrame()
    dataPerctRetorno = pd.DataFrame()

    for comp in comps:
        saida = gerarDataRetornos(comp)
        dataProbGanho = pd.concat([dataProbGanho, pd.DataFrame([[comp, saida['percGanhos'].values[0]]])])
        dataPerctRetorno = pd.concat([dataPerctRetorno, pd.DataFrame([[comp, saida['Rentb'].values[0]]])])

    dataProbGanho.columns = ['ticker', 'ProbGanho']
    dataPerctRetorno.columns = ['ticker', 'PercRetorno']

    df_final = dataProbGanho.merge(dataPerctRetorno, how='left', on='ticker')
    df_final.set_index('ticker', inplace=True)

    return df_final


def calcRetorno(week, janela):

    retW = (week / week.shift(janela) - 1) * 100

    retW.dropna(inplace=True)
    totalJanelas = len(retW)

    qtdeJanPosit = len(retW[retW['Adj Close'] > 0])
    return [abs((qtdeJanPosit / totalJanelas) * 100 - 100), retW['Adj Close'].mean()]


def gerarDataRetornos(ticker):
    probGanhos = list()
    rentMedia = list()

    intervalo = 4
    maxSemanas = 192

    hist = yf.download(ticker, period='15y')
    week = hist.resample('W').mean()

    for i in range(48, maxSemanas, intervalo):
        saida = calcRetorno(week, i)
        probGanhos.append(saida[0])
        rentMedia.append(saida[1])

    data = pd.DataFrame(list(zip(list([*range(4, maxSemanas, intervalo)]), probGanhos, rentMedia)),
                        columns=['interv', 'percGanhos', 'Rentb'])
    data = data.set_index('interv')
    return data[-1:]

def gerar_top_acoes():

    actual_dir = pathlib.Path().absolute()

    path = f'{actual_dir}/data/statusinvest-busca-avancada.csv'
    dados = pd.read_csv(path, decimal=",", delimiter=";", thousands=".")
    dados = dados.fillna(0)

    dados.drop(dados[dados[' LIQUIDEZ MEDIA DIARIA'] < 10000000].index, inplace=True)
    dados.drop(dados[dados['P/L'] <= 0].index, inplace=True)
    dados.drop(dados[dados[' LPA'] <= 0].index, inplace=True)
    dados.drop(dados[dados['EV/EBIT'] <= 0].index, inplace=True)
    dados.drop(dados[dados['EV/EBIT'] > 30].index, inplace=True)
    dados.drop(dados[dados['PRECO'] <= 0].index, inplace=True)

    return dados


def pegar_listadas():

    return ['ABCB4', 'ABEV3', 'AESB3', 'ALOS3', 'ALUP11', 'ARZZ3', 'ASAI3', 'AURE3', 'B3SA3', 'BBAS3', 'BBDC3', 'BBDC4',
     'BBSE3', 'BEEF3', 'BPAC11', 'BPAN4', 'BRAP4', 'BRSR6', 'CCRO3', 'CEAB3', 'CIEL3', 'CMIG4', 'CMIN3', 'CPFE3',
     'CPLE3', 'CPLE6', 'CRFB3', 'CSMG3', 'CURY3', 'CXSE3', 'CYRE3', 'DIRR3', 'DXCO3', 'ECOR3', 'EGIE3', 'ELET3',
     'ELET6', 'ENAT3', 'ENEV3', 'ENGI11', 'EQTL3', 'EZTC3', 'FLRY3', 'GGBR4', 'GGPS3', 'GMAT3', 'GOAU4', 'GOLL4',
     'HBSA3', 'HYPE3', 'IGTI11', 'INTB3', 'ITSA4', 'ITUB4', 'JHSF3', 'KEPL3', 'KLBN11', 'LEVE3', 'LREN3', 'MDIA3',
     'MILS3', 'MULT3', 'NEOE3', 'ODPV3', 'ONCO3', 'PETR3', 'PETR4', 'PETZ3', 'POMO4', 'PORT3', 'POSI3', 'PRIO3',
     'PSSA3', 'RADL3', 'RAIL3', 'RAIZ4', 'RAPT4', 'RDOR3', 'RECV3', 'RENT3', 'SANB11', 'SAPR11', 'SBFG3', 'SBSP3',
     'SIMH3', 'SLCE3', 'SMFT3', 'SMTO3', 'SOMA3', 'SRNA3', 'STBP3', 'SUZB3', 'TAEE11', 'TIMS3', 'TOTS3', 'TRPL4',
     'TTEN3', 'TUPY3', 'UGPA3', 'UNIP6', 'VALE3', 'VAMO3', 'VBBR3', 'VIVA3', 'VIVT3', 'VULC3', 'VVEO3', 'WEGE3',
     'YDUQ3']


def pegar_maiores_empresas():
    actual_dir = pathlib.Path().absolute()

    path = f'{actual_dir}/data/statusinvest-busca-avancada.csv'
    #path = path.split('datafinanceflask')[0] + 'datafinanceflask\\data\\statusinvest-busca-avancada.csv'
    dados = pd.read_csv(path, decimal=",", delimiter=";", thousands=".")
    dados = dados[dados['TICKER'].isin(pegar_listadas())]
    retorno = []

    #maior valor de mercado
    lista = dados.sort_values(by=[' VALOR DE MERCADO'], ascending=False)
    retorno.append(list(lista['TICKER'].head(6).to_dict().values()))

    #maior pagadora de dividendos
    lista = dados.sort_values(by=['DY'], ascending=False)
    retorno.append( list(lista['TICKER'].head(6).to_dict().values()))

    #menor relação preço/lucro
    lista = dados.sort_values(by=['P/L'], ascending=True)
    retorno.append( list(lista['TICKER'].head(6).to_dict().values()))

    #maior retorno de capital investido
    lista = dados.sort_values(by=['ROE'], ascending=False)
    retorno.append(list(lista['TICKER'].head(6).to_dict().values()))

    return retorno

def isListed(dados):
    listed = []
    for i in dados['TICKER']:
        if len(yf.Ticker(i + '.SA').history()) > 0:
            listed.append(i)

    return listed

def get_cotacao_ticker(tickers):
    tickers = [x + '.SA' for x in tickers]

    pares  = yf.download(tickers, period='1mo')['Adj Close']
    pares_ffill = pares.ffill()
    return pares_ffill.iloc[-1].to_dict()

def gerar_listas_acoes_cotacoes():
    dicis = []
    conj = set()
    categorias = pegar_maiores_empresas()
    for lista in categorias:
        for i in lista:
            conj.add(i)

    pares = get_cotacao_ticker(list(conj))
    dic_arred = {chave.replace('.SA', ''): round(valor, 2) for chave, valor in pares.items()}

    for categoria in categorias:
        dicis.append([[ticker, dic_arred.get(ticker) ]for ticker in categoria])

    return dicis

def gerarRentabilidadeVariacao(tempo, tickers):
    atual = dt.datetime.now()
    ano = atual.year
    mes = atual.month

    if tempo == 'no Mês':
        if(mes == 1):

            last_bd = last_business_day(ano - 1 , 12)
        else:
            last_bd = last_business_day(ano, mes - 1)


        inicio = f'{last_bd}'
        data = yf.download(tickers, start=inicio)

    elif tempo == 'no Dia':
        dia = atual.day
        if bool(len(pd.bdate_range(f'{ano}-{mes}-{dia}', f'{ano}-{mes}-{dia}'))):
            #diaUtil = dt.datetime.strptime(f'{ano}-{mes}-{dia}', '%Y-%m-%d') - dt.timedelta(days=1)

            inicio = get_previous_business_day()

        else:
            #TEM QUE TROCAR days=2 para days=1 por conta do feriado
            diaUtil = dt.datetime.strptime(get_previous_business_day(), '%Y-%m-%d') - dt.timedelta(days=1)
            inicio = f'{diaUtil.year}-{diaUtil.month}-{diaUtil.day}'


        data = yf.download(tickers, start=inicio, interval='5m')
        ultimaCotacaoDiaAnterior = data.groupby(data['Adj Close'].index.astype(str).str[:10]).last().iloc[-2]

        lastday = str(data['Adj Close'].index.map(pd.Timestamp.date).unique()[-1])
        data = data[data['Adj Close'].index.astype(str).str[:10] == lastday]
        data.loc[data.index[0], :] = ultimaCotacaoDiaAnterior

    elif tempo == 'no Ano':
        inicio = f'{str(ano - 1)}-12-28'
        data = yf.download(tickers, start=inicio)

    else:
        inicio = f'2021-12-31'
        data = yf.download(tickers, start=inicio)

    return data


def rentabilidadeAcumulada(tempo):

    cart = dao.getCarteira()
    tickers = list(map(lambda x: x + '.SA', list(cart.keys())))
    tickers.append('^BVSP')

    data = gerarRentabilidadeVariacao(tempo, tickers)

    ibov = data['Adj Close']['^BVSP']
    data.drop(('Adj Close', '^BVSP'), axis=1, inplace=True)

    data.ffill(inplace=True)
    data.bfill(inplace=True)

    qtdeTik = pd.DataFrame.from_dict(cart, orient='index', columns=['qtde'])
    qtdeTik.sort_index(inplace=True)

    todayCot = pd.DataFrame(data['Adj Close'].iloc[-1])
    todayCot.columns = ['cota']

    qtdeTik['valor'] = qtdeTik['qtde'].values * todayCot['cota'].values

    total = qtdeTik['valor'].sum()
    qtdeTik['perc'] = round((qtdeTik['valor'] / total) * 100, 3)

    cot_chg = data['Adj Close'].pct_change()
    cot_chg.fillna(0, inplace=True)
    weighted_returns = cot_chg * list(qtdeTik['perc'] / 100)
    port_ret = weighted_returns.sum(axis=1)

    cumulative_ret = ((port_ret + 1).cumprod() - 1) * 100

    ibov.ffill(inplace=True)
    ibov.bfill(inplace=True)

    ibov_chg = ibov.pct_change()
    ibov_chg.fillna(0, inplace=True)

    ibov_cumReturns = (np.cumprod(ibov_chg + 1) - 1) * 100

    final_data = pd.concat([ibov_cumReturns, cumulative_ret], axis=1, join='inner')
    final_data.columns = ['ibov', 'portfolio']

    return final_data


def last_business_day(year, month):
    last_day = calendar.monthrange(year, month)[1]
    date = dt.date(year, month, last_day)
    while date.weekday() > 4:
        date -= dt.timedelta(days=1)
    return date

def get_previous_business_day():
    today = dt.datetime.today()
    one_day = dt.timedelta(days=1)
    previous_day = today - one_day
    while previous_day.weekday() >= 5:
        previous_day -= one_day
    return previous_day.strftime("%Y-%m-%d")
