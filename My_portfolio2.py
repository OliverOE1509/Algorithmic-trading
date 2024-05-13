import numpy as np
import pandas as pd
import os
from db import DBHelper
import pymysql
from sqlalchemy import create_engine
import mysql.connector
from datetime import datetime
import matplotlib.pyplot as plt
import datetime
import math

class Portefølje(object):
    def __init__(self, portfolioID, symbol, amount, ftc = 0.0, vtc = 0.0, verbose = False):
        self.symbol = symbol
        self.initial_amount = amount
        self.amount = amount
        self.ftc = ftc
        self.ptc = vtc
        self.units = 0
        self.position = 0
        self.trades = 0
        self.verbose = verbose
        self.portfolioID = portfolioID
        #self.equity_curve = {'date': [], 'net_wealth': []}
        self.equity_curve = []
        self.dbh = DBHelper()
        #self.data = self.format_connection()
        self.tp = 0
        self.sl = 0
        self.buy_trades = {'Date': [], 'buy_Close': []}
        self.sell_trades = {'Date': [], 'sell_Close': []}

        d = {}

        for symbol in self.symbol:
            inner_dict = {}
            inner_dict['data'] = self.format_connection(symbol)
            inner_dict['amount'] = self.initial_amount / len(self.symbol)
            inner_dict['net_wealth'] = self.initial_amount / len(self.symbol)
            inner_dict['position'] = 0
            inner_dict['units'] = 0
            d[f'{symbol}'] = inner_dict
        
        self.d = d
        #print(self.d)
    
    def make_sql_connection(self):
        print('\n')
        print("make sql conn")
    
        try:
            sqlEngine = create_engine('mysql+pymysql://oliver:Tyranno02@www.toliha.net/FinansDB', pool_recycle=3600)
            dbConnection = sqlEngine.connect()
            """ conn = mysql.connector.connect(host=self.host,
                                                database=self.db,
                                                user=self.user,
                                                password=self.pw) """
            return dbConnection
        except Exception as e:
            return 'Det var et problem med databasekoblingen', e


    def format_connection(self, symbol):
        print('\nformaterer kobling')
        '''Utfører sql spørring for å hente ut data til symbol'''
        self.connection = self.make_sql_connection()
        
        sql = f'SELECT * FROM Kurser WHERE Ticker = "{str(symbol)}" AND Dato >= "2023-01-01" ORDER BY Dato ASC'

        self.data = pd.read_sql(sql, con = self.connection)
        self.data['Dato'] = pd.to_datetime(self.data['Dato'])
        self.data['Ticker'] = self.data['Ticker'].astype(str)

        return self.data

    def get_units(self, bar):
        date, Close = self.get_date_price(bar)
        amount_to_invest = self.amount / len(self.symbol)
        units = math.floor(amount_to_invest / Close)
        #print(units)
        return units



    def get_date_price(self, bar, sym):
        '''Return date and price for a bar'''
        #date = self.data.Dato.iloc[bar]
        date = self.d[f'{sym}']['data'].Dato.iloc[bar]
        #price = self.data.Close_.iloc[bar]
        price = self.d[f'{sym}']['data'].Close_.iloc[bar]
        date = date.date()
        #print(f'Er i get_date_price, dato er        :       {date}      Close_  :       {price}')
        #print(f'\n')
        return date, price


    def get_net_wealth_buy(self, bar, sym):
        '''print current running net wealth'''
        date, Close = self.get_date_price(bar, sym)
        #net_wealth = self.units * Close + self.amount
        net_wealth = self.d[f'{sym}']['units'] * Close + self.d[f'{sym}']['amount']
        #print(f'{self.units} * {Close} + {self.amount}')

        return {'date': date, 'net_wealth': net_wealth}

    
    def place_buy_order(self, bar, units, amount, sym, activate_insert = False):
        '''Place buy order'''
        date, Close = self.get_date_price(bar, sym)
        if units is None:
            units = math.floor(self.d[f'{sym}']['amount'] / Close)
        else:
            units = self.get_units(bar)

        
        #print(f' amount kjøp {sym}: {(units * Close) * (1 + self.ptc ) + self.ftc}')
        

        self.d[f'{sym}']['amount'] -= (units * Close) * (1 + self.ptc ) + self.ftc
        #self.d[f'{sym}']['net_wealth'] = self.d[f'{sym}']['data'].Close_.iloc[bar] * self.d[f'{sym}']['units'] + self.d[f'{sym}']['amount']
        self.d[f'{sym}']['net_wealth'] = Close * units + self.d[f'{sym}']['amount']
        self.d[f'{sym}']['position'] = 1
        self.d[f'{sym}']['units'] += units
        #print(self.d[f'{sym}']['net_wealth'], self.d[f'{sym}']['amount'], self.d[f'{sym}']['position'], self.d[f'{sym}']['units'])


        #print(f'BUY net wealth at bar {bar} : {self.d[f'{sym}']['data'].Close_.iloc[bar], Close, self.d[f'{sym}']['units'], units, self.d[f'{sym}']['amount']}')
        #print(f'sum brukt til kjøp : {(units * Close) * (1 - self.ptc) - self.ftc} på dato {date}')

          
    def place_sell_order(self, bar, units, sym, amount = None, activate_insert = False):
        '''Place sell order'''
        date, Close = self.get_date_price(bar, sym)
        if amount is None:
            amount = self.d2[bar-1][f'{sym}']['units']

        #print(self.d[])
        #print(f' amount salg {sym}: {(units * Close) * (1 + self.ptc ) + self.ftc}')
        #print(f'SELL net wealth at bar {bar} : {self.d[f'{sym}']['data'].Close_.iloc[bar], Close, self.d[f'{sym}']['units'], units, self.d[f'{sym}']['amount']}')

        #print(f'sum brukt til kjøp : {(units * Close) * (1 - self.ptc) - self.ftc} på dato {date}')
        #self.d[f'{sym}']['net_wealth'] = self.d[f'{sym}']['data'].Close_.iloc[bar] * self.d[f'{sym}']['units'] + self.d[f'{sym}']['amount']
        self.d[f'{sym}']['net_wealth'] = Close * units + self.d[f'{sym}']['amount']
        self.d[f'{sym}']['amount'] += ((units * Close) * (1 + self.ptc ) + self.ftc)
        self.d[f'{sym}']['position'] = 0
        self.d[f'{sym}']['units'] -= units
        #print(self.d[f'{sym}']['net_wealth'], self.d[f'{sym}']['amount'], self.d[f'{sym}']['position'], self.d[f'{sym}']['units'])

