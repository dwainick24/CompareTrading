# -*- coding: utf-8 -*-
from Base import BaseStrat

class BuyAndHold(BaseStrat):
    
        
    def next(self):
        if not self.position:
            self.log('BUY CREATE')
            self.order = self.buy()
        
