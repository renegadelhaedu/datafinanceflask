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

    xdata = data.drop(columns=['TICKER'])

    scaler = StandardScaler()
    formatedData = scaler.fit_transform(xdata)

    kmeans = KMeans(n_clusters=3, max_iter=500, random_state=42)
    groups = kmeans.fit_predict(formatedData)


    tickets = data['TICKER'].values
    empresas = {0: [], 1: [], 2: []}
    for i in range(groups.size):
        empresas[groups[i]].append(str(tickets[i]))

    dataGroups = pd.DataFrame.from_dict(empresas, orient='index')
    dataGroups.to_csv('data/clusters.csv', index=False)

    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(formatedData)

    fig = px.scatter(
        x=X_pca[:, 0], 
        y=X_pca[:, 1], 
        color=groups.astype(str),
        title="Visualização dos Clusters com PCA",
        labels={"x": "Componente Principal 1", "y": "Componente Principal 2"},
        opacity=0.7
    )

    for i, ticker in enumerate(data['TICKER']):
        fig.add_trace(
            go.Scatter(
                x=[X_pca[i, 0]],
                y=[X_pca[i, 1]],
                mode="text",
                text=ticker,
                textposition="top center",
                textfont=dict(size=10),
                showlegend=False
            )
        )

    fig.update_layout(
        xaxis_title="Componente Principal 1",
        yaxis_title="Componente Principal 2",
        xaxis=dict(showgrid=True),
        yaxis=dict(showgrid=True),
        coloraxis_colorbar=dict(title="Cluster"),
    )

    return dataGroups, fig.to_html(full_html=False)

def clusteringKmeans2(data=None, csvData=None, displayPlot=False):
    # Carrega o DataFrame e remove a coluna 'TICKER' para o clustering
    if data is None:
        data = pd.read_csv(csvData)

    xdata = data.drop(columns=['TICKER'])

    # Normaliza os dados
    scaler = StandardScaler()
    formatedData = scaler.fit_transform(xdata)

    # Aplica o KMeans
    kmeans = KMeans(n_clusters=3, max_iter=500, random_state=42)
    groups = kmeans.fit_predict(formatedData)

    # Organiza os tickers por cluster
    tickets = data['TICKER'].values
    empresas = {0:[], 1:[], 2:[]}
    for i in range(groups.size):
        empresas[groups[i]].append(str(tickets[i]))

    dataGroups = pd.DataFrame.from_dict(empresas, orient='index')
    dataGroups.to_csv('data/clusters.csv', index=False)

    if displayPlot:
        pca = PCA(n_components=2)
        X_pca = pca.fit_transform(formatedData)
        plt.figure(figsize=(12, 8))
        plt.scatter(X_pca[:, 0], X_pca[:, 1], c=groups, cmap='tab10', s=150, alpha=0.7)
        plt.colorbar(label='Cluster')
        plt.title("Visualização dos Clusters com PCA")
        plt.xlabel("Componente Principal 1")
        plt.ylabel("Componente Principal 2")
        for i, ticker in enumerate(data['TICKER']):
          plt.annotate(ticker, (X_pca[i, 0], X_pca[i, 1]), textcoords="offset points", xytext=(5,5), ha='center', fontsize=8)
        plt.grid(True, linestyle='--', alpha=0.5)
        plt.show()

    return dataGroups

def evaluate_cluster(data=None, csvData=None, max_clusters=15):
    """
    Calcula o silhouette score para diferentes números de clusters e gera o gráfico de elbow.

    Args:
        data: DataFrame com os dados para o clustering.
        csvData: Caminho para o arquivo CSV com os dados para o clustering.
        max_clusters: Número máximo de clusters a serem testados.

    Returns:
        Um DataFrame com o silhouette score para cada número de clusters.
    """

    if data is None:
        data = pd.read_csv(csvData)

    xdata = data.drop(columns=['TICKER'])

    scaler = StandardScaler()
    formatedData = scaler.fit_transform(xdata)

    silhouette_scores = []
    inertias = []

    for n_clusters in range(2, max_clusters + 1):
        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        kmeans.fit(formatedData)
        labels = kmeans.labels_
        silhouette_avg = silhouette_score(formatedData, labels)
        silhouette_scores.append(silhouette_avg)
        inertias.append(kmeans.inertia_)

    plt.plot(range(2, max_clusters + 1), inertias, marker='o')
    plt.title('Método Elbow')
    plt.xlabel('Número de Clusters')
    plt.ylabel('Inércia')
    plt.show()

    silhouette_df = pd.DataFrame({'n_clusters': range(2, max_clusters + 1), 'silhouette_score': silhouette_scores})

    return silhouette_df

def generate_cluster_dataframes(stosckCluster_csv_path, stockData_csv_path, n_clusters):
    stockcCluster_data = pd.read_csv(stosckCluster_csv_path, header=None)
    stock_data = pd.read_csv(stockData_csv_path)
    cluster_dataframes = {}

    for cluster_num in range(n_clusters):
        # Obtém os tickers para o cluster específico
        cluster_stocks = stockcCluster_data.iloc[cluster_num + 1].dropna().tolist()
        
        # Filtra os dados de mercado para incluir apenas os tickers do cluster
        cluster_dataframe = stock_data[stock_data['TICKER'].isin(cluster_stocks)]
        
        # Armazena o DataFrame no dicionário
        cluster_dataframes[f'Cluster_{cluster_num + 1}'] = cluster_dataframe

    return cluster_dataframes