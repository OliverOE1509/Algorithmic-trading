import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from My_portfolio_Github import *
import pprint 
pp = pprint.PrettyPrinter(indent=4)


pd.set_option('display.max_columns', 200)
pd.set_option('display.width', 1000)
pd.set_option('display.max_rows', 10000)

#stocks = ['AKRBP', 'DNB', 'AKAST']
	
#d = mp.Portefølje(1, stocks , 100000, ftc = 0.0, vtc = 0.0, verbose = False)
#print(d.data)

class portefoljø1(Portefølje):
	def strategi(self, SMA):
		'''
		This is a simple SMA strategy for illustrative purposes
		SMA: # of periods behind I calculate the simple moving average on
		'''
		'''Here I just create the SMA column for each stock. Recall the "self.d" dictionary I defined at the top of the
		parent class "Portefølje" in My_porfolio2.py''' 
		for i in self.d:
			self.d[f'{i}']['data']['SMA'] = self.d[f'{i}']['data'].Close_.rolling(SMA).mean()
			self.d[f'{i}']['data'] = self.d[f'{i}']['data'].dropna()


		'''Here I create a universal length for all dataframes of stock data I loop through. It starts by assigning the 
		length of  the first dataframe. Then I check if all other dataframes have equal lengths. If all lengths are equal,
		then nothing is changed.
		Otherwise, the dataframes have unequal lengths, and something is wrong.'''
		first_lens = len(self.d[self.symbol[0]]['data']) 
		if len(self.symbol) > 1:
			for i in self.symbol:
				if len(self.d[f'{i}']['data']) == first_lens:
					continue
				else:
					print("Unequal lengths of dfs")


		self.d2 = {}
		for bar in range(SMA, first_lens):
			self.c2 = {}
			for symbol, inner_dict in self.d.items():
				date, Close = self.get_date_price(bar, symbol)
				#self.net_wealth_curve.append()
				#print(bar)
				#print(self.d['net_wealth'])
				self.c2[f'{symbol}'] = {'amount' : inner_dict['amount'], 
								#'net_wealth' : inner_dict['net_wealth'],
								'net_wealth' : Close * inner_dict['units'] + inner_dict['amount'],
								'position' : inner_dict['position'], 
								'units' : inner_dict['units'],
								'date' : inner_dict['data']['Dato'].iloc[bar],
								'close' : Close}
				
				if inner_dict['position'] == 0:		# If I dont own this stock
					#print(inner_dict['amount'], symbol)
					#if inner_dict['amount'] > 0:

					if inner_dict['data'].Close_.iloc[bar] < inner_dict['data']['SMA'].iloc[bar]:
						#print(f'KJØP er i loop, dato er 		: 		{inner_dict['data'].Dato.iloc[bar]}		Close_	:		{inner_dict['data'].Close_.iloc[bar]}')
						self.place_buy_order(bar, units = None, amount = self.amount, sym = symbol)


				elif inner_dict['position'] == 1:	# If I already own this stock


					if inner_dict['data'].Close_.iloc[bar] > inner_dict['data']['SMA'].iloc[bar]:
						self.place_sell_order(bar, units = inner_dict['units'], sym = symbol)

			self.d2[bar] = self.c2
		self.get_entry_exit_pts() # Run the function that creates the equity curve, and the entry and exit pts to the corresponding stocks

	# Here is the end of the script
		





symbols = ['DNB', 'AKRBP', 'AKAST', 'BORR']
#obj = Portefølje(1, s, 100000, ftc = 0.0, vtc = 0.0, verbose = False)
#obj = portefoljø1(1, symbols, 100000, ftc = 0.0, vtc = 0.0, verbose = False)
#obj.strategi(30)
#print(type(obj.d))
#print(obj.d)

if __name__ == '__main__':
    def run_strategy():
        obj.strategi(50)
        print("Ferdig med run strategy")
    obj = portefoljø1(1, symbols, 100000, ftc = 0, vtc = 0, verbose = False)
    run_strategy()