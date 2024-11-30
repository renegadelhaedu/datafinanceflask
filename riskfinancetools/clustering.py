from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
from sklearn.decomposition import PCA
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

def clusteringKmeans(data=None, csvData=None):
    if data is None:
        data = pd.read_csv(csvData).fillna(0)

    # Validação
    if 'TICKER' not in data.columns:
        raise ValueError("A coluna 'TICKER' é obrigatória.")
    required_columns = ['BETA', 'STD', 'SHARPE RATIO', 'TREYNOR RATIO']
    for col in required_columns:
        if col not in data.columns:
            raise ValueError(f"A coluna '{col}' é obrigatória para o clustering.")

    # Selecionar as colunas desejadas
    xdata = data[required_columns]
    if xdata.shape[1] < 2:
        raise ValueError("São necessárias pelo menos duas métricas numéricas.")

    # Normalização
    scaler = StandardScaler()
    formatedData = scaler.fit_transform(xdata)

    # Quantidade ideal de clusters
    best_score = -1
    n_clusters = 2

    for n_cluster_number in range(2, 15):
        kmeans = KMeans(n_clusters=n_cluster_number, max_iter=500, random_state=42)
        groups = kmeans.fit_predict(formatedData)

        score = silhouette_score(formatedData, groups)

        if score > best_score:
            best_score = score
            n_clusters = n_cluster_number

    # Clusterização
    kmeans = KMeans(n_clusters=n_clusters, max_iter=500, random_state=42)
    groups = kmeans.fit_predict(formatedData)

    # Definir nomes dos clusters
    cluster_names = {i: f"Cluster {i + 1}" for i in range(n_clusters)}
    data['Cluster'] = [cluster_names[group] for group in groups]

    # Exportação com clusters
    data.to_csv('data/clusters.csv', index=False)

    # Paleta de cores para clusters]
    pallete = px.colors.qualitative.Bold    
    cluster_colors = {f"Cluster {i+1}": pallete[i % len(pallete)] for i in range(n_clusters)}

    # Gráfico 3D com legenda
    fig = go.Figure()

    for cluster, color in cluster_colors.items():
        cluster_data = data[data['Cluster'] == cluster]
        fig.add_trace(go.Scatter3d(
            x=cluster_data['BETA'],
            y=cluster_data['STD'] * 100,
            z=cluster_data['SHARPE RATIO'],
            mode='markers',
            marker=dict(
                size=8,
                color=color,
                opacity=0.8
            ),
            name=cluster,  # Nome do cluster para a legenda
            hovertext=cluster_data['TICKER'],  # Nome do TICKER no hover
            hoverinfo="text+x+y+z"  # Mostra hovertext e coordenadas
        ))

    fig.update_layout(
        autosize=True,
        width=800,
        height=800,
        title="Clusters - Gráfico 3D",
        scene=dict(
            xaxis_title='BETA',
            yaxis_title='STD (%)',
            zaxis_title='SHARPE RATIO'
        ),
        legend=dict(
            title="Clusters",
            itemsizing='constant',
            font=dict(size=10),
            orientation="v",
            x=1.05,
            xanchor="left",
            y=1.0,
            yanchor="top"
        )
    )

    return data, fig.to_html(full_html=False)