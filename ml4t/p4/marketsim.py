"""MC2-P1: Market simulator."""
'''@ztz'''
import pandas as pd
import numpy as np
import datetime as dt
import os
from util import get_data, plot_data
import datetime as dt
import matplotlib.pyplot as plt


def compute_portvals(orders_file = "orders.csv", symbol ='ML4T-240', start_val = 10000,start_date = dt.datetime(2007,12,31),end_date = dt.datetime(2009,12,31),plotif = False):
    # this is the function the autograder will call to test your code
    df = get_data([symbol],pd.date_range(start_date,end_date))
    price = df[symbol]
    #print price
    #read my order book 
    orders = pd.read_csv(orders_file,parse_dates=True)
    #print orders
    cash = start_val
    shares = 0

    portvals = pd.DataFrame(price)

    #calculate every order in everyday
    for day in range (0,price.shape[0]):
        
        for order in range(0,orders.shape[0]):
       
            if price.index[day].strftime('%Y-%m-%d %H:%M:%S') == orders.ix[order,'Date']:
                
                #if it is "BUY"
                if orders.ix[order,'Order'] == 'BUY':

                    shares = shares + 100
                    cash = cash - price.ix[day,0]*100
                    if plotif == True:
                        if shares == 0:
                            plt.axvline(orders.ix[order,'Date'],color='black')
                        if shares == 100:
                            plt.axvline(orders.ix[order,'Date'],color='green')
                #if it is "SELL"
                if orders.ix[order,'Order'] == 'SELL':

                    shares = shares - 100
                    cash = cash + price.ix[day,0]*100
                    if plotif == True:
                        if shares == 0:
                            plt.axvline(orders.ix[order,'Date'],color='black')
                        if shares == -100:
                            plt.axvline(orders.ix[order,'Date'],color='red')
                
        portvals.ix[day,0] = cash + shares*price.ix[day,0]
       
    print 'Final values',': ', portvals.ix[-1,0]               

    return portvals


    
if __name__ == "__main__":
    test_code()
