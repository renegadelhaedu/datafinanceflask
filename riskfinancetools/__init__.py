from flask import Blueprint, render_template, session, request, redirect, url_for
from .clustering import clusteringKmeans
from .filtering import filtering
from .portfolio_analisys import walletAnalisys
from pandas import read_csv
from datetime import datetime

riscoretorno_bp = Blueprint('risco_retorno', __name__)

@riscoretorno_bp.route('/clustering', methods=['GET'])
def show_clustering():
    dataframe, graphic = clusteringKmeans(csvData='data/stocksData.csv')

    print(dataframe)

    return render_template('clustering_analisys.html', graphic_html=graphic)

@riscoretorno_bp.route('/updateCsv', methods=['GET'])
def update_dataStocks():
    year = 2022
    start = "2022-01-01"
    end = "2024-11-19"
    # currentDate = datetime.now()
    # end = f'{str(currentDate.year)}-{str(currentDate.month)}-{str(currentDate.day)}'

    #usar a lib os para tentar encontrar esse arquivo se não gerar uma thread para rodar a função filtering
    try:
        #filteredData = rf.filtering('data/statusinvest-busca-avancada.csv', year=year)
        filteredData = filtering('data/statusinvest-busca-avancada.csv', startDate=start, endDate=end)
        listTickersFiltered = read_csv('data/acoes_filtradas.csv')['TICKER'].to_list()
        evaluatedData = walletAnalisys(wallet=listTickersFiltered, market='^BVSP', startDate=start, endDate=end)
    except Exception as e:
        print(f'Error updating data: {e}')
        return redirect(url_for('logado'))

    return redirect(url_for('risco_retorno.show_clustering'))