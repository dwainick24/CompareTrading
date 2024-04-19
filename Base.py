# -*- coding: utf-8 -*-

import backtrader as bt
import backtrader.indicators as btind
import backtrader.feeds as btfeeds

#this file will be used to hold the Base strategy functions that will hold things 
#like the logging fuction and the notify functions 


class BaseStrat(bt.Strategy):
    #this strategy is a base of all the other strategies. It will hold things 
    #like a logging function that will remain consistent 

        
    def __init__(self):
        # Keep a reference to the lines in the data[0] dataseries
        self.dataclose = self.datas[0].close
        self.datalow = self.datas[0].low
        self.datahigh = self.datas[0].high
        

        # To keep track of pending orders and buy price/commission
        self.order = None
        self.buyprice = None
        self.buycomm = None
        
    def log(self, txt, dt=None):
        #This is the logging function. This function should simply add the trade to a list of trades that have been made
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))
        
    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    'BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                    (order.executed.price,
                     order.executed.value,
                     order.executed.comm))

                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            else:  # Sell
                self.log('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                         (order.executed.price,
                          order.executed.value,
                          order.executed.comm))

            self.bar_executed = len(self)
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        self.order = None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' %
                 (trade.pnl, trade.pnlcomm))
        
        
    def stop(self):
        self.log('Ending Value %.2f' %
                 (self.broker.getvalue()))
        self.log(self.position)
        

def run(strategy, datafeed, starting_cash):
    #this function will run a strategy 
    cerebro = bt.Cerebro(stdstats=False)
    cerebro.addstrategy(strategy)
    cerebro.adddata(datafeed)
    cerebro.broker.setcash(starting_cash)
    cerebro.addsizer(bt.sizers.AllInSizer)
    cerebro.addobserver(bt.observers.BuySell)
    cerebro.run()
    #final_value = cerebro.broker.getvalue()
    #return_perc = ((final_value - starting_cash) / starting_cash) * 100
    return cerebro

