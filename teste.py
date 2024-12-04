import yfinance as yf
import numpy as np
import pandas as pd
import random
from deap import base, creator, tools, algorithms
import dao

print(yf.download(['BBAS3.SA', 'BBDC4.SA'], period='10y'))
def ag_mult(num_acoes, tickers):

    if type(tickers) is list:
        tickers = [x + '.SA' for x in tickers]
    else:
        tickers = [x + '.SA' for x in tickers.keys()]

    def get_stock_data(tickers):
        data = yf.download(tickers, period='10y')["Adj Close"]
        returns = data.pct_change().dropna()
        daily_returns = returns.mean()
        annualized_returns = daily_returns * 252  # 252 dias úteis por ano
        annual_returns_data = returns.resample('YE').apply(lambda x: (1 + x).prod() - 1)
        annual_corr_matrix = annual_returns_data.corr()
        return annualized_returns, annual_corr_matrix

    annualized_returns, annual_corr_matrix = get_stock_data(tickers)

    print("Retornos Anualizados:")
    print(annualized_returns)

    print("\nMatriz de Correlação Anualizada:")
    print(annual_corr_matrix)

    mean_returns, corr_matrix = get_stock_data(tickers)

    creator.create("FitnessMulti", base.Fitness, weights=(1.0, -1.0))  # Maximizar retorno, minimizar correlação
    creator.create("Individual", list, fitness=creator.FitnessMulti)

    toolbox = base.Toolbox()
    toolbox.register("attr_item", lambda: random.randint(0, len(tickers) - 1))
    toolbox.register("individual", lambda: creator.Individual(random.sample(range(len(tickers)), num_acoes)))
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    def evaluate(individual):
        """
        Avalia o indivíduo com base em:
        1. Retorno médio dos ativos selecionados.
        2. Correlação média entre os ativos selecionados.
        """
        selected_tickers = [tickers[i] for i in individual]
        avg_return = np.mean([mean_returns[ticker] for ticker in selected_tickers])
        selected_corr = corr_matrix.loc[selected_tickers, selected_tickers]
        avg_corr = np.mean(selected_corr.to_numpy()[np.triu_indices(num_acoes, 1)])  # Média da parte superior da matriz
        return avg_return, avg_corr

    toolbox.register("evaluate", evaluate)
    toolbox.register("mate", tools.cxTwoPoint)
    toolbox.register("mutate", tools.mutUniformInt, low=0, up=len(tickers) - 1, indpb=0.1)
    toolbox.register("select", tools.selNSGA2)  # Seleção para problemas multiobjetivo

    # Função para corrigir duplicatas
    def fix_individual(individual):
        unique_individual = list(set(individual))
        while len(unique_individual) < num_acoes:
            new_gene = random.choice(range(len(tickers)))
            if new_gene not in unique_individual:
                unique_individual.append(new_gene)
        individual[:] = unique_individual
        return individual

    # Aplicar correção após mutação e cruzamento
    def mate_and_fix(ind1, ind2):
        tools.cxTwoPoint(ind1, ind2)
        fix_individual(ind1)
        fix_individual(ind2)
        return ind1, ind2  # Retorna os indivíduos corrigidos

    def mutate_and_fix(ind):
        tools.mutUniformInt(ind, low=0, up=len(tickers) - 1, indpb=0.1)
        fix_individual(ind)
        return ind,  # Retorna o indivíduo corrigido como uma tupla

    toolbox.register("mate", mate_and_fix)
    toolbox.register("mutate", mutate_and_fix)

    # Criar população inicial e executar o algoritmo genético
    pop = toolbox.population(n=20)
    ngen = 100
    cxpb, mutpb = 0.5, 0.2

    # Estatísticas para acompanhar o progresso
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", np.mean, axis=0)
    stats.register("min", np.min, axis=0)
    stats.register("max", np.max, axis=0)

    # Executar o algoritmo genético
    algorithms.eaMuPlusLambda(pop, toolbox, mu=100, lambda_=200, cxpb=cxpb, mutpb=mutpb, ngen=ngen,
                              stats=stats, verbose=True)

    # Selecionar o melhor indivíduo (não dominado) com base no retorno
    pareto_front = tools.sortNondominated(pop, len(pop), first_front_only=True)[0]
    best_ind = max(pareto_front, key=lambda ind: ind.fitness.values[0])  # Baseado no retorno
    best_tickers = [tickers[i] for i in best_ind]

    print("Melhores indivíduo:", best_ind)
    print("Tickers selecionados:", best_tickers)
    print("Retorno médio:", evaluate(best_ind)[0])
    print("Correlação média:", evaluate(best_ind)[1])

    return best_tickers, evaluate(best_ind)[0], evaluate(best_ind)[1]

a = ag_mult(5, {'BBAS3': 0, 'BBDC4': 0, 'VALE3': 0, 'SUZB3': 0, 'ITUB4': 0, 'PETR4': 0, 'AGRO3': 0})
