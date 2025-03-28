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
    valores = [round(x, 2) for x in list(dados['Close'].ffill().iloc[-1].values)]
    nomes = [y.replace('.SA', '') for y in list(dados['Close'].columns.values)]

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


def gerarCorrelacoesCarteiraXindMacro(tickers):
    selic_df = consulta_bc(432)
    ibcbr_df = consulta_bc(24364)
    ipca_df = consulta_bc(433)

    lista = []
    for ticker in tickers:
        print(ticker)
        ipca = gerarcorrelacaoindividual(ticker ,'ipca',ipca_df)
        selic = gerarcorrelacaoindividual(ticker , 'selic', selic_df)
        ibcbr = gerarcorrelacaoindividual(ticker, 'ibcbr', ibcbr_df)

        lista.append([ipca[0], selic[0], ibcbr[0]])

    data = pd.DataFrame(lista, index=tickers,columns=['ipca','selic','ibcbr'])
    return data


def gerarcorrelacaoindividual(ticker, indicador, data_indicador):
    if indicador == 'selic':
        ind_df = data_indicador
    elif indicador == 'ibcbr':
        ind_df = data_indicador
    elif indicador == 'ipca':
        ind_df = data_indicador
    data_inicio = '2014-01-01'

    cotaMensal = yf.Ticker(ticker + ".SA").history(start='2014-01-01').resample('ME')['Close'].mean().to_frame()
    ind_df = ind_df[ind_df.index >= data_inicio]
    ind_df = ind_df.resample('ME').mean()


    if cotaMensal.size - ind_df.size > 0:
        cotaMensal.drop(cotaMensal.tail(cotaMensal.size - ind_df.size).index, inplace=True)

    if cotaMensal.size - ind_df.size < 0:
        ind_df.drop(ind_df.head(ind_df.size - cotaMensal.size).index, inplace=True)

    cotaMensal.index = pd.to_datetime(cotaMensal.index.date)

    ind_stock = pd.concat([ind_df, cotaMensal], axis=1, ignore_index=True)
    ind_stock.dropna(inplace=True)

    df_norm = (ind_stock - ind_stock.min()) / (ind_stock.max() - ind_stock.min())
    df_norm.columns = ['indicador', 'stock']

    return round(float(df_norm.corr().iloc(0)[1][0]), 2), df_norm


def calcularRiscoRetJanelasTemp(tickers):

    comps = [x + '.SA' for x in tickers]

    dataProbGanho = pd.DataFrame(columns=['ticker', 'ProbGanho'])
    dataPerctRetorno = pd.DataFrame(columns=['ticker', 'PercRetorno'])

    for comp in comps:
        saida = gerarDataRetornos(comp)
        novo_dado_prob = pd.DataFrame([[comp, saida[0]]], columns=['ticker', 'ProbGanho'])
        dataProbGanho = pd.concat([dataProbGanho, novo_dado_prob], ignore_index=True)

        novo_dado_ret = pd.DataFrame([[comp, saida[1]]], columns=['ticker', 'PercRetorno'])
        dataPerctRetorno = pd.concat([dataPerctRetorno, novo_dado_ret], ignore_index=True)

    dataProbGanho.columns = ['ticker', 'ProbGanho']
    dataPerctRetorno.columns = ['ticker', 'PercRetorno']

    df_final = dataProbGanho.merge(dataPerctRetorno, how='left', on='ticker')
    df_final.set_index('ticker', inplace=True)

    return df_final


def gerarDataRetornos(ticker):

    hist = yf.download(ticker, period='10y', interval='1d')
    hist = hist[['Close']].dropna()

    hist['Retorno'] = (hist['Close'] / hist['Close'].shift(252) - 1) * 100
    hist.dropna(inplace=True)

    hist['Positiva'] = hist['Retorno'] > 0
    total_janelas = len(hist)
    janelas_positivas = hist['Positiva'].sum()

    if total_janelas > 0:
        percentual_positivo = (janelas_positivas / total_janelas) * 100
    else:
        percentual_positivo = 0

    return percentual_positivo, hist['Retorno'].mean()


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

    pares  = yf.download(tickers, period='1mo')['Close']
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
        ultimaCotacaoDiaAnterior = data.groupby(data['Close'].index.astype(str).str[:10]).last().iloc[-2]

        lastday = str(data['Close'].index.map(pd.Timestamp.date).unique()[-1])
        data = data[data['Close'].index.astype(str).str[:10] == lastday]
        data.loc[data.index[0], :] = ultimaCotacaoDiaAnterior

    elif tempo == 'no Ano':
        inicio = f'{str(ano - 1)}-12-28'
        data = yf.download(tickers, start=inicio)

    else:
        inicio = f'2021-12-31'
        data = yf.download(tickers, start=inicio)

    return data


def rentabilidadeAcumulada(tempo, carteira):
   # ['no Dia', 'no Mês', 'no Ano', 'Desde início do ano passado']

    tickers = list(map(lambda x: x + '.SA', list(carteira.keys())))
    tickers.append('^BVSP')

    data = gerarRentabilidadeVariacao(tempo, tickers)

    ibov = data['Close']['^BVSP']
    data.drop(('Close', '^BVSP'), axis=1, inplace=True)

    data.ffill(inplace=True)
    data.bfill(inplace=True)

    qtdeTik = pd.DataFrame.from_dict(carteira, orient='index', columns=['qtde'])
    qtdeTik.sort_index(inplace=True)

    todayCot = pd.DataFrame(data['Close'].iloc[-1])
    todayCot.columns = ['cota']

    qtdeTik['valor'] = qtdeTik['qtde'].values * todayCot['cota'].values

    total = qtdeTik['valor'].sum()
    qtdeTik['perc'] = round((qtdeTik['valor'] / total) * 100, 3)

    cot_chg = data['Close'].pct_change()
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


def processarAnalise():

    actual_dir = pathlib.Path().absolute()

    path = f'{actual_dir}/data/statusinvest-busca-avancada.csv'
    dados = pd.read_csv(path, decimal=",", delimiter=";", thousands=".")
    dados3 = dados[dados['TICKER'].isin(dao.getAcoesListadas())]

    filtroMaisLiquidas = ticketsMaiorLiquidez(dados3)
    dados3 = dados3[dados3['TICKER'].isin(filtroMaisLiquidas)]
    dados3.fillna(0, inplace=True)
    dados3.loc[dados3['MARGEM EBIT'] == 0, 'MARGEM EBIT'] = dados3['MARGEM EBIT'].median()

    dados3.drop(dados3[dados3[' LIQUIDEZ MEDIA DIARIA'] < 1000000].index, inplace=True)
    dados3.drop(dados3[dados3['P/L'] <= 0].index, inplace=True)
    dados3.drop(dados3[dados3['DIVIDA LIQUIDA / EBIT'] >= 3].index, inplace=True)
    dados3.drop(dados3[dados3[' LPA'] <= 0].index, inplace=True)
    dados3.drop(dados3[dados3['DY'] < 1].index, inplace=True)
    dados3.drop(dados3[dados3['ROE'] < 3].index, inplace=True)
    dados3.drop(dados3[dados3['EV/EBIT'] <= 0].index, inplace=True)
    dados3.drop(dados3[dados3['EV/EBIT'] > 30].index, inplace=True)
    dados3.drop(dados3[dados3['PRECO'] <= 0].index, inplace=True)

    magdata = calcularMagicFormulaRene(dados3)

    gordondata = modeloGordon(dados3)

    tmag = magdata
    tgordon = gordondata

    tmag = tmag.merge(tgordon, how='left', on='stock')

    return tmag


def calcularMagicFormulaRene(dados):
    dados4 = dados.replace(np.nan, 0)

    ranks = dict(zip(list(dados4.TICKER), [0] * len(dados4)))
#    for name in dados4.TICKER:
#        ranks[name] = 0

    dados4 = dados4.sort_values(by=['ROE'], ascending=False)
    i = 1
    for name in dados4.TICKER:
        i = i + 1
        ranks[name] = ranks[name] + i

    dados4 = dados4.sort_values(by=['MARGEM EBIT'], ascending=False)
    i = 0
    for name in dados4.TICKER:
        i = i + 1
        ranks[name] = ranks[name] + i

    dados4 = dados4.sort_values(by=['EV/EBIT'])
    i = 1
    for name in dados4.TICKER:
        i = i + 1
        ranks[name] = ranks[name] + i

    final = pd.DataFrame.from_dict({'stock': ranks.keys(), 'pontos': ranks.values()})
    final = final.sort_values(by=['pontos'])
    final = final.reset_index()
    final = final.drop(columns=['index'])

    return final

def modeloGordon(dados):
    gordon = []

    for name in dados.TICKER:

        empresa = name + '.SA'
        comp = yf.Ticker(empresa)
        hist2 = comp.history(start='2020-01-01')
        hist = comp.history()
        somaDiv = hist2['Dividends'].resample('Y').sum()

        if len(hist2) != 0 or len(somaDiv) < 4:

            gordonPrice = somaDiv.median() / 0.06

            lastPrice = hist['Close'][-1]
            if pd.isna(lastPrice):
                lastPrice = hist['Close'][-2]

            difGordon = (gordonPrice - lastPrice) / gordonPrice * 100

            gordon.append([name, float("{0:.2f}".format(difGordon))])

    dadoGordon = pd.DataFrame(gordon, columns=['stock', 'margemGordon'])
    return dadoGordon

def ticketsMaiorLiquidez(dados):
    tickets = dados['TICKER']

    ticketsNoNumber = set()
    for emp in tickets:
        ticketsNoNumber.add(emp[0:4])

    ticketsMaisLiquidos = []
    for j in ticketsNoNumber:
        ticketsMaisLiquidos.append(
            dados[dados['TICKER'].str.contains(j)].sort_values(by=[' LIQUIDEZ MEDIA DIARIA'], ascending=False)[
                'TICKER'].iloc[0])

    return ticketsMaisLiquidos


def computarRankingFundamentos(tdiv):
    tdiv = tdiv.set_index('stock')

    tdiv['notaMedia'] = 0

    for i in tdiv.index:

        nota = 0
        if tdiv.loc[i, 'pontos'] == tdiv.describe()['pontos'][3]:
            nota = nota + 0
        if tdiv.loc[i, 'pontos'] <= tdiv.describe()['pontos'][4]:
            nota = nota + 3
        elif tdiv.loc[i, 'pontos'] <= tdiv.describe()['pontos'][5]:
            nota = nota + 2
        elif tdiv.loc[i, 'pontos'] <= tdiv.describe()['pontos'][6]:
            nota = nota + 1
        else:
            nota = nota + 0

        if tdiv.loc[i, 'margemGordon'] == tdiv.describe()['margemGordon'][7]:
            nota = nota + 0
        if tdiv.loc[i, 'margemGordon'] >= tdiv.describe()['margemGordon'][6]:
            nota = nota + 7
        elif tdiv.loc[i, 'margemGordon'] >= tdiv.describe()['margemGordon'][5]:
            nota = nota + 5
        elif tdiv.loc[i, 'margemGordon'] >= tdiv.describe()['margemGordon'][4]:
            nota = nota + 3
        else:
            nota = nota + 0

        tdiv.loc[i, 'notaMedia'] = nota

    return tdiv
