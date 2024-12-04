from flask import Blueprint, current_app, render_template, session, request, redirect, url_for
import pandas as pd
import dataAnalise
import grafico
import dao
from threading import Thread
from correlations import ag_mult

carteira_session = {}

def pegar_carteira_thread(login):
    carteira_session['carteira'] = dao.get_carteira(login)



    
logado_bp = Blueprint('logado', __name__)

@logado_bp.route('/<pagina>')
def pagina_iframe_logado(pagina):

    if 'user' in session and pagina == 'principal':
        if 'carteira' not in carteira_session:
            Thread(target=pegar_carteira_thread, args=(session['user'][2],)).start()

        return render_template('iframelogado.html', login=session['user'][2])


@logado_bp.route('/rentabilidadecarteira/<login>')
def calcular_rentabilidade_carteira(login):

    if 'carteira' not in session:
        session['carteira'] = carteira_session['carteira']

    dados = dataAnalise.rentabilidadeAcumulada('no Mês', login, session['carteira'])
    figura = grafico.gerarGraficoRentabilidadeAcumulada(dados)

    return render_template('rentabilidadeacumulada.html', plot=figura)

@logado_bp.route('/riscoretorno/<login>')
def gerar_graf2d_risco_retorno(login):

    if 'carteira' not in session:
        session['carteira'] = carteira_session['carteira']

    data = dataAnalise.calcularRiscoRetJanelasTemp(session['carteira'].keys())

    figura = grafico.gerarGrafRiscRet(data)

    return render_template('grafico2driscoretorno.html', plot=figura)


@logado_bp.route('/correlacaoindicadoresmacro', methods=['GET'])
def correlacaoallindicadores():
    if 'carteira' not in session:
        session['carteira'] = carteira_session['carteira']

    #dataCorr = dataAnalise.gerarCorrelacoesCarteiraXindMacro(session['carteira'].keys())
    dataCorr = pd.read_pickle('data/correlacoesIndMacroAll.pkl')
    carteiraCorr = dataCorr[dataCorr.index.isin(session['carteira'].keys())]
    return render_template('correlationindicadores.html', plot=grafico.gerarGrafCorrIndicAll3D(carteiraCorr))


@logado_bp.route('/gerarmelhorcarteiraag', methods=['GET'])
def gerar_carteira_ideal_ag():
    try:
        num_acoes = session.get('num_acoes')
        tickers = session.get('tickers')

        if not num_acoes or not tickers:
            return "Configuração não encontrada. Configure primeiro o AG.", 400

        print(f"Configuração recuperada: num_acoes={num_acoes}, tickers={tickers}")  # Log para depuração

        resultados = ag_mult(num_acoes, tickers)

        print(f"Resultados obtidos: {resultados}")  # Log para ver se tá recevendo

        return render_template(
            'ag_carteira.html',
            melhores_tickers=resultados[0],
            retorno_medio=resultados[1],
            correlacao_media=resultados[2]
        )
    except Exception as e:
        print(f"Erro ao gerar a carteira ideal: {e}")
        return "Erro ao gerar a carteira ideal", 500


@logado_bp.route('/configurarag', methods=['GET', 'POST'])
def configurar_ag():
    if request.method == 'POST':
        try:
            num_acoes = int(request.form.get('num_acoes'))
            tickers = request.form.get('tickers').split(',')

            session['num_acoes'] = num_acoes
            session['tickers'] = {ticker.strip(): 0 for ticker in tickers}

            print(f"Configuração salva: num_acoes={num_acoes}, tickers={session['tickers']}")  # Log para depuração

            return redirect(url_for('logado.gerar_carteira_ideal_ag'))
        except Exception as e:
            print(f"Erro ao configurar AG: {e}")
            return "Erro ao configurar AG", 500

    return render_template('configurar_ag.html')
