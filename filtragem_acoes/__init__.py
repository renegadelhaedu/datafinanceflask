from flask import Blueprint, current_app, render_template, session, request, redirect, url_for
import pandas as pd
import dataAnalise as da


filtragem_bp = Blueprint('filtragem', __name__)

@filtragem_bp.route('/')
def exibir_acoes_filtradas():
    dados = pd.read_pickle('data/filtragem_acoes.pkl')

    dados.drop(dados[dados['margemGordon'] < -100].index, inplace=True)
    dados = da.computarRankingFundamentos(dados)
    dados.sort_values(by=['notaMedia'], ascending=False, inplace=True)

    table_html = dados.to_html(classes="table table-striped", index=True, border=1)
    return render_template("filtragemacoes.html", table=table_html)




