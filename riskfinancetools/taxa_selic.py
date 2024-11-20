import pandas as pd
import matplotlib.pyplot as plt
import datetime

#Consultar taxa selic e retornar última cotação
def consulta_bc(codigo_bcb):
    url = f'http://api.bcb.gov.br/dados/serie/bcdata.sgs.{codigo_bcb}/dados?formato=json'
    df = pd.read_json(url)
    df['data'] = pd.to_datetime(df['data'], dayfirst=True)
    df.set_index('data', inplace=True)
    return df

def quotation(year):
    data_selic = consulta_bc(432)
    ultima_cotacao_selic = data_selic[data_selic.index.year == int(year)]['valor'].iloc[-1]

    return ultima_cotacao_selic

#Gerar gráfico com últimas cotações da taxa selic
data_selic = consulta_bc(432)
ano_atual = datetime.datetime.now().year
data_selic_atual = data_selic[data_selic.index.year == ano_atual]

def graf_selic():
    # Código para gerar o gráfico
    plt.figure(figsize=(12, 6))
    plt.plot(data_selic_atual.index, data_selic_atual['valor'])
    plt.title('Taxa Selic - Ano Atual')
    plt.xlabel('Data')
    plt.ylabel('Valor')
    plt.grid(True)
    plt.show()

if __name__ == '__main__':  
    graf_selic()