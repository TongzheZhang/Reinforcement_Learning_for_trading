"""Utility functions"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def symbol_to_path(symbol, base_dir="data"):
    """Return CSV file path given ticker symbol."""
    return os.path.join(base_dir, "{}.csv".format(str(symbol)))


def get_data(symbols, dates):
    """Read stock data (adjusted close) for given symbols from CSV files."""
    df = pd.DataFrame(index=dates)
    if 'SPY' not in symbols:  # add SPY for reference, if absent
        symbols.insert(0, 'SPY')

    for symbol in symbols:
        df_temp = pd.read_csv(symbol_to_path(symbol),index_col='Date',
                parse_dates=True, usecols=['Date','Adj Close'], na_values=['nan'])
        df_temp = df_temp.rename(columns={'Adj Close':symbol})
        df = df.join(df_temp)
        if symbol =='SPY':
            df = df.dropna(subset=['SPY'])

    return df

def normalize_data(df):
    '''Normalize stock prices using the first rows of the dataframe'''
    return df/df.ix[0,:]


def plot_data(df, title="Stock prices", xlabel="Date", ylabel="Price"):
    """Plot stock prices with a custom title and meaningful axis labels."""
    ax = df.plot(title=title, fontsize=12)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    plt.show()
    #ax.set_xlabel("Date")
    #ax.set_ylabel("Price")
    #ax.legend(loc='upper left')


def plot_selected(df, columns, start_index, end_index):
    """Plot the desired columns over index values in the given range."""
    df = df.ix[start_index:end_index,columns]
    # Note: DO NOT modify anything else!
    plot_data(df)

def get_rolling_mean(values, window):
    """Return rolling mean of given values, using specified window size."""
    return pd.rolling_mean(values, window=window)

def get_rolling_std(values, window):
    """Return rolling standard deviation of given values, using specified window size."""
    return pd.rolling_std(values, window=window)


def get_bollinger_bands(rm, rstd):
    """Return upper and lower Bollinger Bands."""
    upper_band = rm + rstd*2
    lower_band = rm - rstd*2

    return upper_band, lower_band

def compute_daily_returns(df):
    """Compute and return the daily return values."""
    daily_returns = df.copy()
    #Compute daily returns for rows 1 onwars
    daily_returns[1:] = (df[1:]/df[:-1].values) -1 #.values to use numpy
    #daily_returns = (df /df.shift(1)) -1     #much easier with Pandas
    daily_returns.ix[0,:] = 0 #set daily_returnsfor row 0 to 0
    return daily_returns

def compute_cumulative_returns(df):
    """Compute and return the daily return values."""
    cumulative_returns = df.copy()
    #Compute cumulative_returns for rows 1 onwars
    #cumulative_returns = (df/df.ix[0,:].values) -1 #.values to use numpy
    cumulative_returns = (df/df.ix[0,:]) -1      #much easier with Pandas
    return cumulative_returns


def test_run():
    # Define a date range
    dates = pd.date_range('2010-01-01', '2010-12-31')

    # Choose stock symbols to read
    symbols = ['GOOG', 'IBM', 'GLD']

    # Get stock data
    df = get_data(symbols, dates)

    # Slice by row range (dates)
    #print (df.ix['2010-01-01':'2010-01-31'])

    #Slice by column (symbols)
    #print (df['GOOG'])
    #print (df[['IBM','GLD']])

    # Slice by row range (dates) & column
    #print (df.ix['2010-01-01':'2010-01-31',['IBM','GLD']])

    #Data plot
    #plot_data(df)
    #ax = df['SPY'].plot(title="SPY rolling mean",label='SPY')

    # Slice and plot
    #plot_selected(df, ['SPY', 'IBM'], '2010-03-01', '2010-04-01')

    #Compute mean
    #print (df.mean())
    #Compute rolling mean using a 20-days window
    rm_SPY = pd.rolling_mean(df['SPY'],window=20)

    #Compute rolling standard deviation
    rstd_SPY = get_rolling_std(df['SPY'], window=20)

    #Compute upper and lower bands
    upper_band, lower_band = get_bollinger_bands(rm_SPY, rstd_SPY)

    # Plot raw SPY values, rolling mean and Bollinger Bands
    ax = df['SPY'].plot(title="Bollinger Bands", label='SPY')
    rm_SPY.plot(label='Rolling mean', ax=ax)
    upper_band.plot(label='upper band', ax=ax)
    lower_band.plot(label='lower band', ax=ax)

    # Add axis labels and legend
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    ax.legend(loc='upper left')
    plt.show()

    # Compute daily returns
    daily_returns = compute_daily_returns(df)
    plot_data(daily_returns, title="Daily returns", ylabel="Daily returns")

    # Compute daily returns
    cumulative_returns = compute_cumulative_returns(df)
    plot_data(cumulative_returns, title="Cumulative Returns", ylabel="Cumulative Returns")

if __name__ == "__main__":
    test_run()
