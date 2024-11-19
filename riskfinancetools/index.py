import pandas as pd
import riskfinancetools as rf
import clustering as ctr

# Não funcionou: 'ENBR3.SA'(energia) 
# 'VVAR3.SA', 'BTOW3.SA'(Varejo) 
# 'BRDT3.SA' (Mineração)
#  'LINX3.SA' (tecnologia)
# 'PARD3.SA' (Saúde)

carteira_energia = ['TAEE11.SA', 'EQTL3.SA', 'CMIG4.SA', 'CPLE6.SA']
carteira_financeiro = ['ITUB4.SA', 'BBDC4.SA', 'SANB11.SA', 'BBAS3.SA', 'BPAC11.SA'] #todas funcionaram no período de 4 anos
carteira_varejo = ['MGLU3.SA', 'LREN3.SA', 'AMAR3.SA']
carteira_mineracao = ['VALE3.SA', 'GGBR4.SA', 'CSNA3.SA', 'USIM5.SA', 'BRAP4.SA'] #todas funcionaram no período de 4 anos
carteira_petroleo_gas = ['PETR4.SA', 'PRIO3.SA', 'RRRP3.SA', 'UGPA3.SA']
carteira_tecnologia = ['WEGE3.SA', 'POSI3.SA', 'TOTS3.SA', 'LWSA3.SA']
carteira_alimentos_bebidas = ['ABEV3.SA', 'JBSS3.SA', 'BRFS3.SA', 'MDIA3.SA', 'SMTO3.SA'] #todas funcionaram no período de 4 anos
carteira_saude = ['RDOR3.SA', 'HAPV3.SA', 'QUAL3.SA', 'FLRY3.SA']
carteira_construcao = ['EZTC3.SA', 'MRVE3.SA', 'CYRE3.SA', 'TEND3.SA', 'TRIS3.SA'] #todas funcionaram no período de 4 anos
carteira_logistica = ['RAIL3.SA', 'GOLL4.SA', 'AZUL4.SA', 'ECOR3.SA', 'TUPY3.SA'] #todas funcionaram no período de 4 anos

year = 2022
start = "2016-01-01"
end = "2024-11-01"

#Filtragem
#filteredData = rf.filtering('CSV/statusinvest-busca-avancada.csv', year=year)
filteredData = rf.filtering('CSV/statusinvest-busca-avancada.csv', startDate=start, endDate=end)

#Análise de volatilidade e retorno x risco
#evaluatedData = rf.walletAnalisys(year=year, market='^BVSP', wallet=filteredData['TICKER'].to_list())
evaluatedData = rf.walletAnalisys(startDate=start, endDate=end, market='^BVSP', wallet=filteredData['TICKER'].to_list())
#evaluatedData = rf.walletAnalisys(startDate=start, endDate=end, market='^BVSP', wallet=carteira_financeiro)
print(evaluatedData)


#análise do cluster e geração do mesmo
silhoueteDataFrame = ctr.evaluate_cluster(csvData='CSV/stocksData.csv', max_clusters=10)
print(silhoueteDataFrame)

clusteringDataframe = ctr.clusteringKmeans(csvData='CSV/stocksData.csv', displayPlot=True)
clustersDataFrame = ctr.generate_cluster_dataframes('CSV/clusters.csv', 'CSV/stocksData.csv', 3)

for cluster_name, cluster_dataframe in clustersDataFrame.items():
    print("\n")
    print(cluster_name)
    print(cluster_dataframe)