from flask import Blueprint, render_template, session, request, redirect, url_for
from .clustering import clusteringKmeans
from .filtering import filtering
from .portfolio_analisys import walletAnalisys
from pandas import read_csv
from datetime import datetime
from dao import *

riscoretorno_bp = Blueprint('riscoretorno', __name__)

@riscoretorno_bp.route('/clustering', methods=['GET'])
def show_clustering():
    if 'user' in session:
        dataframe, graphic = clusteringKmeans(csvData='data/stocksData.csv')

        return render_template('clustering_analisys.html', graphic_html=graphic)
    else:
        return render_template('home.html')
    
@riscoretorno_bp.route('/indicadoresriscoretorno', methods=['GET'])
def calculate_inidicators_with_user_wallet():
    if 'user' in session:
        if 'carteira' not in session:
            session['carteira'] = get_carteira(session['user'][2])
        wallet = list(session['carteira'].keys())
        start = "2022-01-01"
        currentDate = datetime.now()
        end = f'{str(currentDate.year)}-{str(currentDate.month)}-{str(currentDate.day)}'

        indicatorsDataframe = walletAnalisys(wallet=wallet, market='^BVSP', startDate=start, endDate=end, exportCsv=False)
        indicators = indicatorsDataframe.to_dict(orient='records')
        print(indicatorsDataframe)

        return render_template('indicadores_riscoretorno.html', indicators=indicators)


@riscoretorno_bp.route('/updateCsv', methods=['GET'])
def update_dataStocks():
    if 'user' in session:
        try:
            start = "2014-01-01"
            end = "2024-12-31"
            filtering('data/statusinvest-busca-avancada.csv', startDate=start, endDate=end)
            listTickersFiltered = read_csv('data/acoes_filtradas.csv')['TICKER'].to_list()
            walletAnalisys(wallet=listTickersFiltered, market='^BVSP', startDate=start, endDate=end)
        except Exception as e:
            print(f'Error updating data: {e}')
            return redirect(url_for('mainpage'))

        return render_template('updatecsvanalisys.html')
    else:
        return render_template('home.html')