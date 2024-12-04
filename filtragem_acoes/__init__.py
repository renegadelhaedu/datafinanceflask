from flask import Blueprint, current_app, render_template, session, request, redirect, url_for
import pandas as pd



filtragem_bp = Blueprint('filtragem', __name__)

@filtragem_bp.route('/')
def exibir_acoes_filtradas():
    dados = pd.read_pickle('data/filtragem_acoes.pkl')

    table_html = dados.to_html(classes="table table-striped", index=False, border=0)
    return render_template("filtragemacoes.html", table=table_html)




