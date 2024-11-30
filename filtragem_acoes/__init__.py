valuation_list = []
for index, row in selecao.iterrows():
    ticker = row['TICKER']
    try:
        median_dy = median_dy_dict[ticker + ".SA"]
        criteria_evaluation = {}

        #  Dividend Yield (DY)
        if row['DY'] >= median_dy * 1.2:  # DY 20% maior que a mediana
            criteria_evaluation['DY'] = 'Bom'
        elif row['DY'] >= median_dy:  # Pelo menos a mediana
            criteria_evaluation['DY'] = 'Ok'
        else:
            criteria_evaluation['DY'] = 'Ruim'

        #  P/L
        if row['P/L'] >= 10:
            criteria_evaluation['P/L'] = 'Bom'
        elif row['P/L'] <= 15:
            criteria_evaluation['P/L'] = 'Ok'
        else:
            criteria_evaluation['P/L'] = 'Ruim'

        #  P/VP
        if row['P/VP'] <= 1.5:
            criteria_evaluation['P/VP'] = 'Bom'
        elif row['P/VP'] <= 2:
            criteria_evaluation['P/VP'] = 'Ok'
        else:
            criteria_evaluation['P/VP'] = 'Ruim'

        #  Margem Líquida
        if row['MARG. LIQUIDA'] >= 0.20:
            criteria_evaluation['MARG. LIQUIDA'] = 'Bom'
        elif row['MARG. LIQUIDA'] >= 0.15:
            criteria_evaluation['MARG. LIQUIDA'] = 'Ok'
        else:
            criteria_evaluation['MARG. LIQUIDA'] = 'Ruim'

        #  ROE
        if row['ROE'] >= 0.20:
            criteria_evaluation['ROE'] = 'Bom'
        elif row['ROE'] >= 0.14:
            criteria_evaluation['ROE'] = 'Ok'
        else:
            criteria_evaluation['ROE'] = 'Ruim'

        #  Dívida Líquida / EBIT
        if row['DIVIDA LIQUIDA / EBIT'] <= 1.5:
            criteria_evaluation['DIVIDA LIQUIDA / EBIT'] = 'Bom'
        elif row['DIVIDA LIQUIDA / EBIT'] <= 2.5:
            criteria_evaluation['DIVIDA LIQUIDA / EBIT'] = 'Ok'
        else:
            criteria_evaluation['DIVIDA LIQUIDA / EBIT'] = 'Ruim'

        # Valuation
        current_price = yf.Ticker(ticker + ".SA").info.get("currentPrice")
        valuation = (median_dy * current_price) / 0.06
        valuation_list.append([ticker, row['DY'], median_dy, valuation, criteria_evaluation])

    except KeyError:
        print(f"Median DY not found for {ticker}")

valuation_df = pd.DataFrame(valuation_list,
                            columns=['Ticker', 'DY', 'Median DY', 'Valuation', 'Criterios Fundamentalistas'])
