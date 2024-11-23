from flask import Blueprint, current_app, render_template, session, request, redirect, url_for
import yfinance as yf
import grafico as gr
import carteira as cart
import dataAnalise
import dao

minhacarteira_bp = Blueprint('acoes', __name__)

@minhacarteira_bp.route('/exibirdetalhesacao/<nome>', methods=['GET'])
def exibir_detalhes_acao(nome):
    tick = yf.Ticker(nome + '.SA')
    info = tick.info

    graf, valor_acao= gr.dados_acao(nome)
    return render_template('dataActions.html', plot=graf, nome=nome, valor=round(valor_acao,2), info=info)


@minhacarteira_bp.route('/adicionar', methods=['POST'])
def inserir_acao():
    if 'user' in session:
        codigo = request.form.get('codigo').upper()
        qtde = request.form.get('qtde')
        pmedio = request.form.get('precomedio') #falta fazer tratamento no front ------------
        email = session['user'][2]

        if codigo not in current_app.config['TICKERS']:
            return '<h2>Código de ação inválido</h2>' #criar pagina de erro ao inserir------------

        if dao.inserir_acao(email, codigo, qtde, pmedio):
            return redirect(url_for('acoes.gerarminhacarteira'))
        else:
            return '<h2>ação nao foi inserida</h2>' #criar pagina de erro ao inserir------------
    else:
        return render_template('home.html')


@minhacarteira_bp.route('/atualizar', methods=['POST'])
def atualizar_acao():
    if 'user' in session and 'carteira' in session:
        carteira_atualizada = dict()
        for acao in session['carteira'].keys():
            qtde_acao = int(request.form.get(acao))
            if qtde_acao != session['carteira'].get(acao):
                carteira_atualizada[acao] = qtde_acao

        if len(carteira_atualizada) > 0:
            if dao.atualizar_acoes(session['user'][2], carteira_atualizada):
                return redirect(url_for('acoes.gerarminhacarteira'))
            else:
                return redirect(url_for('acoes.gerarminhacarteira')) #falta fazer msg de erro ao atualizar
        else:
            return redirect(url_for('acoes.gerarminhacarteira')) #carteira nao modificada
    else:
        return redirect(url_for('acoes.gerarminhacarteira'))

@minhacarteira_bp.route('/excluir/<codigo>', methods=['GET'])
def excluir_acao(codigo):
    if 'user' in session:
        if dao.excluir_acao(session['user'][2], codigo):
            return redirect(url_for('acoes.gerarminhacarteira'))
        else:
            return redirect(url_for('acoes.gerarminhacarteira'))  # falta fazer msg de erro ao atualizar
    else:
        return render_template('home.html')

@minhacarteira_bp.route('/paginas/<string:metodo>')
def pagina_acoes_add(metodo):

    if metodo == 'adicionar' and 'user' in session:
        return render_template('adicionaracao.html')

    elif metodo == 'atualizar' and 'user' in session:
        if 'carteira' not in session:
            carteira = dao.get_carteira(session['user'][2])
            session['carteira'] = carteira

        lista = [(chave, session['carteira'].get(chave)) for chave in session['carteira'].keys()]
        return render_template('atualizaracao.html', acoes=lista)

    elif metodo == 'excluir' and 'user' in session:
        if 'carteira' not in session:
            carteira = dao.get_carteira(session['user'][2])
            session['carteira'] = carteira

        return render_template('excluiracao.html', acoes=session['carteira']) #---------falta fazer
    else:
        return render_template('minhacarteira.html')


@minhacarteira_bp.route("/dividendospagos")
def gerarrankingdividendos():
    if 'carteira' not in session:
        carteira = dao.get_carteira(session['user'][2])
        session['carteira'] = carteira

    dividen_df = dataAnalise.gerarrankingdividendos(session['carteira'].keys())

    fig = gr.gerarBarGrafDividendos(dividen_df)
    return render_template('rankingdividendos.html', plot=fig)


@minhacarteira_bp.route("/gerarminhacarteira")
def gerarminhacarteira():
    if 'user' in session:
        data, grid, dict_acoes = cart.gerarPercentuais(session['user'][2])
        session['carteira'] = dict_acoes
        if data is None:
            return render_template('adicionaracao.html')

        lista_percentuais = [['ticker', 'percentual']]
        for key, val in data.items():
            lista_percentuais.append([key, val])

        lista_qtde_acoes = []
        for key, val in dict_acoes.items():
            lista_qtde_acoes.append([key, val])

        return render_template('mostrarcarteira.html', data=lista_percentuais, grid=grid, listaqtde=lista_qtde_acoes)
    else:
        return render_template('home.html')
