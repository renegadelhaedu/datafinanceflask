import pathlib
from flask import *
import dataAnalise as da
import grafico as gr
import atualizar
import dao 
import carteira as gf
import yfinance as yf


app = Flask(__name__)
app.secret_key = '6#aASD675@'

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/gerarmoduloanalise')
def gerarmoduloanalise():
    return render_template('logado.html')

@app.route('/retornar')
def retornar():
    if 'user' in session:
        user = session['user']
        return render_template('logado.html', name=nome, state=estado, profession=profissao)
    else:
        return redirect(url_for('verificarlogin'))


@app.route('/register', methods=['POST','GET'])
def registrar_user():
        
        dao.conectardb()

        if request.method == 'GET':
            return render_template('cadastro.html')
        
        else:
            nome = request.form['nome']
            email = request.form['email']
            estado = request.form['estado']
            profissao = request.form['profissao']
            senha = request.form['senha']

        if dao.inserir_user(nome,email,estado,profissao,senha):
            return render_template('login.html')
        else:
            return render_template('cadatro.html', msg='erro ao inserir usuário')


@app.route('/verificarlogin', methods=['POST','GET'])
def verificarlogin():

    dao.conectardb()

    user = request.form.get('username')
    senha = request.form.get('password')

    saida = dao.login(user, senha)
    nome = saida[0][0]
    estado = saida[0][1]
    profissao = saida[0][2]
    
    if dao.login(user, senha):
        session['user'] = user
        return render_template('logado.html', name=nome, state=estado, profession=profissao)
    else:
        return render_template('login.html',msg_erro='usuário ou senha incorreta')
    
@app.route('/teste')
def teste():
    return render_template('hometeste.html')

@app.route('/cadastro')
def registro_page():
    return render_template('cadastro.html')

@app.route('/carteira')
def carteira():
    return render_template('carteira.html')

@app.route('/calcularRiscoRetorno/<opcao>', methods=['GET','POST'])
def calcularRiscoRetorno(opcao):
    df_final = da.readRiscoRetornoFile(opcao)
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

@app.route('/correlacaoindicadores', methods=['POST','GET'])
def correlacaoallindicadores():
    if request.method == 'GET':
        dataCorr = da.readCorrelacoesIndicFile('all')
    else:
        dataCorr = da.readCorrelacoesIndicFile('minhas')

    return render_template('correlationindicadores.html',
                           plot=gr.gerarGrafCorrIndicAll3D(dataCorr))

@app.route('/atualizarcorrelacaoindicadores')
def atualizarcorrelacaoallindicadores():
    atualizar.atualizar()
    return redirect('/correlacaoindicadores')

@app.route('/gerariframeprincipal')
def gerariframeprincipal():
    pares = da.pegarcotacoes()

    return render_template('Carousel.html', pares=pares)

@app.route('/gerariframecard')
def gerariframecard():
    pares = da.gerar_listas_acoes_cotacoes()

    return render_template('cardActions.html', pares=pares)

@app.route('/exibirdetalhesacao/<nome>', methods=['GET'])
def exibir_detalhes_acao(nome):
    tick = yf.Ticker(nome + '.SA')
    info = tick.info

    graf, valor_acao= gr.dados_acao(nome)
    return render_template('dataActions.html', plot=graf, nome=nome, valor=round(valor_acao,2), info=info)

@app.route("/gerarminhacarteira")
def gerarminhacarteira():
    data, grid = gf.gerarPercentuais()
    lista = [['ticker', 'percentual']]
    for key, val in data.items():
        lista.append([key, val])

    return render_template('minhacarteira.html', data=lista, grid=grid)

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