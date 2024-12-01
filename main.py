import pathlib
from flask import *
import dataAnalise as da
import grafico as gr
import carteira as cart
import atualizar
import dao 


app = Flask(__name__)
app.secret_key = '6#aASD675@'
app.config['TICKERS'] = cart.get_codigos_acoes()

from minhacarteira import  minhacarteira_bp
from riskfinancetools import riscoretorno_bp
from logado import logado_bp
#from filtragem_acoes import filtragem_bp


app.register_blueprint(minhacarteira_bp, url_prefix="/acoes")
app.register_blueprint(riscoretorno_bp, url_prefix="/riscoretorno")
app.register_blueprint(logado_bp, url_prefix="/logado")
#app.register_blueprint(filtragem_bp, url_prefix="/filtragem")

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route("/mainpage")
def mainpage ():
    return render_template('mainpage.html', name=session['user'][0], profession=session['user'][1])


@app.route('/gerarmoduloanalise')
def gerarmoduloanalise():
    return render_template('logado.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    session.pop('carteira', None)

    return make_response(render_template('home.html'))

@app.route('/homepageuser')
def retornar():
    if 'user' in session:
        user = session['user']
        nome = user[0]
        profissao = user[1]
        return render_template('mainpage.html', name=nome, profession=profissao)
    else:
        return redirect(url_for('verificarlogin'))


@app.route('/registernewuser', methods=['POST', 'GET'])
def registrar_user():
    if request.method == 'GET':
        return render_template('register.html')

    else:
        nome = request.form.get('nome')
        email = request.form.get('email')
        profissao = request.form.get('profissao')
        senha = request.form.get('senha')

    if dao.inserir_user(nome, email, profissao, senha):
        return render_template('home.html')
    else:
        return render_template('register.html', msg='Erro ao inserir usuário')


@app.route('/verificarlogin', methods=['POST','GET'])
def verificarlogin():

    if request.method == 'POST':

        login = request.form.get('username')
        senha = request.form.get('password')

        usuario = dao.login(login, senha)

        if len(usuario) > 0:
            session['user'] = usuario[0]
            return render_template('mainpage.html', name=session['user'][0], profession=session['user'][1])
        else:
            return render_template('home.html',msg_erro='usuário ou senha incorreta')

    elif request.method == 'GET' and 'user' in session:
        return render_template('mainpage.html', name=session['user'][0], profession=session['user'][1])

    else:
        return render_template('home.html')


@app.route('/teste')
def teste():
    return render_template('hometeste.html')


@app.route('/carteira')
def carteira():
    if 'user' in session:
        return render_template('minhacarteira.html')
    else:
        return render_template('home.html')

@app.route('/calcularRiscoRetorno/<opcao>', methods=['GET','POST'])
def calcularRiscoRetorno(opcao):
    df_final = da.readRiscoRetornoFile(opcao)
    print(df_final.columns)
    return render_template('calcRiscoRet.html', plot=gr.gerarGrafRiscRet(df_final))


@app.route('/correlacaoindividual', methods=['POST','GET'])
def correlacaotickerindicador():
    if request.method == 'POST':
        indicador = request.form.get('indicador_radio')
        ticker = str(request.form.get('ticker'))
        correlacao, graficodados = da.gerarcorrelacaoindividual(ticker, indicador)
        return render_template('correlationindicador.html', correlac=correlacao, plot=gr.gerarGrafCorrInd(graficodados,indicador))
    else:
        return render_template('correlationindicador.html')


@app.route('/gerariframeprincipal')
def gerariframeprincipal():
    pares = da.pegarcotacoes()

    return render_template('Carousel.html', pares=pares)


@app.route('/gerariframecard')
def gerariframecard():
    pares = da.pegar_maiores_empresas()
    return render_template('cardActions.html', pares=pares)


@app.route('/rankingdividendos/<opcao>', methods=['GET','POST'])
def gerarrankingdividendos(opcao):
    if opcao == 'all':
        data = da.readRankingDividendos('all')
    else:
        data = da.readRankingDividendos('minhas') 

    return render_template('rankingdividendos.html', plot=gr.gerarBarGrafDividendos(data))

@app.route('/rankingacoes/<opcao>', methods=['GET', 'POST'])
def gerarrankingvalores(opcao):
    if opcao == 'all':
        caminho_arquivo = pathlib.Path('data/statusinvest-busca-avancada.csv').resolve()
    else:
        caminho_arquivo = pathlib.Path('data/statusinvest-busca-avancada.csv').resolve()

    data = gr.lerDadosCSV(caminho_arquivo)
 
    plot_html = gr.gerarBarGrafValores(data)
    
    return render_template('rankingacao.html', plot=plot_html)

@app.route('/actions')
def actions():
    return render_template('actions.html')



if __name__ == "__main__":
    app.run(debug=True)