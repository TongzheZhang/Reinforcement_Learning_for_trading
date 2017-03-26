"""MC1-P1: Analyze a portfolio."""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt
from util import get_data, plot_data

# This is the function that will be tested by the autograder
# The student must update this code to properly implement the functionality
def assess_portfolio(sd = dt.datetime(2008,1,1), ed = dt.datetime(2009,1,1), \
    syms = ['GOOG','AAPL','GLD','XOM'], \
    allocs=[0.1,0.2,0.3,0.4], \
    sv=1000000, rfr=0.0, sf=252.0, \
    gen_plot=False):

    # Read in adjusted closing prices for given symbols, date range
    dates = pd.date_range(sd, ed)
    prices_all = get_data(syms, dates)  # automatically adds SPY
    prices = prices_all[syms]  # only portfolio symbols   
    prices_SPY = prices_all['SPY']  # only SPY, for comparison later
    
    # my code
    # Get daily portfolio value  
    # add code here to compute daily portfolio values
    normalized_prices_SPY =  prices_SPY/prices_SPY[0] 
    normalized_prices_port = prices / prices.ix[0, :]
    
    normalized_port = normalized_prices_port*allocs
    normalized_port_total = normalized_port.sum(axis = 1)
    
    port_val = normalized_port_total
    prices_SPY = normalized_prices_SPY
    
    
    # Get portfolio statistics (note: std_daily_ret = volatility)
    cr, adr, sddr, sr = [0.25, 0.001, 0.0005, 2.1] # add code here to compute stats
    #Cumulative return,right
    cr = normalized_port_total[-1]/normalized_port_total[0]-1
    #daily_rets
    daily_rets =(normalized_port_total/normalized_port_total.shift(1))-1
    #daily_rets.ix[0] = 0
    #Average daily return
    adr = daily_rets.mean()
    
    #sddr:Standard deviation of daily return
    sddr = daily_rets.std()
    #sr = Sharpe Ratio
    sr = np.sqrt(sf) * (adr/sddr)
    
    #normalized_prices_SPY.join(normalized_port_total)
    '''test print '''

    #print normalized_prices_SPY.head()
    #print normalized_port_total.head()
 
    # Compare daily portfolio value with SPY using a normalized plot
    if gen_plot:
        # add code to plot here

        df_temp = pd.concat([port_val, prices_SPY], keys=['Portfolio', 'SPY'], axis=1)
        plot_data(df_temp,ylabel="normalized_price")
        
        pass

    # Add code here to properly compute end value
    ev = 1000000*normalized_port_total[-1]
    
    
    
    return cr, adr, sddr, sr, ev

def test_code():
    # This code WILL NOT be tested by the auto grader
    # It is only here to help you set up and test your code

    # Define input parameters
    # Note that ALL of these values will be set to different values by
    # the autograder!
   
    start_date = dt.datetime(2009,1,1)
    end_date = dt.datetime(2009,12,31)
    symbols = ['GOOG', 'AAPL', 'GLD', 'MSFT']
    allocations = [0.3, 0.3, 0.1, 0.3]
    start_val = 1000000  
    risk_free_rate = 0.0
    sample_freq = 252

    # Assess the portfolio
    cr, adr, sddr, sr, ev = assess_portfolio(sd = start_date, ed = end_date,\
        syms = symbols, \
        allocs = allocations,\
        sv = start_val, \
        gen_plot = True)

        
    # Print statistics
    print "Start Date:", start_date
    print "End Date:", end_date
    print "Symbols:", symbols
    print "Allocations:", allocations
    print "Sharpe Ratio:", sr
    print "Volatility (stdev of daily returns):", sddr
    print "Average Daily Return:", adr
    print "Cumulative Return:", cr
    #print end value
    #print "end value:",ev

if __name__ == "__main__":
    test_code()
