import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt

us_loc = pd.read_csv("../input/us-counties-covid-19-dataset/us-counties.csv", parse_dates=['date'],
                                index_col=['date'])
us_loc.tail()

# New York City
new_york = us_loc[us_loc["county"] == "New York City"]
new_york.head()

# Creating the "new_cases" column
new_york["new_cases"] = new_york['cases'] - new_york['cases'].shift(1)
new_york["new_cases"] = new_york["new_cases"].replace('NaN', 0)
new_york.head()

# imports from:
# Di Pietro, M (2020) Python source code (Version 3.0) [Source code]. 
# https://github.com/mdipietro09/DataScience_ArtificialIntelligence_Utils/tree/a7f3991814dd6b2ac3f3f73892b5dcaf9122d296/time_series
from scipy import optimize

def fit_curve(X, y, f=None, kind=None, p0=None):
    ## define f(x) if not specified
    if f is None:
        if kind == "logistic":
            f = lambda p,X: p[0] / (1 + np.exp(-p[1]*(X-p[2])))
        elif find == "gaussian":
            f = lambda p,X: p[0] * np.exp(-0.5 * ((X-p[1])/p[2])**2)
    
    ## find optimal parameters
    model, cov = optimize.curve_fit(f, X, y, maxfev=10000, p0=p0)
    return model
    
def utils_predict_curve(model, f, X):
    fitted = f(X, model[0], model[1], model[2])
    return fitted

def utils_generate_indexdate(start, end=None, n=None, freq="D"):
    if end is not None:
        index = pd.date_range(start=start, end=end, freq=freq)
    else:
        index = pd.date_range(start=start, periods=n, freq=freq)
    index = index[1:]
    print("--- generating index date --> start:", index[0], "| end:", index[-1], "| len:", len(index), "---")
    return index

def utils_plot_parametric(new_york, zoom=30, figsize=(15,5)):
    ## interval
    new_york["residuals"] = new_york["ts"] - new_york["model"]
    new_york["conf_int_low"] = new_york["forecast"] - 1.96*new_york["residuals"].std()
    new_york["conf_int_up"] = new_york["forecast"] + 1.96*new_york["residuals"].std()
    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=figsize)
    
    ## entire series
    new_york["ts"].plot(marker=".", linestyle='None', ax=ax[0], title="Parametric Fitting", color="black")
    new_york["model"].plot(ax=ax[0], color="green", label="model", legend=True)
    new_york["forecast"].plot(ax=ax[0], grid=True, color="red", label="forecast", legend=True)
    ax[0].fill_between(x=new_york.index, y1=new_york['conf_int_low'], y2=new_york['conf_int_up'], color='b', alpha=0.3)
   
    ## focus on last
    first_idx = new_york[pd.notnull(new_york["forecast"])].index[0]
    first_loc = new_york.index.tolist().index(first_idx)
    zoom_idx = new_york.index[first_loc-zoom]
    new_york.loc[zoom_idx:]["ts"].plot(marker=".", linestyle='None', ax=ax[1], color="black", 
                                  title="Zoom on the last "+str(zoom)+" observations")
    new_york.loc[zoom_idx:]["model"].plot(ax=ax[1], color="green")
    new_york.loc[zoom_idx:]["forecast"].plot(ax=ax[1], grid=True, color="red")
    ax[1].fill_between(x=new_york.loc[zoom_idx:].index, y1=new_york.loc[zoom_idx:]['conf_int_low'], 
                       y2=new_york.loc[zoom_idx:]['conf_int_up'], color='b', alpha=0.3)
    plt.show()
    return new_york[["ts","model","residuals","conf_int_low","forecast","conf_int_up"]]

def forecast_curve(ts, f, model, pred_ahead=None, end=None, freq="D", zoom=30, figsize=(15,5)):
    ## fit
    fitted = utils_predict_curve(model, f, X=np.arange(len(ts)))
    new_york = ts.to_frame(name="ts")
    new_york["model"] = fitted
    
    ## index
    index = utils_generate_indexdate(start=ts.index[-1], end=end, n=pred_ahead, freq=freq)
    
    ## forecast
    preds = utils_predict_curve(model, f, X=np.arange(len(ts)+1, len(ts)+1+len(index)))
    new_york = new_york.append(pd.DataFrame(data=preds, index=index, columns=["forecast"]))
    
    ## plot
    utils_plot_parametric(new_york, zoom=zoom)
    return new_york
    
# test logistic curve
def f(x): 
    return 90000 / (1 + np.exp(-0.5*(x-20)))

y_logistic = f(x=np.arange(len(new_york)))

def f(X, c, k, m):
    y = c / (1 + np.exp(-k*(X-m)))
    return y

# fit the logistic curve to the model
model = fit_curve(X=np.arange(len(new_york["cases"])), y=new_york["cases"].values, f=f, p0=[np.max(new_york["cases"]), 1, 1])

# forecast the model based on the logistic curve
preds = forecast_curve(new_york["cases"], f, model, pred_ahead=60, end=None, freq="D", zoom=15, figsize=(15,5))

# create Gaussian curve
def gauss(X, a, b, c):
    y = a * np.exp(-0.5 * ((X-b)/c)**2)
    return y

# the first row had a NaN value, so it needs to be filled with "0" before testing the new cases 
new_york.fillna(0, inplace=True)

# fit the Gaussian curve to the model
model = fit_curve(X=np.arange(len(new_york["new_cases"])), y=new_york["new_cases"].values, f=gauss, p0=[1, np.mean(new_york["new_cases"]), np.std(new_york["new_cases"])])

# forecast the model based on the Gaussian curve
preds = forecast_curve(new_york["new_cases"], gauss, model, pred_ahead=60, end=None, freq="D", zoom=15, figsize=(15,5))
