from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
from sklearn.decomposition import PCA
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

def clusteringKmeans(data=None, csvData=None, n_components=2):
    if data is None:
        data = pd.read_csv(csvData).fillna(0)

    # Validação
    if 'TICKER' not in data.columns:
        raise ValueError("A coluna 'TICKER' é obrigatória.")
    xdata = data.drop(columns=['TICKER'])
    if xdata.shape[1] < 2:
        raise ValueError("São necessárias pelo menos duas métricas numéricas.")

    # normalização
    scaler = StandardScaler()
    formatedData = scaler.fit_transform(xdata)

    # quantidade ideal de clusters
    best_score = -1
    n_clusters = 2

    for n_cluster_number in range(2, 15):
        kmeans = KMeans(n_clusters=n_cluster_number, max_iter=500, random_state=42)
        groups = kmeans.fit_predict(formatedData)
        
        score = silhouette_score(formatedData, groups)

        if score > best_score:
            best_score = score
            n_clusters = n_cluster_number

    #Clusterização
    kmeans = KMeans(n_clusters=n_clusters, max_iter=500, random_state=42)
    groups = kmeans.fit_predict(formatedData)

    # Definir nomes dos clusters
    cluster_names = {i: f"Cluster {i + 1}" for i in range(n_clusters)}
    data['Cluster'] = [cluster_names[group] for group in groups]

    # Exportação com clusters
    data.to_csv('data/clusters.csv', index=False)

    # PCA para visualização
    pca = PCA(n_components=n_components)
    X_pca = pca.fit_transform(formatedData)

    cluster_colors = {f"Cluster {i+1}": f"rgb({(i*60)%255},{(i*80)%255},{(i*100)%255})" for i in range(n_clusters)}

    # Gráfico Interativo
    fig = px.scatter(
        x=X_pca[:, 0],
        height=650,
        y=X_pca[:, 1],
        color=data['Cluster'],  # Usar nomes dos clusters
        title="Visualização dos Clusters com PCA",
        labels={"x": "Componente Principal 1", "y": "Componente Principal 2"},
        opacity=0.7,
        category_orders={'Cluster': [f"Cluster {i + 1}" for i in range(n_clusters)]},
        hover_name=data['TICKER'],
        hover_data={'Cluster': data['Cluster']},
        color_continuous_scale='Viridis',
    )

    # Ajuste de Layout
    fig.update_layout(
        xaxis=dict(showgrid=True, zeroline=True),
        yaxis=dict(showgrid=True, zeroline=True),
        plot_bgcolor="white",
        title=dict(x=0.5, font=dict(size=20)),
        legend_title="Cluster",
        legend=dict(traceorder="normal"),
    )

    return data, fig.to_html(full_html=False)