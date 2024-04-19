# -*- coding: utf-8 -*-
from Base import BaseStrat
import backtrader.indicators as btind


class BuyLowSellHigh(BaseStrat):
    
    def __init__(self):
        super().__init__()
        self.highest = btind.Highest(self.datahigh, period=365)
        self.lowest = btind.Lowest(self.datalow, period=365)
        
    def next(self):

        
        if self.order:
            #self.log('if self order statement went off')
            self.log(f'order in limbo is {self.order.status}')
            return
        
        #check if in market 
        if not self.position:
            #BUY if data high is the 50 day high
            if self.datalow[0] == self.lowest[0]:
                self.log('BUY CREATE, %.2f' % self.dataclose[0])
                self.order = self.buy()
        
        else:
            #SELL if data is the 50 days low 
            if self.datahigh[0] == self.highest[0]:
                self.log('SELL CREATE, %.2f' % self.dataclose[0])

                # Keep track of the created order to avoid a 2nd order
                self.order = self.sell()
        
                

