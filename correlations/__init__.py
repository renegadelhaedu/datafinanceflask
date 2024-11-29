import yfinance as yf
import numpy as np
import pandas as pd
import random
from deap import base, creator, tools, algorithms
import dao

def gerar_ag():
    #AG single objetivo
    #ser multiobjetivo no qual o critério de escolha do filho deveria ser baseada em 2 fatores:
    #maximizar o retorno e minimizar a correlação geral entre os ativos/acoes
    #impedir tickers duplicados na carteira final
    tickers = dao.getMinhasEmpresasListadas()
    if type(tickers) is list:
        tickers = [x + '.SA' for x in tickers]
    else:
        tickers = [x + '.SA' for x in tickers.keys()]

    def get_correlation_matrix(tickers):
        data = yf.download(tickers, period='10y')["Adj Close"]
        returns = data.pct_change().dropna()
        corr_matrix = returns.corr()
        return corr_matrix

    corr_matrix = get_correlation_matrix(tickers)

    creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMin)

    toolbox = base.Toolbox()
    toolbox.register("attr_item", lambda: random.randint(0, len(tickers) - 1))
    toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_item, n=10)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    def evaluate(individual):
        selected_tickers = [tickers[i] for i in individual]
        selected_corr = corr_matrix.loc[selected_tickers, selected_tickers]
        avg_corr = np.mean(selected_corr.to_numpy()[np.triu_indices(10, 1)])
        return avg_corr,

    toolbox.register("evaluate", evaluate)
    toolbox.register("mate", tools.cxTwoPoint)
    toolbox.register("mutate", tools.mutUniformInt, low=0, up=len(tickers) - 1, indpb=0.1)
    toolbox.register("select", tools.selTournament, tournsize=3)

    pop = toolbox.population(n=100)
    ngen = 50
    cxpb, mutpb = 0.5, 0.2

    result = algorithms.eaSimple(pop, toolbox, cxpb, mutpb, ngen, stats=None, verbose=True)

    best_ind = tools.selBest(pop, 1)[0]
    best_tickers = [tickers[i] for i in best_ind]
    print(best_ind)
    print(best_tickers)