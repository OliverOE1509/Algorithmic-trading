import numpy as np
import pandas as pd
import os
from db import DBHelper     # A script with helper functions to be used for SQL statements 
import pymysql
from sqlalchemy import create_engine
import mysql.connector
from datetime import datetime
import matplotlib.pyplot as plt
import datetime
import math
import sqlite3

import pprint 
pp = pprint.PrettyPrinter(indent=4)

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
        self.dbh = DBHelper()
        self.tp = 0
        self.sl = 0
        self.buy_trades_acknowledged = pd.DataFrame(columns = ['date', 'Close', 'tick', 'buy'])
        self.sell_trades_acknowledged = pd.DataFrame(columns = ['date', 'Close', 'tick', 'sell'])

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
            #fd = open('Kurser.sql', 'r')
            #sqlfile = fd.read(f'SELECT * FROM Kurser WHERE Ticker = "{str(symbol)}" AND Dato >= "2023-01-01" ORDER BY Dato ASC')
            #print(sqlfile)
            return connection
        except Exception as e:
            return 'Det var et problem med databasekoblingen', e


    def format_connection(self, symbol):
        print('\nformaterer kobling')
        '''Utfører sql spørring for å hente ut data til symbol'''

        # conn = sqlite3.connect('lokalKurser.db')
        # cursor = conn.cursor()
        sql = f'SELECT * FROM Kurser WHERE Ticker = "{str(symbol)}" AND Dato >= "2023-01-01" ORDER BY Dato ASC'
        # cursor.execute(sql)
        # #self.dbh.fetch(sql)
        # result = cursor.fetchall()
        # for i in result:
        #     print(i)

        cnx = sqlite3.connect('lokalKurser.db')
        self.data = pd.read_sql_query(sql, cnx)
        #print(self.data.info())
        cnx.commit()
        cnx.close()
        self.data['Dato'] = pd.to_datetime(self.data['Dato'])
        self.data['Ticker'] = self.data['Ticker'].astype(str)
        return self.data
        # self.data = pd.read_sql(sql, con = self.connection)
        # self.data['Dato'] = pd.to_datetime(self.data['Dato'])
        # self.data['Ticker'] = self.data['Ticker'].astype(str)

        # return self.data

    def get_units(self, bar):
        date, Close = self.get_date_price(bar)
        amount_to_invest = self.amount / len(self.symbol)
        units = math.floor(amount_to_invest / Close)

        return units



    def get_date_price(self, bar, sym):
        '''Return date and price for a bar'''
        date = self.d[f'{sym}']['data'].Dato.iloc[bar]
        price = self.d[f'{sym}']['data'].Close_.iloc[bar]
        #print(type(date))
        date = date.date()

        return date, price


    def get_net_wealth_buy(self, bar, sym):
        '''print current running net wealth'''
        date, Close = self.get_date_price(bar, sym)
        net_wealth = self.d[f'{sym}']['units'] * Close + self.d[f'{sym}']['amount']

        return {'date': date, 'net_wealth': net_wealth}

    
    def place_buy_order(self, bar, units, amount, sym, activate_insert = False):
        '''Place buy order'''
        date, Close = self.get_date_price(bar, sym)
        if units is None:
            units = math.floor(self.d[f'{sym}']['amount'] / Close)
        else:
            units = self.get_units(bar)

        if (units * Close) * (1 + self.ptc ) + self.ftc > self.d[f'{sym}']['amount']:
            pass
        else: 
            self.d[f'{sym}']['amount'] -= (units * Close) * (1 + self.ptc ) + self.ftc
            self.d[f'{sym}']['net_wealth'] = Close * units + self.d[f'{sym}']['amount']
            self.d[f'{sym}']['position'] = 1
            self.d[f'{sym}']['units'] += units

            self.buy_trades_acknowledged.loc[bar] = [date, Close, f'{sym}', 'buy']
            self.trades += 1

          
    def place_sell_order(self, bar, units, sym, amount = None, activate_insert = False):
        '''Place sell order'''
        date, Close = self.get_date_price(bar, sym)
        if amount is None:
            amount = self.d2[bar-1][f'{sym}']['units']

        self.d[f'{sym}']['net_wealth'] = Close * units + self.d[f'{sym}']['amount']
        self.d[f'{sym}']['amount'] += ((units * Close) * (1 + self.ptc ) + self.ftc)
        self.d[f'{sym}']['position'] = 0
        self.d[f'{sym}']['units'] -= units

        self.sell_trades_acknowledged.loc[bar] = [date, Close, f'{sym}', 'sell']
        self.trades += 1

    def get_entry_exit_pts(self):
        '''
        This function gets the time and portfolio value we enter and exit all positions at. Only related to the final graph
        '''
        self.total_net_wealth_development = []
        for key, value in self.d2.items():
            sum_netWealth_i = []
            for u in self.symbol:
                sum_netWealth_i.append(value[f'{u}']['net_wealth'])
            self.total_net_wealth_development.append([key, value[f'{u}']['date'], sum(sum_netWealth_i)])
        nw_df = pd.DataFrame(data = [(u, k, v) for u, k, v in self.total_net_wealth_development], columns = ['bar', 'date', 'value'])
        nw_df.set_index('date', inplace = True)
        nw_df.index = pd.to_datetime(nw_df.index)
        self.buy_trades_acknowledged = self.buy_trades_acknowledged.reset_index().set_index('date')
        self.sell_trades_acknowledged = self.sell_trades_acknowledged.reset_index().set_index('date')
        buy_idx = nw_df.index.intersection(self.buy_trades_acknowledged.index)
        sell_idx = nw_df.index.intersection(self.sell_trades_acknowledged.index)
        buy_trades = nw_df.loc[buy_idx]
        sell_trades = nw_df.loc[sell_idx]

        buy_trades['tick'] = self.buy_trades_acknowledged['tick'].values
        sell_trades['tick'] = self.sell_trades_acknowledged['tick'].values

        # Now for plotting the entry and exit pts for each stock
        plt.figure(figsize = (10,7))
        for i, label in enumerate(buy_trades['tick']):
            plt.text(buy_trades.index[i], buy_trades.value.iloc[i], label, fontsize = 8, ha = 'right')

        for i, label in enumerate(sell_trades['tick']):
            plt.text(sell_trades.index[i], sell_trades.value.iloc[i], label, fontsize = 8, ha = 'right')

        plt.plot(nw_df['value'], color = 'black', label = 'equity')
        plt.scatter(buy_trades.index, buy_trades.value, color = 'green', label = 'buy', marker = '^')
        plt.scatter(sell_trades.index, sell_trades.value, color = 'red', label = 'sell', marker = 'v')
        #plt.title(f'Equity development of strategi number {self.portfolioID}', font = 16)
        plt.grid()
        plt.show()

