import yahoo_fin.stock_info as yf
import pandas as pd
import plotly.express as px


def tickers():
    t = []
    #t =yf.tickers_ftse100()
    nt = int(input('Inserire numero di aziende da confrontare:'))
    for i in range(nt):
        ticker = str(input('''Inserisci ticker dell'impresa numero ''' + str(i) + ':'))
        t.append(ticker)
    return t


def correggi(stato_patrimoniale):
    stato_patrimoniale = stato_patrimoniale.fillna(0)

    try:
        stato_patrimoniale['longTermDebt']
    except:
        stato_patrimoniale['longTermDebt'] = [0, 0, 0, 0]
    try:
        stato_patrimoniale['shortLongTermDebt']
    except:
        stato_patrimoniale['shortLongTermDebt'] = [0, 0, 0, 0]
    try:
        stato_patrimoniale['cash']
    except:
        stato_patrimoniale['cash'] = [0, 0, 0, 0]
    try:
        stato_patrimoniale['shortTermInvestments']
    except:
        stato_patrimoniale['shortTermInvestments'] = [0, 0, 0, 0]
    try:
        stato_patrimoniale['preferredStock']
    except:
        stato_patrimoniale['preferredStock'] = [0, 0, 0, 0]

    return stato_patrimoniale


def Calcolo_ROIC_FAUSTMANN(t):
    ROIC = []
    FAUSTMANN = []
    lista = []

    for x in t:

        try:
            stato_patrimoniale = yf.get_balance_sheet(x)
            stato_patrimoniale = stato_patrimoniale.T
            stato_patrimoniale = correggi(stato_patrimoniale)

            totalAssets = stato_patrimoniale['totalAssets']
            totalLiab = stato_patrimoniale['totalLiab']
            longTermDebt = stato_patrimoniale['longTermDebt']
            shortLongTermDebt = stato_patrimoniale['shortLongTermDebt']
            totalStockholderEquity = stato_patrimoniale['totalStockholderEquity']
            cash = stato_patrimoniale['cash'] + stato_patrimoniale['shortTermInvestments']
            preferredStock = stato_patrimoniale['preferredStock']

            BookValueEquity = totalAssets.iloc[0] - totalLiab.iloc[0]
            Debt = longTermDebt.iloc[0] + shortLongTermDebt.iloc[0]
            InvestedCapital = totalStockholderEquity[0] + Debt - cash[0]

            conto_economico = yf.get_income_statement(x)
            ebit = conto_economico.T['ebit']
            ROIC.append(ebit[0] / InvestedCapital)

            MC = yf.get_quote_table(x, dict_result=False).iloc[11, 1]
            if MC[-1] == "B":
                MC = MC.replace("B", "")
                MC = float(MC)
                MC = MC * 1000000000
            elif MC[-1] == "M":
                MC = MC.replace("M", "")
                MC = float(MC)
                MC = MC * 1000000
            else:
                MC = MC.replace("T", "")
                MC = float(MC)
                MC = MC * 1000000000000

            FAUSTMANN.append(MC / totalStockholderEquity[0])
        except:
            lista.append(x)
            continue

    for x in lista:
        t.remove(x)

    Data = {'Ticker': t, 'ROIC': ROIC, 'FAUSTMANN': FAUSTMANN}
    SIGFRIDI = pd.DataFrame(Data)

    return SIGFRIDI


def Grafico(SIGFRIDI):
    fig = px.scatter(SIGFRIDI, x="ROIC", y="FAUSTMANN",
                     color='Ticker')
    return fig.show()


def Programma():
    while True:
        t = tickers()
        SIGFRIDI = Calcolo_ROIC_FAUSTMANN(t)
        excel = pd.ExcelWriter('AZIONI.xlsx', engine='xlsxwriter')
        SIGFRIDI.to_excel(excel, sheet_name='Azione')
        excel.save()
        Grafico(SIGFRIDI)
        while True:
            risposta = str(input('Vuoi visualizzare un nuovo grafico? (si/no): '))
            if risposta in ('si', 'no'):
                break
            print('Input non valido.')
        if risposta == 'si':
            continue
        else:
            print('Ciao')
            break


Programma()