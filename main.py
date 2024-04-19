# -*- coding: utf-8 -*-

#in the current iteration of this folder, this file does practically nothing.
#all it does is run one of the strategies. Please see CompareStrategies.ipynb

import backtrader as bt
import backtrader.indicators as btind
import backtrader.feeds as btfeeds
from Strategies.BuyHighSellLow import BuyHighSellLow
from Base import run


if __name__ == '__main__':
    starting_cash = 10000.00

    # Datas are in a subfolder of the samples. Need to find where the script is
    # because it could have been called from anywhere
    datapath = 'SPY_max.csv'

    # Create a Data Feed
    #there are a few different types of data feeds you can create. The simplest
    #was to download from YahooFinance and use the built in 
    data = bt.feeds.YahooFinanceCSVData(
        dataname=datapath)
    

    buy_high = run(strategy=BuyHighSellLow, datafeed=data, starting_cash=starting_cash)
    final_value_bh = buy_high.broker.getvalue()
    return_perc_bh = ((final_value_bh - starting_cash) / starting_cash) * 100
    #print(buy_high.broker.trades)
    
    print(f'Final Portfolio Value Buy High: {final_value_bh}')  
    print(f'% return BuyHigh: {return_perc_bh}')
    buy_high.plot()


