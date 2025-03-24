import pandas as pd
import yfinance as yf
import dao
import pathlib



def get_codigos_acoes():

    actual_dir = pathlib.Path().absolute()
    path = f'{actual_dir}/data/statusinvest-busca-avancada.csv'
    dados = pd.read_csv(path, decimal=",", delimiter=";", thousands=".")
    dados = dados.fillna(0)
    dados.drop(dados[dados['PRECO'] <= 0].index, inplace=True)

    return dados['TICKER'].values.tolist()


def gerarPercentuais(email):
    cart = dao.get_carteira(email)

    if len(cart) == 0:
        return None, None, None

    tikers = list(map(lambda x: x + '.SA', list(cart.keys())))

    data = yf.download(tikers)
    data.ffill(inplace=True)

    qtdeTik = pd.DataFrame.from_dict(cart, orient='index', columns=['qtde'])
    qtdeTik.sort_index(inplace=True)
    todayCot = pd.DataFrame(data['Close'].iloc[-1])
    todayCot.columns = ['cota']

    qtdeTik['valor'] = qtdeTik['qtde'].values * todayCot['cota'].values
    total = qtdeTik['valor'].sum()
    qtdeTik['perc'] = round((qtdeTik['valor'] / total) * 100, 1)
    qtdeTik.sort_values(by=['perc'], ascending=False, inplace=True)

    grid = pd.concat([(data['Close'].pct_change() * 100).iloc[-1], data['Close'].iloc[-1]], axis=1)
    grid.index = grid.index.str.replace('.SA', '', regex=False)
    grid.reset_index(inplace=True)
    grid = grid.round(2)

    return qtdeTik.to_dict()['perc'], grid.values.tolist(), cart