# -*- coding: utf-8 -*-

from Base import BaseStrat
import backtrader.indicators as btind

#This file will hold various strategies - these strategies may eventually 
#be broken up into a folder and each strategy a different file 
#the next method in the strategies is the actual strategy, so that is the single
#focus of these files 


#High and Low strategies should be first in here 

class BuyHighSellLow(BaseStrat):

    

    def __init__(self):
        super().__init__()
        self.highest = btind.Highest(self.datahigh, period=365)
        self.lowest = btind.Lowest(self.datalow, period=365)
        
    def next(self):
        
        if self.order:
            self.log(f'order in limbo is {self.order.status}')
            return
        
        #check if in market 
        if not self.position:
            #BUY if data 50 day high
            if self.datahigh[0] == self.highest[0]:
                self.log('BUY CREATE, %.2f' % self.dataclose[0])
                self.order = self.buy()
        
        else:
            #SELL if data is 50 day low
            if self.datalow[0] == self.lowest[0]:
                self.log('SELL CREATE, %.2f' % self.dataclose[0])

                # Keep track of the created order to avoid a 2nd order
                self.order = self.sell()
                

