"""
By Tongzhe Zhang
Template for implementing StrategyLearner  (c) 2016 Tucker Balch
"""

import datetime as dt
import QLearner as ql
import pandas as pd
import util as ut
import numpy as np


class StrategyLearner(object):

    # constructor
    def __init__(self, verbose = False):
        self.verbose = verbose
        self.bins = 10

    # this method should create a QLearner, and train it for trading
    def addEvidence(self, symbol = "IBM", \
        sd=dt.datetime(2008,1,1), \
        ed=dt.datetime(2009,1,1), \
        sv = 10000): 


        self.symbol = symbol
        self.sv = sv

        #print "in addEvidence"
        # initialize learner
        self.learner = ql.QLearner(num_states=3000,num_actions = 3, rar = 0.98, radr = 0.9999, dyna = 0, verbose=False)
        # add your code to do learning here
        

        # example usage of the old backward compatible util function
        syms=[symbol]
        dates = pd.date_range(sd, ed)
        prices_all = ut.get_data(syms, dates)  # automatically adds SPY
        prices = prices_all[syms]  # only portfolio symbols
        prices_SPY = prices_all['SPY']  # only SPY, for comparison later
        if self.verbose: print prices
        # example use with new colname 
        volume_all = ut.get_data(syms, dates, colname = "Volume")  # automatically adds SPY
        volume = volume_all[syms]  # only portfolio symbols
        volume_SPY = volume_all['SPY']  # only SPY, for comparison later
        if self.verbose: print volume

        '''start: get features '''
        #volatility
        train_daily_rets = (prices/prices.shift(1))-1
        train_volatility = pd.rolling_std(train_daily_rets,20)

        #momentum
        train_momentum = prices/prices.shift(20)-1.0
        
        #bb_value
        train_stdev = pd.rolling_std(prices,20)
        train_SMA = pd.rolling_mean(prices,20)
        train_bb_value = (prices-train_SMA)/(2*train_stdev)
        
        #fill three features with mean
        train_bb_value = train_bb_value.fillna(train_bb_value.mean())
        train_momentum = train_momentum.fillna(train_momentum.mean())
        train_volatility = train_volatility.fillna(train_volatility.mean())
        #print train_bb_value.head()

        '''end: get features '''


        ''' start:discretize'''

        thresholds = np.zeros((10,3))
        for i in range(1,self.bins):
            thresholds[i-1,0] = ((train_bb_value.max()-train_bb_value.min())*i)/self.bins+train_bb_value.min()
            thresholds[i-1,1] = ((train_momentum.max()-train_momentum.min())*i)/self.bins+train_momentum.min()
            thresholds[i-1,2] = ((train_volatility.max()-train_volatility.min())*i)/self.bins+train_volatility.min()
        thresholds[self.bins-1,0] = train_bb_value.max()
        thresholds[self.bins-1,1] = train_momentum.max()
        thresholds[self.bins-1,2] = train_volatility.max()

        train_bb_value_copy = train_bb_value.copy()
        train_momentum_copy = train_momentum.copy()
        train_volatility_copy = train_volatility.copy()
        
        #print thresholds
        train_momentum.ix[:,0] = 9
        train_bb_value.ix[:,0] = 9
        train_volatility.ix[:,0] = 9
        for i in range(0,prices.shape[0]):
            r = 0
            while r<=8:
                
                if train_bb_value_copy.ix[i,0] <= thresholds[r,0]: 
                    train_bb_value.ix[i,0] = r
                    break 
                r = r + 1


        for i in range(0,prices.shape[0]):
            r = 0
            while r<=8:
                
                if train_momentum_copy.ix[i,0] <= thresholds[r,1]: 
                    train_momentum.ix[i,0] = r
                    break
                r = r + 1


        for i in range(0,prices.shape[0]):
            r = 0
            while r<=8:
                
                if train_volatility_copy.ix[i,0] <= thresholds[r,2]: 
                    train_volatility.ix[i,0] = r
                    break
                r = r + 1


        train_data = pd.concat([train_bb_value,train_momentum,train_volatility,train_daily_rets],keys=['train_BB','train_Momentum','train_Volatility','train_Daily_rets'],axis = 1)
        train_dis_features = train_data['train_BB']*100+train_data['train_Momentum']*10+train_data['train_Volatility']
  
        ''' end:discretize'''

        '''strat:train learner'''
        #build what hold is 
        dates = pd.date_range(train_dis_features.index[0],train_dis_features.index[-1])
        columes = [self.symbol,'Price of stock','Cash','Port value']
        TrainHolding = pd.DataFrame(index = dates, columns = columes)

        TrainHolding.ix[:,'Price of stock'] = prices.ix[:,self.symbol]


        TrainHolding.ix[:,self.symbol] = 0
        TrainHolding.ix[:,'Cash'] = self.sv
        TrainHolding.ix[:,'Port value'] = self.sv
        TrainHolding  = TrainHolding.dropna()
        #TrainHoldingCopy = TrainHolding.copy()
        
        #transfer df to np
        TrainHolding =  TrainHolding.values
        train_dis_features = train_dis_features.values
     
        #train in Qlearner 1 means -100 share ,0 means 0 share , 2 means 100share;0 means do nothing 1 means selling , 2 means buying


        for i in range(0,1201):
            date = 0
            current_pos = 0
            state = train_dis_features[date,0] + current_pos *1000

            action = self.learner.querysetstate(state)


            for date in range(1,train_dis_features.size):

                ordercash = TrainHolding[date-1,2]
                ordershares = TrainHolding[date-1,0]
                ordervalue = TrainHolding[date-1,3]

                newprice = TrainHolding[date,1]
                newcash = 0
                newshares = 0

                newfeature = train_dis_features[date,0]

                if current_pos == 0 and action == 2:
                
                    current_pos = 2
                    newshares = TrainHolding[date,0] = 100
                    newcash = TrainHolding[date,2] = ordercash- newprice*100

                elif current_pos == 2 and action == 1:
             
                    current_pos = 0
                    newshares = TrainHolding[date,0] = 0
                    newcash = TrainHolding[date,2] = ordercash+newprice*100

                elif current_pos == 0 and action == 1:
                
                    current_pos = 1
                    newshares = TrainHolding[date,0] = -100
                    newcash = TrainHolding[date,2] = ordercash+newprice*100

                elif current_pos == 1 and action == 2:
          
                    current_pos = 0
                    newshares = TrainHolding[date,0] = 0
                    newcash = TrainHolding[date,2] = ordercash- newprice*100

                else:
               
                    current_pos = current_pos
                    newshares = TrainHolding[date,0] = ordershares
                    newcash = TrainHolding[date,2] = ordercash

                value = TrainHolding[date,3] = newcash + newshares * newprice               

                rwd = value/ordervalue-1

                state = newfeature + current_pos *1000

                action = self.learner.query(state, rwd)
		
            #if i ==1200:
                #print 'the last training: ',i,TrainHolding[date,3]


        '''end:train learner'''
        


        #print "out addEvidence"







    # this method should use the existing policy and test it against new data
    def testPolicy(self, symbol = "IBM", \
        sd=dt.datetime(2009,1,1), \
        ed=dt.datetime(2010,1,1), \
        sv = 10000):
        #print 'rar of learner :',self.learner.rar
        # here we build a fake set of trades
        # your code should return the same sort of data
        dates = pd.date_range(sd, ed)
        prices_all = ut.get_data([symbol], dates)  # automatically adds SPY
        prices = prices_all[[symbol]]  # only portfolio symbols
        #print prices
        #build trade
        trades =  prices.copy()
	trades.values[:,:] = 0 # set them all to nothing        

        trades_SPY = prices_all['SPY']  # only SPY, for comparison late

        '''start: testPolicy'''
        #volatility
        test_daily_rets = (prices/prices.shift(1))-1
        test_volatility = pd.rolling_std(test_daily_rets,20)

        #momentum
        test_momentum = prices/prices.shift(20)-1.0
        
        #bb_value
        test_stdev = pd.rolling_std(prices,20)
        test_SMA = pd.rolling_mean(prices,20)
        test_bb_value = (prices-test_SMA)/(2*test_stdev)
        
        #fill three features with mean
        test_bb_value = test_bb_value.fillna(test_bb_value.mean())
        test_momentum = test_momentum.fillna(test_momentum.mean())
        test_volatility = test_volatility.fillna(test_volatility.mean())
        #print test_bb_value.head()

        '''end: get features '''


        ''' start:discretize'''
        
        thresholds = np.zeros((10,3))
        for i in range(1,self.bins):
            thresholds[i-1,0] = ((test_bb_value.max()-test_bb_value.min())*i)/self.bins+test_bb_value.min()
            thresholds[i-1,1] = ((test_momentum.max()-test_momentum.min())*i)/self.bins+test_momentum.min()
            thresholds[i-1,2] = ((test_volatility.max()-test_volatility.min())*i)/self.bins+test_volatility.min()
        thresholds[self.bins-1,0] = test_bb_value.max()
        thresholds[self.bins-1,1] = test_momentum.max()
        thresholds[self.bins-1,2] = test_volatility.max()
        
        #print thresholds
        test_bb_value_copy = test_bb_value.copy()
        test_momentum_copy = test_momentum.copy()
        test_volatility_copy = test_volatility.copy()
        
        #print thresholds
        test_momentum.ix[:,0] = 9
        test_bb_value.ix[:,0] = 9
        test_volatility.ix[:,0] = 9
        for i in range(0,prices.shape[0]):
            r = 0
            while r<=8:
                
                if test_bb_value_copy.ix[i,0] <= thresholds[r,0]: 
                    test_bb_value.ix[i,0] = r
                    break 
                r = r + 1


        for i in range(0,prices.shape[0]):
            r = 0
            while r<=8:
                
                if test_momentum_copy.ix[i,0] <= thresholds[r,1]: 
                    test_momentum.ix[i,0] = r
                    break
                r = r + 1


        for i in range(0,prices.shape[0]):
            r = 0
            while r<=8:
                
                if test_volatility_copy.ix[i,0] <= thresholds[r,2]: 
                    test_volatility.ix[i,0] = r
                    break
                r = r + 1


        test_data = pd.concat([test_bb_value,test_momentum,test_volatility,test_daily_rets],keys=['test_BB','test_Momentum','test_Volatility','test_Daily_rets'],axis = 1)
        test_dis_features = test_data['test_BB']*100+test_data['test_Momentum']*10+test_data['test_Volatility']
 
        #print test_dis_features
        
        ''' end:discretize'''

        '''strat:test learner'''
        #build what hold is 
        dates = pd.date_range(test_dis_features.index[0],test_dis_features.index[-1])
        columes = [symbol,'Price of stock','Cash','Port value']
        TestHolding = pd.DataFrame(index = dates, columns = columes)

        TestHolding.ix[:,'Price of stock'] = prices.ix[:,self.symbol]


        TestHolding.ix[:,symbol] = 0
        TestHolding.ix[:,'Cash'] = sv
        TestHolding.ix[:,'Port value'] = sv
        TestHolding  = TestHolding.dropna()
        
        #print TestHolding
        
        #transfer pd to np
        TestHolding =  TestHolding.values
        test_dis_features = test_dis_features.values
     
        #test in Qlearner 1 means -100 share ,0 means 0 share , 2 means 100share;0 means do nothing 1 means selling , 2 means buying


        date = 0
        current_pos = 0
        state = test_dis_features[date,0] + current_pos *1000

        action = self.learner.querysetstate(state)


        for date in range(1,test_dis_features.size):
            #print action
            ordercash = TestHolding[date-1,2]
            ordershares = TestHolding[date-1,0]
            
            ordervalue = TestHolding[date-1,3]
            newprice = TestHolding[date,1]
            newcash = 0
            newshares = 0
            newfeature = test_dis_features[date,0]

            if current_pos == 0 and action == 2:
	        trades.values[date,:] = 100 # add a BUY at the dateth date               
                current_pos = 2
                newshares = TestHolding[date,0] = 100
                newcash = TestHolding[date,2] = ordercash- newprice*100

            elif current_pos == 2 and action == 1:
	        trades.values[date,:] = -100 # add a BUY at the dateth date             
                current_pos = 0
                newshares = TestHolding[date,0] = 0
                newcash = TestHolding[date,2] = ordercash+newprice*100

            elif current_pos == 0 and action == 1:
	        trades.values[date,:] = -100 # add a BUY at the dateth date                
                current_pos = 1
                newshares = TestHolding[date,0] = -100
                newcash = TestHolding[date,2] = ordercash+newprice*100

            elif current_pos == 1 and action == 2:
	        trades.values[date,:] = 100 # add a BUY at the dateth date         
                current_pos = 0
                newshares = TestHolding[date,0] = 0
                newcash = TestHolding[date,2] = ordercash- newprice*100

            else:
               
                current_pos = current_pos
                newshares = TestHolding[date,0] = ordershares
                newcash = TestHolding[date,2] = ordercash

	
            value = TestHolding[date,3] = newcash + newshares * newprice               
            rwd = value/ordervalue-1
            state = newfeature + current_pos *1000

            action = self.learner.query(state,rwd)

        #print TestHolding[0:20,:]
        #print TestHolding[-20:,:]	
   
        #print 'final value:', TestHolding[-1,3]
     
        #print trades
        '''end: testPolicy'''



        if self.verbose: print type(trades) # it better be a DataFrame!
        if self.verbose: print trades
        if self.verbose: print prices_all
        return trades



if __name__=="__main__":
    print "One does not simply think up a strategy"



