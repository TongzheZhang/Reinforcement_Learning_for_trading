'Plot a histogram'

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from get_data import get_data, plot_data

def compute_daily_returns(df):

    daily_returns = df.copy()
    daily_returns[1:] = (daily_returns[1:]/daily_returns[:-1].values) -1
    daily_returns.ix[0, :] = 0
    return daily_returns

def test_run():
    dates = pd.date_range('2009-01-01','2012-12-31')
    symbols =['SPY','XOM','GLD']
    df = get_data(symbols,dates)
    #plot_data(df)

    daily_returns = compute_daily_returns(df)
    #plot_data(daily_returns, title ='Daily Return', ylabel = 'Daily Return')

    #histogram
    #daily_returns['SPY'].hist(bins=20,label ='SPY')
    #daily_returns['XOM'].hist(bins=20,label ='XOM')
    #plt.legend(loc='upper left')
    #plt.show()

    #mean_SPY = daily_returns['SPY'].mean()
    #print ('mean_SPY = ',mean_SPY)
    #std_SPY = daily_returns['SPY'].std()
    #print ('std_SPY = ',std_SPY)

    #plt.axvline(mean_SPY,color ='w',linestyle = 'dashed', linewidth = 2)
    #plt.axvline(std_SPY,color ='r',linestyle = 'dashed', linewidth = 2)
    #plt.axvline(-std_SPY,color ='r',linestyle = 'dashed', linewidth = 2)
    #plt.show()

    #print (daily_returns.kurtosis())

    #Scaller plot
    daily_returns.plot(kind ='scatter',x = 'SPY',y='XOM')
    beta_XOM,alpha_XOM = np.polyfit(daily_returns['SPY'],daily_returns['XOM'],1)
    plt.plot(daily_returns['SPY'],beta_XOM*daily_returns['SPY']+alpha_XOM,'-',color ='r')

    daily_returns.plot(kind ='scatter',x = 'SPY',y='GLD')
    beta_GLD,alpha_GLD = np.polyfit(daily_returns['SPY'],daily_returns['GLD'],1)
    plt.plot(daily_returns['SPY'],beta_GLD*daily_returns['SPY']+alpha_GLD,'-',color ='r')
    plt.show()

    print('beta_XOM =' ,beta_XOM)
    print('alpha_XOM =', alpha_XOM)
    print('beta_GLD =' ,beta_GLD) #comment tu te comport par rapport aux marché
    print('alpha_GLD =' ,alpha_GLD) # comment tu te comporte par rapport à SPY

    print(daily_returns.corr(method ='pearson'))


if __name__ == '__main__':
    test_run()
