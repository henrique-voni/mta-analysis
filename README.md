# Analysis of MTA data (forecasting)
This repository holds a data analysis on MTA data. The dataset sums up to 7 years of registries categorized by station, turnistile and other fields. This analysis tries to capture temporal relationships with classic autoregressive models and forecast a period in time. 

Some decomposition techniques were applied in order to assert seasonality, trend and residual components in data. Also, null-hypothesis tests were applied in order to check for stationary features. 

In summary, it was concluded that data is consistent after processing, and the forecasting model could achieve feasible results without much trouble. Check the notebook for in-depth details of the experiment. 

## Repository Description 
- `requirements.txt`: Definition of specific package versions that should be used.
- `utils.py`: Helper script with utility functions used in analysis notebook.
- `analysis.ipynb`: main notebook containing all analysis and modelling tasks