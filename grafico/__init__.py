import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import yfinance as yf
import pandas as pd
import dataAnalise as da

def dados_acao(nome):
    dados = yf.Ticker(nome + '.sa').history(start='2020-01-01')
    print(dados.columns)

    fig = px.line(dados, x=dados.index, y='Close')
    valor_acao = dados['Close'].iloc[-1]
    
    return fig.to_html(), valor_acao

def gerarBarGrafDividendos(data):

    fig = px.bar(data, x='ticker', y='mediana', hover_data=['valorDividendo', 'media'])
    return fig.to_html()

def gerarBarGrafValores(data):
    fig = px.bar(data, x='TICKER', y='PRECO', hover_data=['PRECO'])
    fig.update_layout(
    xaxis=dict(
        tickangle=-90
    )
    )
    return fig.to_html()

def gerarrankingvalores(dados):
    dataf = []
    for empresa in dados:
        data = da.dyanalise(empresa)
        if data:
            dataf.append(data)

    df = pd.DataFrame(np.array(dataf), columns=['ticker', 'preco'])
    df = df.sort_values(by=['preco'], ascending=False).head(50)
    return df


def lerDadosCSV(caminho_arquivo):

    df = pd.read_csv(caminho_arquivo, delimiter=';')

    df = df.sort_values(by=df.columns[0], ascending=False).head(50)
    return df

def gerarGrafRiscRet(df_final):
    fig = go.Figure(data=go.Scatter(x=df_final['ProbGanho'],
                              y=df_final['PercRetorno'],
                              mode='markers',
                              text=df_final.index))
    fig.update_layout(
        xaxis_title= df_final.columns[0],
        yaxis_title= df_final.columns[1]

    )
    return fig.to_html()

def gerarGrafCorrIndicAll3D(df_final):
    fig = go.Figure(data=go.Scatter3d(x=df_final.iloc[:, 0],
                              y=df_final.iloc[:, 1],
                              z=df_final.iloc[:, 2],
                              mode='markers',
                              text=df_final.index),
                    )

    fig.update_layout(autosize=True,width=700,height=700 )
    fig.update_layout(
        scene=dict(
            xaxis_title=df_final.columns[0],
            yaxis_title=df_final.columns[1],
            zaxis_title=df_final.columns[2],
        )
    )
    return fig.to_html()

def gerarGrafCorrIndicAll(df_final):
    fig = go.Figure(data=go.Scatter(x=df_final.iloc[:, 0],
                              y=df_final.iloc[:, 1],
                              mode='markers',
                              text=df_final.index))

    fig.update_layout(autosize=True,width=900,height=500 )
    fig.update_layout(
        xaxis_title= df_final.columns[0],
        yaxis_title= df_final.columns[1]

    )
    return fig.to_html()


def gerarGrafCorrInd(graficodados, indicador):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        name=indicador,
        x=graficodados.index,
        y=graficodados['indicador'],
        mode='lines',
        line=dict(color='blue')

    ))
    fig.update_layout(
        autosize=True,
        width=900,
        height=500
    )
    fig.add_trace(go.Scatter(
        name='Cotação',
        x=graficodados.index,
        y=graficodados['stock'],
        mode='lines',
        line=dict(color='red'),
        legendgroup='Cotação'
    ))
    return fig.to_html()