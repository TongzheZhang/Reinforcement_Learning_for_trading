"""MC4-P1."""
'''@ztz'''
import pandas as pd
import numpy as np
import datetime as dt
import math
import os
import KNNLearner as knn
import csv
import marketsim as sim
from util import get_data, plot_data
import matplotlib.pyplot as plt

#data of train 
def get_trainX(i = 1):
    print "from TrainX"
    
    #get train data features
    start_date = dt.datetime(2007,12,31)
    end_date = dt.datetime(2009,12,31)
    dfc = get_data(['ML4T-240'],pd.date_range(start_date,end_date))
    priceC = dfc['ML4T-240']
    
    #volatility
    train_daily_rets = (priceC/priceC.shift(1))-1
    train_volatility = pd.rolling_std(train_daily_rets,20)
    #momentum
    train_momentum = priceC/priceC.shift(19)-1.0
    #bb_value
    train_stdev = pd.rolling_std(priceC,20)
    train_SMA = pd.rolling_mean(priceC,20)
    train_bb_value = (train_stdev-train_SMA)/(2*train_stdev)
    
    train_dataX = pd.concat([train_bb_value,train_momentum,train_volatility],keys=['train_BB','train_Momentum','train_Volatility'],axis = 1)
    
    #normalize
    train_dataX['train_BB'] = (train_dataX['train_BB']-train_dataX['train_BB'].mean())/train_dataX['train_BB'].std()
    train_dataX['train_Momentum'] = (train_dataX['train_Momentum']-train_dataX['train_Momentum'].mean())/train_dataX['train_Momentum'].std()
    train_dataX['train_Volatility'] = (train_dataX['train_Volatility']-train_dataX['train_Volatility'].mean())/train_dataX['train_Volatility'].std()
    
    return train_dataX.dropna()

def get_trainY():
    print "from TrainY"
    start_date = dt.datetime(2007,12,31)
    end_date = dt.datetime(2009,12,31)
    dfc = get_data(['ML4T-240'],pd.date_range(start_date,end_date))
    priceC = dfc['ML4T-240']
   
    train_dataY = priceC.shift(-5)/priceC-1.0
    return train_dataY.dropna()

# data of test
def get_testX(i = 1):
    print "from TestX"
    
    #get test data features
    test_start_date = dt.datetime(2009,12,31)
    test_end_date = dt.datetime(2011,12,31)
    dfTest = get_data(['ML4T-240'],pd.date_range(test_start_date,test_end_date))
    test_price = dfTest['ML4T-240']
    
    #volatility
    test_daily_rets = (test_price/test_price.shift(1))-1
    test_volatility = pd.rolling_std(test_daily_rets,20)
    #momentum
    test_momentum = test_price/test_price.shift(19)-1.0
    #bb_value
    test_stdev = pd.rolling_std(test_price,20)
    test_SMA = pd.rolling_mean(test_price,20)
    test_bb_value = (test_stdev-test_SMA)/(2*test_stdev)
    
    test_dataX = pd.concat([test_bb_value,test_momentum,test_volatility],keys=['test_BB','test_Momentum','test_Volatility'],axis = 1)
    
    #normalize
    test_dataX['test_BB'] = (test_dataX['test_BB']-test_dataX['test_BB'].mean())/test_dataX['test_BB'].std()
    test_dataX['test_Momentum'] = (test_dataX['test_Momentum']-test_dataX['test_Momentum'].mean())/test_dataX['test_Momentum'].std()
    test_dataX['test_Volatility'] = (test_dataX['test_Volatility']-test_dataX['test_Volatility'].mean())/test_dataX['test_Volatility'].std()
    
    return test_dataX.dropna()


def get_testY():
    print "from TestY"
    test_start_date = dt.datetime(2009,12,31)
    test_end_date = dt.datetime(2011,12,31)
    dfTest = get_data(['ML4T-240'],pd.date_range(test_start_date,test_end_date))
    test_price = dfTest['ML4T-240']
   
    test_dataY = test_price.shift(-5)/test_price-1.0
    return test_dataY.dropna()
    

'''create order'''
def newOrder(predY):
    print "from newOrder"
    #print predY

    file = open("orders.csv","wb")
    writefile = csv.writer(file)
    writefile.writerow(('Date','Symbol','Order','Shares'))
    shares = 0
    price = get_data(['ML4T-240'],pd.date_range(predY.index[0],predY.index[-1]))
    price = price['ML4T-240']
    #print predY
    i = 0
    while i < predY.shape[0]:
        #print i

        if predY.ix[i][0] > 0.005 and shares == 0:
            writefile.writerow((predY.index[i],'ML4T-240','BUY','100'))
            shares = shares + 100
            i = i + 1
        elif predY.ix[i][0] > 0 and shares == -100:
            writefile.writerow((predY.index[i],'ML4T-240','BUY','0'))
            shares = shares + 100
            i = i + 1
        elif predY.ix[i][0] < 0 and shares == 100:
            writefile.writerow((predY.index[i],'ML4T-240','SELL','0'))
            shares = shares - 100
            i = i + 1
        elif predY.ix[i][0] < -0.005 and shares == 0:
            writefile.writerow((predY.index[i],'ML4T-240','SELL','-100'))
            shares = shares - 100
            i = i + 1
        else:i = i + 1
    print shares
 
'''create order''' 


 
if __name__=="__main__":
    print "test whether the code"
    #position 5
    start_date = dt.datetime(2009,12,31)
    end_date = dt.datetime(2011,12,31)
    dfc = get_data(['ML4T-240'],pd.date_range(start_date,end_date))
    priceC = dfc['ML4T-240']

    priceC = priceC.to_frame()

    price_mean = priceC.mean().values
    price_std = priceC.std().values
    temp_train = priceC.rename(columns={'ML4T-240':'price_of_stock'})
    temp_train = (priceC.rename(columns={'ML4T-240':'price_of_stock_norm'})-price_mean)/ price_std
    #position 4
    temp_test = priceC.rename(columns={'ML4T-240':'price_of_stock'})
    #temp_test = (priceC.rename(columns={'ML4T-240':'price_of_stock_norm'})-price_mean)/ price_std

    train_dataX = get_trainX()[:-5]
    train_dataY = get_trainY()[20:]
    test_dataX = get_testX()[:-5]
    test_dataY = get_testY()[20:]

    #create learner
    learner = knn.KNNLearner(k = 3, verbose = False)
    learner.addEvidence(train_dataX,train_dataY)


    '''train data'''
    #get df predY_train
    predY_train = learner.query(train_dataX.values)
    predY_train_df = train_dataY.copy(deep=True)
    
    predY_train_df[:] = predY_train

    predY_train_df = predY_train_df.to_frame()
    predY_train_df = predY_train_df.rename(columns={'ML4T-240':'PredY_train'})
    
    #get df Y_train
    train_dataY_df = pd.DataFrame(train_dataY)
    train_dataY_df = train_dataY_df.rename(columns={'ML4T-240':'Y_train'})
    
    #combine them
    temp_train = temp_train.join(predY_train_df*5)

    temp_train = temp_train.join(train_dataY_df*5)  
    '''train data'''

    '''test data'''
    #get df predY_test
    predY_test = learner.query(test_dataX.values)
    predY_test_df = test_dataY.copy(deep=True)
    predY_test_df[:] = predY_test
    predY_test_df = predY_test_df.to_frame()

    predY_test_df = predY_test_df.rename(columns={'ML4T-240':'PredY_test'})
    #get df Y_test
    test_dataY_df = pd.DataFrame(test_dataY)
    test_dataY_df = test_dataY_df.rename(columns={'ML4T-240':'Y_test'})
    #combine them position6
    #temp_test = temp_test.join(predY_test_df*5)

    #temp_test = temp_test.join(test_dataY_df*5) 
    '''test data'''

    #create new order 
    newOrder(predY_test_df)

    #plot position1
    #ax = temp_test.plot(title="test data of ML4T-240(Price,enter,exit)", fontsize=12)
    #ax.set_xlabel("Date")
    #ax.set_ylabel("price")
    
    #position3
    myport = sim.compute_portvals(symbol = 'ML4T-240',start_date = dt.datetime(2009,12,31),end_date = dt.datetime(2011,12,31),plotif = False)
    #plt.show()
    
    spydata = get_data(["$SPX"], pd.date_range(start_date,end_date))
    spydata = spydata.ix[:,'$SPX']
    daily_rets_ref = spydata/spydata.ix[0]
    daily_rets_my = myport/myport.ix[0]
    
    daily_rets_ref = daily_rets_ref.to_frame()
    
    temp_bench = daily_rets_ref.join(daily_rets_my)
    temp_bench = temp_bench.rename(columns={'ML4T-240':'My_value_ML4T-240'})
    #print temp_bench
    #position 2
    plot_data(temp_bench, title="test_ML4T-240_backtest_norm", xlabel="Date", ylabel="",shou=True)

