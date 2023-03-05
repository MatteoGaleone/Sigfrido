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

def Calculation_ROE_PB(t):
    ROE = []
    PB = []
    lista = []

    for x in t:
        try:
            Return_on_equity=yf.get_stats(x).iloc[34,1]
            if Return_on_equity[-1] == "%":
                Return_on_equity = Return_on_equity.replace("%", "")
                Return_on_equity = float(Return_on_equity)
            ROE.append(Return_on_equity)
            
            Price_to_book_ratio=float(yf.get_stats_valuation(x).iloc[6,1])
            PB.append(Price_to_book_ratio)
            
        except:
            lista.append(x)
            continue

    for x in lista:
        t.remove(x)

    Data = {'Ticker': t, 'Return_on_equity': ROE, 'Price_to_book_ratio': PB}
    SIGFRIDS = pd.DataFrame(Data)
    return SIGFRIDS


def Graphic(SIGFRIDS):
    fig = px.scatter(SIGFRIDS, x="Return_on_equity", y="Price_to_book_ratio",
                     color='Ticker')
    return fig.show()


def Program():
    while True:
        t = tickers()
        SIGFRIDS = Calculation_ROE_PB(t)
        excel = pd.ExcelWriter('Sigfrids.xlsx', engine='xlsxwriter')
        SIGFRIDS.to_excel(excel, sheet_name='Stocks')
        excel.save()
        Graphic(SIGFRIDS)
        print(SIGFRIDS)
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
