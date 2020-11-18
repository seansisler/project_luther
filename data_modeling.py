import statsmodels.api as sm
from sklearn.model_selection import train_test_split
from sklearn.feature_selection import mutual_info_regression, f_regression, SelectKBest
import numpy as np
from sklearn.preprocessing import StandardScaler
import pandas as pd
from collections import defaultdict
from statsmodels.stats.outliers_influence import variance_inflation_factor

def standardize_data(data):
    
    std = StandardScaler()
    
    new_data = std.fit_transform(data)
    
    return pd.DataFrame(new_data, columns=data.columns)

def linear_regression_summary(x, y):
    """
    Input is the independent variables (x) and the target/dependent variable (y).
    The independent variables will be scaled with scikit-learn's Standard Scaler class. 
    Returns the StatsModels' API summary report from running an OLS regression.
    """
    
    # standardize data
    x_scale = standardize_data(x)
    
    # add constant to independent variables
    model = sm.OLS(y, sm.add_constant(x_scale))
    
    # fit the model
    results = model.fit()
    
    # return the summary statistics
    return results.summary()

def fit_simple_lr(x, y):
    """
    Input is a single feature and the target variable. An OLS is performed and the output is the fit of the model.
    """
    # add constant to independent variables
    model = sm.OLS(y, sm.add_constant(x))

    # fit model
    fit = model.fit()
    
    return fit



def per_feature_OLS(x, y):
    """
    Input is the independent and dependent variables. The data for the independent variables is not standardized here because there aren't numerous features to have mor than one scale. Each feature has an OLS regression performed and the coefficent, standard error, t-value, and p-value are added to the return dictionary. 
    Output is a table with all of the statistics to help with feature selection.
    """
    
    return_dictionary = defaultdict(dict)
    
    
    for i in x.columns:
        
        fit = fit_simple_lr(x[i], y)
        
        params = fit.params
        t_test = fit.t_test([1, 0])
        
        return_dictionary[i]['coefficent'] = params['const']
        return_dictionary[i]['standard_error'] = t_test.sd[0][0]
        return_dictionary[i]['t_value'] = t_test.tvalue[0][0]
        return_dictionary[i]['p_value'] = t_test.pvalue
        
    df = pd.DataFrame.from_dict(return_dictionary).T.reset_index()
    
    
    return df

def select_best_k_features(x, y):
    
    # configure to select all features
    bestk = SelectKBest(score_func=f_regression, k='all')
    
    # fit to learn relationship
    bestk.fit(x, y)
    
    return bestk.scores_

def f_test_p_values(x, y):
    
    f_test, p_values = f_regression(x, y)
    
    f_test /= np.max(f_test)
    
    return f_test, p_values

def get_mutual_information(x,y):
    
    mutual_info = mutual_info_regression(x, y)
    mutual_info /= np.max(mutual_info)
    
    return mutual_info

def search_for_multicolinearity(x, y):
    
    std = StandardScaler()

    ## standardizing independent variables to deal with multicolinearity 
    x_scale = std.fit_transform(x)


    x_scale = pd.DataFrame(x_scale, columns=x.columns)
    
    # get feature importance scores from scikit-learn's SelectBestK calss
    scores = select_best_k_features(x_scale, y)

    # calculate mutual information/mutual dependence of the metascore with the independent variables - captures any kind of dependency between variables/how much information the presence or absence of a term contributes to making the product
    mutual_info = get_mutual_information(x_scale, y)

    # calculating f-test - linear dependancy 
    f_test, p_values = f_test_p_values(x_scale, y)

    # making df for visualization
    df = pd.DataFrame(list(zip(x_scale.columns, scores, mutual_info, f_test, p_values)), columns=['feature', 'select_best_k_score', 'mutual_information', 'f_test', 'p_value'])
    
    
    
    
    return df

def vif(x, y):
    """
    Input is the independent variables and the target variable. 
    Output is a DataFrame with that shows the variance inflation factor
    """
    
    x_scale = standardize_data(x)
    
    vif_data = pd.DataFrame()
    
    vif_data['feature'] = x_scale.columns
    vif_data['VIF'] = [variance_inflation_factor(x_scale.values, i) for i in range(len(x_scale.columns))]
    
    return vif_data.sort_values('VIF', ascending=False).reset_index(drop=True)


def train_val_test_split(x, y):
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=.2, random_state=4550)
    xtrain, x_val, ytrain, y_val = train_test_split(x_train, y_train, test_size=.25, random_state=4550)
    return xtrain, x_val, x_test, ytrain, y_val, y_test

        
    
    
    