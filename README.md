# Algorithmic-trading
A repository for my attempt at coding a working algorithmic trading framework, thats supposed to take an input of several stock tickers (could really be anything that is noted on an exchange, that has time series type data), these four stocks will be allocated 100 000 / # of stocks, so all stocks have equal portions of the total sum put into the framework.

The two files of interest are My_portfolio2.py and check_portfolio.py, dont mind the copy.

My_portfolio2.py contains the definition of the parent class that defines all functions universal in all algorithmic trading strategies. This is for instance the buy and sell function. I will later implement a function, that will plot the equity curve of the total value of the portfolio.

check_portfolio.py is the first strategy I have defined, and it inherits the object "Portefølje", which I defined in My_portfolio.
