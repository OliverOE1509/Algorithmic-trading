# Algorithmic-trading
Note:
lokalKurser.db.zip needs to be extracted because it was too large. Download the two github.py files, and the extracted db file to a directory. When you then run run_algorithm_Github.py, and you get an equity curve showing in matplotlib, then the code has been run successfully.

A repository for my attempt at coding a working algorithmic trading framework, thats supposed to take an input of several stock tickers (could really be anything that is noted on an exchange, that has time series type data), these four stocks will be allocated (100 000 / # of stocks). For example, if I have 4 stocks trading, then all 4 stocks will be allocated 25000, so all stocks have equal portions of the total sum put into the framework. Implementing this for a single stock is 
simple enough, but implementing several stocks at once, while ensuring that I dont use more cash than available to buy a stock, is a bit more of a serious task...

The algorithm in "check_portfolio.py" works the following:
1. I first create a dictionary called d2, which will have a key being the current bar (bar = date), and item being the inner_dict containing all info for each row.
2. I then loop through all bars, which in this case is SMA to the length of all dataframe rows. All dataframes selected, have the same # of rows.
3. For each bar, I create an inner dict
4. In this inner dict, I assign to it a key being the ticker of the stock of interest, and an item being another dict containing ;
   (amount (cash available),
   net_wealth (cash + (units * stock_price) at this bar),
   position (boolean value, 0 if not active, 1 if active),
   units (# of stocks owned at bar), date (date at this bar))
7. If I dont have any positions (position == 0) and I have a buying signal at this bar, I will run the buy function defined in the parent class Portefølje, called "place_buy_order"
8. If I already have positions, and I get a sell signal, I run the sell function defined in the parent class Portefølje, called "place_sell_order"

The code works, as far as im concerned, but the implementation seems tedious and more complicated than necessary. To sum up, my approach loops through all rows, and for each row, I record the date, amount to buy, my net wealth, the amount of units I have at this row and the boolean position, which is done for each stock.
The result is self.d2. If you prettyprint it, I cant find any rows, where the amount is negative.


Dont bother about the SQL part. I will supply a static database for running the code. My database at home updates itself everyday, inserting into the database the most recent data available from Euronext.com. I can supply the method of how I went through the Euronext wall if it is of interest.


The two files of interest are My_portfolio2.py and check_portfolio.py, dont mind the copy at the end of check_portfolio.py.

My_portfolio2.py initiates the parent class that defines all functions universal in all algorithmic trading strategies. This is for instance the buy and sell function. 

The data is also gathered in the parent class. The format_connection() function, is what selects all data relevant from the database. Now look at self.d, which is a nested dictionary, where the outer key and value, is the ticker of the stock, and the value is the dataframe selected from the database. This is the most efficient and best way to store the data for each stock.


check_portfolio.py is the first strategy I have defined, and it inherits the object "Portefølje", which I defined in My_portfolio. In this case, its a very simple moving average model for simplicitys sake, that takes the input of how many days behind to calculate the average price of. For now (To Mika, Christoffer and Yulin), I just want to make the framework itself work. 
It is supposed to be really simple to implement new strategies, due to the universal "Portefølje" object I define in My_Portfolio2.py, but I think it is inefficient due to the amount of dictionaries I define. I have also looked into methods called threading, for running simulatenous processes in a script. I havent learned this yet.

My question is if there is a simpler way to create this framework. A good system should have a universal method of creating new strategies, and this has been my goal from the start.
Additionally, when I allocate equal portions to each stock I am trading, it becomes a problem when I am trading 100 stocks, as all stocks will have 1000kr (assuming I have 100 000kr initial value) to trade with. This becomes a problem, because if I have 1000 kr to trade Nvidia for instance, I am very limited because the stock price itself is higher than 1000kr xD (at least at this point of time when writing 12.06.2024).
