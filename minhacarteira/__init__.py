from flask import Blueprint, render_template, session, request, redirect, url_for
import yfinance as yf
import grafico as gr
import carteira as gf
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
        codigo = request.form.get('codigo') #falta verificar se o codigo da açao é valido
        qtde = request.form.get('qtde')
        pmedio = request.form.get('precomedio') #falta fazer tratamento ------------
        email = session['user'][3]

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
            if dao.atualizar_acoes(session['user'][3], carteira_atualizada):
                return redirect(url_for('acoes.gerarminhacarteira'))
            else:
                return redirect(url_for('acoes.gerarminhacarteira')) #falta fazer msg de erro ao atualizar
        else:
            return redirect(url_for('acoes.gerarminhacarteira'))


@minhacarteira_bp.route('/paginas/<string:metodo>')
def pagina_acoes_add(metodo):

    if metodo == 'adicionar' and 'user' in session:
        return render_template('adicionaracao.html')

    elif metodo == 'atualizar' and 'user' in session:
        carteira = dao.get_carteira(session['user'][3])
        session['carteira'] = carteira
        lista = [(chave, carteira.get(chave)) for chave in carteira.keys()]
        return render_template('atualizaracao.html', acoes=lista)

    elif metodo == 'excluir' and 'user' in session:
        return render_template('adicionaracao.html') #---------falta fazer
    else:
        return render_template('minhacarteira.html')

@minhacarteira_bp.route("/gerarminhacarteira")
def gerarminhacarteira():
    if 'user' in session:
        data, grid, dict_acoes = gf.gerarPercentuais(session['user'][3])
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
