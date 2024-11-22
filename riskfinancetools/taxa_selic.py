import requests
import pandas as pd

def consulta_bc(codigo_bcb):
    url = f'http://api.bcb.gov.br/dados/serie/bcdata.sgs.{codigo_bcb}/dados?formato=json'
    try:
        response = requests.get(url)
        response.raise_for_status() 
        print(f'Conteúdo retornado: {response.text[:200]}...')

        # Verifica se o conteúdo é JSON válido
        df = pd.read_json(response.text)
        df['data'] = pd.to_datetime(df['data'], dayfirst=True)
        df.set_index('data', inplace=True)
        return df
    except requests.exceptions.RequestException as req_error:
        print(f'Erro ao fazer a requisição: {req_error}')
    except ValueError as val_error:
        print(f'Erro ao converter para JSON: {val_error}')
    except Exception as e:
        print(f'Erro inesperado: {e}')
    return pd.DataFrame()

def quotation(year):
    try:
        data_selic = consulta_bc(432)
        if not data_selic.empty:
            ultima_cotacao_selic = data_selic[data_selic.index.year == int(year)]['valor'].iloc[-1]
            return ultima_cotacao_selic
        else:
            print('Dados não encontrados para a Selic.')
            return 10
    except Exception as e:
        print(f'Erro ao consultar a Selic: {e}')
        return 10


#Gerar gráfico com últimas cotações da taxa selic
# data_selic = consulta_bc(432)
# ano_atual = datetime.datetime.now().year
# data_selic_atual = data_selic[data_selic.index.year == ano_atual]

# def graf_selic():
#     # Código para gerar o gráfico
#     plt.figure(figsize=(12, 6))
#     plt.plot(data_selic_atual.index, data_selic_atual['valor'])
#     plt.title('Taxa Selic - Ano Atual')
#     plt.xlabel('Data')
#     plt.ylabel('Valor')
#     plt.grid(True)
#     plt.show()

if __name__ == '__main__':  
    graf_selic()