import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import detrend
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.holtwinters import SimpleExpSmoothing
from statsmodels.graphics.tsaplots import plot_pacf, plot_acf

# FUNCTIONS 
def downcast_columns(df):
    """Downcasts columns dtypes of a dataframe for memory optmization.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame to be optimized

    Returns
    -------
    pd.DataFrame
        Optimized dataframe with proper column types
    """    
    for column in df:
        if df[column].dtype == 'float64':
            df[column]=pd.to_numeric(df[column], downcast='float')
        if df[column].dtype == 'int64':
            df[column]=pd.to_numeric(df[column], downcast='integer')
    return df


def generate_train_test(df=None, station_name=None, test_date_start=None, detrendify=True):
    """Generates train and test sets for modelling

    Parameters
    ----------
    df : pd.DataFrame
        Dataframe with temporal data (must have DateTimeIndex)
    station_name : str
        Station name to be filtered
    test_date_start : str
        Time instant (datetime string) to be considered as split for testing
    detrendify : bool, optional
        Whether detrending is required, by default True

    Returns
    -------
    (np.array, np.array)
        Returns a tuple of sequences for train and test, respectively.
    """    
    station_df = df.iloc[df.index.get_level_values('station') == station_name]
    
    if detrendify:
        station_df['detrended'] = detrend(station_df.traffic)
        x_train = station_df.iloc[station_df.index.get_level_values('time') < test_date_start].reset_index().detrended.astype(float)
        x_test = station_df.iloc[station_df.index.get_level_values('time') > test_date_start].reset_index().detrended.astype(float)

    x_train = station_df.iloc[station_df.index.get_level_values('time') < test_date_start].reset_index().traffic.astype(float)
    x_test = station_df.iloc[station_df.index.get_level_values('time') > test_date_start].reset_index().traffic.astype(float)

    return x_train, x_test

def analyze_arima_params(x_train=None):
    """Performs parameter analysis for ARIMA models. It runs Adfuller's
       test and prints autocorrelation/partial autocorrelation plots.

    Parameters
    ----------
    x_train : np.array
        Input temporal data
    """        
    # parameter D
    test = adfuller(x_train)
    print('ADF Statistic: %f' % test[0])
    print('p-value: %f' % test[1])

    # parameter P
    plot_pacf(x_train.diff().dropna())
    plt.show()

    # parameter Q
    plot_acf(x_train.diff().dropna())
    plt.show()


def model_pipeline(model_name='ARIMA', p=[1,5], d=0, q=[7,11], x_train=None, x_test=None):
    """_summary_

    Parameters
    ----------
    model_name : str, optional
        model type to be generated, by default 'ARIMA'. Any different value will instantiate ExponentialSmoothing model.
    p : list, optional
        If ARIMA is selected, this represents values that should be tested for p, by default [1,5]
    d : int, optional
        If ARIMA is selected, this represents the value for d, by default 0
    q : list, optional
        If ARIMA is selected, this represents values that should be tested for q, by default [7,11]
    x_train : np.array
        input train data
    x_test : np.array
        input test data

    Returns
    -------
    (history, predictions)
        returns history (sequence of train points) and predictions (sequence of predicted points in test)
    """
    history = [x for x in x_train]
    predictions = []
    
    for t in range(len(x_test)):
        if model_name == 'ARIMA':
            model = ARIMA(history, order=(p, d, q))
        else:
            model = SimpleExpSmoothing(history)

        model_fit = model.fit()
        output = model_fit.forecast()
        yhat = output[0]
        predictions.append(yhat)
        obs = x_test[t]
        history.append(obs)
    
    return history, predictions

def MAPE(y_true, y_pred):
    """Computes Mean Absoulte Percentage Error for evaluation

    Parameters
    ----------
    y_true : np.array
        ground-truth values used for comparison
    y_pred : np.array
        predicted values generated by the model

    Returns
    -------
    float
        Evaluation percentage metric 
    """    
    y_true, y_pred = np.array(y_true), np.array(y_pred)
    return np.mean(np.abs((y_true - y_pred) / y_true)) * 100