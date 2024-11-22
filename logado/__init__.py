from flask import Blueprint, current_app, render_template, session, request, redirect, url_for

import dataAnalise
import grafico
import dao
from threading import Thread


carteira_session = {}

def pegar_carteira_thread(login):
    carteira_session['carteira'] = dao.get_carteira(login)

logado_bp = Blueprint('logado', __name__)

@logado_bp.route('/<pagina>')
def pagina_iframe_logado(pagina):

    if 'user' in session and pagina == 'principal':
        if 'carteira' not in session:
            print('nao tava na sessao principal')
            Thread(target=pegar_carteira_thread, args=(session['user'][3],)).start()

        return render_template('iframelogado.html', login=session['user'][3])


@logado_bp.route('/rentabilidadecarteira/<login>')
def calcular_rentabilidade_carteira(login):

    if 'carteira' not in session:
        print('nao tava na sessao rentabilciarteira')
        session['carteira'] = carteira_session['carteira']

    dados = dataAnalise.rentabilidadeAcumulada('no Mês', login, session['carteira'])
    figura = grafico.gerarGraficoRentabilidadeAcumulada(dados)

    return render_template('rentabilidadeacumulada.html', plot=figura)


@logado_bp.route('/riscoretorno/<login>')
def gerar_graf2d_risco_retorno(login):

    if 'carteira' not in session:
        print('nao tava na sessao risco retorno')
        session['carteira'] = carteira_session['carteira']

    data = dataAnalise.calcularRiscoRetJanelasTemp(session['carteira'].keys())

    figura = grafico.gerarGrafRiscRet(data)

    return render_template('grafico2driscoretorno.html', plot=figura)
