import threading
import dataAnalise as da

def atualizarcorrInd3D(opcao):
    if opcao == 'all':
        da.gerarCorrelaAll('all').to_pickle('data/correlacoesIndAll3D.pkl')
    else:
        da.gerarCorrelaAll('minhas').to_pickle('data/correlacoesIndMinhas3D.pkl')


def atualizar():
    threading.Thread(target=atualizarcorrInd3D, args=("minhas",)).start()