import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from My_portfolio2 import *
import pprint 
pp = pprint.PrettyPrinter(indent=4)


pd.set_option('display.max_columns', 200)
pd.set_option('display.width', 1000)
pd.set_option('display.max_rows', 10000)

class portefoljø1(Portefølje):
	def strategi(self, SMA):

		"""Here I define the new column of interest, to determine when to buy and when to sell a stock."""
		for i in self.d:
			#print(self.d[f'{i}']['data'])
			self.d[f'{i}']['data']['SMA'] = self.d[f'{i}']['data'].Close_.rolling(SMA).mean()
			self.d[f'{i}']['data']['SMA'].dropna(inplace = True)

		

		"""Here I just define how many rows of data I have. The end result "first_lens", is an integer that is the total length of the data"""
		first_lens = len(self.d[self.symbol[0]]['data'])
		if len(self.symbol) > 1:
			for i in self.symbol:
				if len(self.d[f'{i}']['data']) == first_lens:
					continue
				else:
					print("Unequal lengths of dfs, all dfs need to have same length")


		self.d2 = {}
		for bar in range(SMA, first_lens):
			c2 = {}
			for symbol, inner_dict in self.d.items():
				date, Close = self.get_date_price(bar, symbol)
				#self.net_wealth_curve.append()
				#print(bar)
				#print(self.d['net_wealth'])
				c2[f'{symbol}'] = {'amount' : inner_dict['amount'], 
								#'net_wealth' : inner_dict['net_wealth'],
								'net_wealth' : Close * inner_dict['units'] + inner_dict['amount'],
								'position' : inner_dict['position'], 
								'units' : inner_dict['units'],
								'date' : inner_dict['data']['Dato'].iloc[bar]}
				
				if inner_dict['position'] == 0:
					if self.get_units(bar, sym) * inner_dict['data'].Close_.iloc[bar] < inner_dict['amount']:
						#print(inner_dict['amount'], symbol)
						#if inner_dict['amount'] > 0:

						if inner_dict['data'].Close_.iloc[bar] < inner_dict['data']['SMA'].iloc[bar]:
							#print(f'KJØP er i loop, dato er 		: 		{inner_dict['data'].Dato.iloc[bar]}		Close_	:		{inner_dict['data'].Close_.iloc[bar]}')
							self.place_buy_order(bar, units = None, amount = self.amount, sym = symbol)
							#print(f'Bought : {self.units}, amount : {self.amount}')
						
							#inner_dict['position'] = 1

				elif inner_dict['position'] == 1:


					if inner_dict['data'].Close_.iloc[bar] > inner_dict['data']['SMA'].iloc[bar]:
						#print(f'SALG er i loop, dato er 		: 		{inner_dict['data'].Dato.iloc[bar]}		Close_	:		{inner_dict['data'].Close_.iloc[bar]}')
						self.place_sell_order(bar, units = inner_dict['units'], sym = symbol)
						#print(f'Sold : {self.units}, amount : {self.amount}, net_wealth : {self.get_net_wealth_buy(bar)}\n')
						#print(f'\n')
						
						#inner_dict['position'] = 0
			self.d2[bar] = c2
			#print(self.d['DNB']['net_wealth'])
		#print(self.d.items())	
		#pp.pprint(self.d2)
		
		#pp.pprint(self.d2)

		#exit()
		total_net_wealth_development = []
		for i in self.d2.items():
			#print("i")
			#print(i[1])
			sum_netWealth_i = []
			for u in self.symbol:
				print(i[1][f'{u}']['net_wealth'])
				sum_netWealth_i.append(i[1][f'{u}']['net_wealth'])
			#print(sum_netWealth_i)
			total_net_wealth_development.append(sum(sum_netWealth_i))
			#akrbp.append(i[1]['DNB']['net_wealth'])
		print(total_net_wealth_development	)
		plt.plot(total_net_wealth_development	)
		plt.show()
		





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
    obj = portefoljø1(1, symbols, 100000, ftc = 0.0, vtc = 0.0, verbose = False)
    run_strategy()
