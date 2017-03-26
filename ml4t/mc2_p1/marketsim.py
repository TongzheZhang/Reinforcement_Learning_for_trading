"""MC2-P1: Market simulator."""
'''@ztz'''
import pandas as pd
import numpy as np
import datetime as dt
import os
from util import get_data, plot_data

def compute_portvals(orders_file = "./orders/orders.csv", start_val = 1000000):
    # this is the function the autograder will call to test your code
    
    #read my order book 
    orders = pd.read_csv(orders_file,parse_dates=True)
    #get all symbol
    Symbol = orders['Symbol'].values
    #get all order symbol
    all_symbols = []
    for symbol in Symbol:
        if symbol not in all_symbols:
            all_symbols.append(symbol)
    #get # of stocks type
    num = len(all_symbols)
    
    #get the start and end date
    start_date = orders.ix[0,'Date']
    end_date = orders.ix[orders.shape[0]-1,'Date']

    #get all price from panda 
    result = get_data(all_symbols,pd.date_range(start_date,end_date))
   
    #add some rows to result,such how many shares, and cash, and port_val
    for sym in all_symbols:
        result[sym+' Shares'] = pd.Series(0,index=result.index)
    result['cash'] = pd.Series(start_val,index=result.index)
    result['port_val'] = pd.Series(start_val,index=result.index)
 
    
    #calculate every order in everyday
    for day in range (0,result.shape[0]):

        #first assume that no order happen, shares and cash is same as before
        result.ix[day,num+1:2*num+3] = result.ix[day-1,num+1:2*num+3]
       
        #traversal orders
        for order in range(0,orders.shape[0]):
            
            if result.index[day].strftime('%Y-%m-%d') == orders.ix[order,'Date']:
            
                #if it is "buy"
                if orders.ix[order,'Order'] == 'BUY':
                    
                    # get some order information
                    tsym = orders.ix[order,'Symbol']
                    tshare = orders.ix[order,'Shares']
                    tprice = result.ix[day,tsym]

                    #update cash and shares
                    result.ix[day,'cash'] = result.ix[day,'cash'] - tshare*tprice
                    result.ix[day,tsym+' Shares'] = result.ix[day,tsym+' Shares'] + tshare

                    #calculate leverage
                    if result.ix[day,'cash'] < tshare*tprice:
                        
                        sumle = 0
                        sumsh = 0
                        for s in range(0,num):

                            sumle = sumle + result.ix[day,1+s]*abs(result.ix[day,num+1+s])
                            sumsh = sumsh + result.ix[day,1+s]*result.ix[day,num+1+s]

                        if sumle/(sumsh + result.ix[day,'cash'])>2.0:

                            result.ix[day,'cash'] = result.ix[day,'cash'] + tshare*tprice
                            result.ix[day,tsym+' Shares'] = result.ix[day,tsym+' Shares'] - tshare   



                if orders.ix[order,'Order'] == 'SELL':
                    # get some order information
                    tsym = orders.ix[order,'Symbol']
                    tshare = orders.ix[order,'Shares']
                    tprice = result.ix[day,tsym]
                    #update shares and cash
                    result.ix[day,'cash'] = result.ix[day,'cash'] + tshare*tprice
                    result.ix[day,tsym+' Shares'] = result.ix[day,tsym+' Shares'] - tshare
                    
                    ##calculate leverage
                    if result.ix[day-1,tsym+' Shares'] < tshare:

                        sumle = 0
                        sumsh = 0
                        for s in range(0,num):

                            sumle = sumle + result.ix[day,1+s]*abs(result.ix[day,num+1+s])
                            sumsh = sumsh + result.ix[day,1+s]*result.ix[day,num+1+s]

                        if sumle/(sumsh + result.ix[day,'cash'])>2.0:


                            result.ix[day,'cash'] = result.ix[day,'cash'] - tshare*tprice
                            result.ix[day,tsym+' Shares'] = result.ix[day,tsym+' Shares'] + tshare
                            
        #calculate the final value of thisday 
        sum1 = 0 #value of stocks
        for s in range(0,num):
            sum1 = sum1 + result.ix[day,1+s]*result.ix[day,num+1+s]
       
        result.ix[day,'port_val'] = sum1 +result.ix[day,'cash']
    

    portvals = result.ix[:,'port_val']
    portvals = portvals.to_frame()
    #print portvals.head()
    #print portvals.tail()
    

    # test the putput whether is DataFrame
    #print portvals.cc

    return portvals

def test_code():
    # this is a helper function you can use to test your code
    # note that during autograding his function will not be called.
    # Define input parameters

    of = "./orders/orders-leverage-3.csv"
    sv = 1000000

    # Process orders
    portvals = compute_portvals(orders_file = of, start_val = sv)
    if isinstance(portvals, pd.DataFrame):
        portvals = portvals[portvals.columns[0]] # just get the first column
    else:
        "warning, code did not return a DataFrame"

    # Get portfolio stats
    # Here we just fake the data. you should use your code from previous assignments.
    start_date = dt.datetime(2008,1,1)
    end_date = dt.datetime(2008,6,1)
    cum_ret, avg_daily_ret, std_daily_ret, sharpe_ratio = [0.2,0.01,0.02,1.5]
    cum_ret_SPY, avg_daily_ret_SPY, std_daily_ret_SPY, sharpe_ratio_SPY = [0.2,0.01,0.02,1.5]
    
    start_date = portvals.index[0].strftime('%Y-%m-%d')
    end_date = portvals.index[-1].strftime('%Y-%m-%d')
    
    daily_rets = (portvals/portvals.shift(1))-1
    adr = daily_rets.mean()
    sddr = daily_rets.std()
    sr = np.sqrt(252.0)*(adr/sddr)
    cr = portvals[-1]/portvals[0]-1
    cum_ret = cr
    avg_daily_ret = adr
    std_daily_ret = sddr
    sharpe_ratio = sr
    spydata = get_data(['$SPX'],pd.date_range(start_date,end_date))
    #print '1'
    #print spydata.head()
    spydata = spydata.ix[:,'$SPX']
    #print 
    #print ' spydata'
    #print spydata.head()
    daily_rets_spy = (spydata/spydata.shift(1))-1
    cum_ret_SPY = spydata[-1]/spydata[0]-1
    avg_daily_ret_SPY = daily_rets_spy.mean()
    std_daily_ret_SPY = daily_rets_spy.std()
    sharpe_ratio_SPY = np.sqrt(252.0)*(avg_daily_ret_SPY/std_daily_ret_SPY)

 
    # Compare portfolio against $SPX
    print 'how many days? :', portvals.shape[0]
    #print "Date Range: {} to {}".format(start_date, end_date)
    #print
    print "Sharpe Ratio of Fund: {}".format(sharpe_ratio)
    #print "Sharpe Ratio of SPY : {}".format(sharpe_ratio_SPY)
    #print
    #print "Cumulative Return of Fund: {}".format(cum_ret)
    #print "Cumulative Return of SPY : {}".format(cum_ret_SPY)
    #print
    #print "Standard Deviation of Fund: {}".format(std_daily_ret)
    #print "Standard Deviation of SPY : {}".format(std_daily_ret_SPY)
    #print
    print "Average Daily Return of Fund: {}".format(avg_daily_ret)
    #print "Average Daily Return of SPY : {}".format(avg_daily_ret_SPY)
    #print
    print "Final Portfolio Value: {}".format(portvals[-1])
    
if __name__ == "__main__":
    test_code()
