import yahoo_fin.stock_info as yf
import pandas as pd
import plotly.express as px


def tickers():
    t = []
    #t =yf.tickers_ftse100()
    nt = int(input('Insert number of stock:'))
    for i in range(nt):
        ticker = str(input('''Insert the ticker of the stock number ''' + str(i) + ':'))
        t.append(ticker)
    return t


def correct(balance_sheet):
    balance_sheet = balance_sheet.fillna(0)

    try:
        balance_sheet['longTermDebt']
    except:
        balance_sheet['longTermDebt'] = [0, 0, 0, 0]
    try:
        balance_sheet['shortLongTermDebt']
    except:
        balance_sheet['shortLongTermDebt'] = [0, 0, 0, 0]
    try:
        balance_sheet['cash']
    except:
        balance_sheet['cash'] = [0, 0, 0, 0]
    try:
        balance_sheet['shortTermInvestments']
    except:
        balance_sheet['shortTermInvestments'] = [0, 0, 0, 0]
    try:
        balance_sheet['preferredStock']
    except:
        balance_sheet['preferredStock'] = [0, 0, 0, 0]

    return balance_sheet


def Calculation_ROIC_FAUSTMANN(t):
    ROIC = []
    FAUSTMANN = []
    lista = []

    for x in t:

        try:
            balance_sheet = yf.get_balance_sheet(x)
            balance_sheet = balance_sheet.T
            balance_sheet = correct(balance_sheet)
            totalAssets = balance_sheet['totalAssets']
            totalLiab = balance_sheet['totalLiab']
            longTermDebt = balance_sheet['longTermDebt']
            shortLongTermDebt = balance_sheet['shortLongTermDebt']
            totalStockholderEquity = balance_sheet['totalStockholderEquity']
            cash = balance_sheet['cash'] + balance_sheet['shortTermInvestments']
            preferredStock = balance_sheet['preferredStock']

            BookValueEquity = totalAssets.iloc[0] - totalLiab.iloc[0]
            Debt = longTermDebt.iloc[0] + shortLongTermDebt.iloc[0]
            InvestedCapital = totalStockholderEquity[0] + Debt - cash[0]

            income_statement = yf.get_income_statement(x)
            ebit = income_statement.T['ebit']
            ROIC.append(ebit[0] / InvestedCapital)

            MarketCap = yf.get_quote_table(x, dict_result=False).iloc[11, 1]
            if MarketCap[-1] == "B":
                MarketCap = MarketCap.replace("B", "")
                MarketCap = float(MarketCap)
                MarketCap = MarketCap * 1000000000
            elif MarketCap[-1] == "M":
                MarketCap = MarketCap.replace("M", "")
                MarketCap = float(MarketCap)
                MarketCap = MarketCap * 1000000
            else:
                MarketCap = MarketCap.replace("T", "")
                MarketCap = float(MarketCap)
                MarketCap = MarketCap * 1000000000000

            FAUSTMANN.append(MarketCap / totalStockholderEquity[0])
        except:
            lista.append(x)
            continue

    for x in lista:
        t.remove(x)

    Data = {'Ticker': t, 'ROIC': ROIC, 'FAUSTMANN': FAUSTMANN}
    SIGFRIDS = pd.DataFrame(Data)

    return SIGFRIDS


def Graphic(SIGFRIDS):
    fig = px.scatter(SIGFRIDS, x="ROIC", y="FAUSTMANN",
                     color='Ticker')
    return fig.show()


def Program():
    while True:
        t = tickers()
        SIGFRIDS = Calculation_ROIC_FAUSTMANN(t)
        excel = pd.ExcelWriter('Sigfrids.xlsx', engine='xlsxwriter')
        SIGFRIDS.to_excel(excel, sheet_name='Stocks')
        excel.save()
        Graphic(SIGFRIDS)
        while True:
            response = str(input('Do you want to visualize a new Graphic? (yes/no): '))
            if response in ('yes', 'no'):
                break
            print('Input not valid.')
        if response == 'yes':
            continue
        else:
            print('Bye')
            break


Program()
