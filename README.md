# Algorithmic-trading
A repository for my attempt at coding a working algorithmic trading framework, thats supposed to take an input of several stock tickers (could really be anything that is noted on an exchange, that has time series type data), these four stocks will be allocated 100 000 / # of stocks, so all stocks have
equal portions of the total sum put into the framework. Implementing this for a single stock is "easy" enough, but implementing several stocks at once, while ensuring that I dont use more cash than available to buy a stock, is a bit more of a serious task. 

The algorithm in "check_portfolio.py" works the following:
1. I first create a dictionary called d2, which will have a key being the current bar, and item being the inner_dict containing all info for each row, for each stock
2. I then loop through all bars, which in this case is SMA to the length of all dataframe rows. All dataframes selected, have the same # of rows.
3. For each bar, I create an inner dict
4. In this inner dict, I assign to it a key being the ticker of the stock of interest, and an item being another dict containing ; (amount (cash available), net_wealth (cash + (units * stock_price) at this bar), position (boolean value, 0 if not active, 1 if active), units (# of stocks owned at bar), date (date at this bar))
5. If I dont have any positions (position == 0) and I have a buying signal at this bar, I will run the buy function defined in the parent class Portefølje
6. If I already have positions, and I get a sell signal, I run the sell function defined in the parent class Portefølje

The code works, as far as im concerned, but the implementation seems tedious and more complicated than necessary. To sum up, my approach loops through all rows, and for each row, I record the date, amount to buy, my net wealth, the amount of units I have at this row and the boolean position, which is done for each stock.
The result is self.d2. If you prettyprint it, I cant find any rows, where the amount is negative.


Dont bother about the SQL part. I will supply a static database for running the code. My database at home updates itself everyday, inserting into the database the most recent data available from Euronext.com. I can supply the method of how I went through the Euronext wall if it is of interest).


The two files of interest are My_portfolio2.py and check_portfolio.py, dont mind the copy at the end of check_portfolio.py.

My_portfolio2.py initiates the parent class that defines all functions universal in all algorithmic trading strategies. This is for instance the buy and sell function. I will later implement a function, that will plot the equity curve of the total value of the portfolio.

check_portfolio.py is the first strategy I have defined, and it inherits the object "Portefølje", which I defined in My_portfolio. In this case, its a very simple moving average model for simplicitys sake, that takes the input of how many days behind to calculate the average price of. For now (To Mika and Christoffer), I just want to make the framework itself work. 
It is supposed to be really simple to implement new strategies, due to the universal "Portefølje" object I define in My_Portfolio2.py, but I think it is inefficient due to the amount of dictionaries I define. I have also looked into methods called threading, for running simulatenous processes in a script. I havent learned this yet.

The initial question I have, is if there is an easier way to do this.
