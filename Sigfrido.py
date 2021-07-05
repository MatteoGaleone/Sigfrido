#!/usr/bin/env python
# coding: utf-8

import yahoo_fin.stock_info as yf
import pandas as pd
from pandas_datareader import data
import plotly.express as px

def tickers():
    t=[]
    nt=int(input('Inserire numero di aziende da confrontare:'))
    for i in range(nt):
        ticker=str(input('''Inserisci ticker dell'impresa numero ''' + str(i) +':'))
        t.append(ticker)
    return t

def correggi(stato_patrimoniale):
    stato_patrimoniale=stato_patrimoniale.fillna(0)
    try:
        stato_patrimoniale['totalAssets']
    except:
        stato_patrimoniale['totalAssets']=[0,0,0,0]
    try:
        stato_patrimoniale['totalLiab']
    except:
        stato_patrimoniale['totalLiab']=[0,0,0,0]
    try:
        stato_patrimoniale['longTermDebt']
    except:
        stato_patrimoniale['longTermDebt']=[0,0,0,0]
    try:
        stato_patrimoniale['shortLongTermDebt']
    except:
        stato_patrimoniale['shortLongTermDebt']=[0,0,0,0]

    return stato_patrimoniale
    
    
def Calcolo_ROIC_FAUSTMANN (t):
    ROIC=[]
    FAUSTMANN=[]
    s=[0,0,0,0]
    sp1=pd.DataFrame()
    i=0
    
    for x in t:
        sp1=pd.DataFrame()
        stato_patrimoniale=yf.get_balance_sheet(x)
        stato_patrimoniale=stato_patrimoniale.T
        stato_patrimoniale=correggi(stato_patrimoniale)
        sp1.insert(0, 'Book Value Equity', stato_patrimoniale['totalAssets']-stato_patrimoniale['totalLiab'])
        sp1.insert(0, 'Debt', stato_patrimoniale['longTermDebt']+stato_patrimoniale['shortLongTermDebt'])
        sp1.insert(0, 'Invested Capital', sp1['Book Value Equity']+sp1['Debt'])
    
        conto_economico=yf.get_income_statement(x)
        sp1.insert(0, 'ebit', conto_economico.T['ebit'])
        
        mc=data.get_quote_yahoo(x)['marketCap']
        s[0]=mc[0]
        sp1.insert(0, 'Market Cap', s)
    
        ROIC.append(sp1.iloc[0,1]/sp1.iloc[1,2])
        FAUSTMANN.append(sp1.iloc[0,0]/sp1.iloc[0,4])
    
    
    Data={'Ticker':t, 'ROIC':ROIC, 'FAUSTMANN':FAUSTMANN}
    SIGFRIDI=pd.DataFrame(Data)
    return SIGFRIDI
        

def Grafico(SIGFRIDI):
    fig = px.scatter(SIGFRIDI, x="ROIC", y="FAUSTMANN", 
                 color='Ticker')
    return fig.show()


def Programma():
    while True:
        t=tickers()
        SIGFRIDI=Calcolo_ROIC_FAUSTMANN(t)
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

