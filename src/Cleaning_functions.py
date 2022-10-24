#!/usr/bin/env python
# coding: utf-8

# # Cleaning functions
# 

# In[1]:


import pandas as pd
import numpy as np
import random as rd


# ## 1.Functions to correct the categorical variables
# 

# In[2]:


def correct_Annual_Premium(dataframe):
    """
    Receive the dataframe and replace the Annual_Premium variable with the log of the feature. From the distribution 
    we choose the data with less dispersion. 
    Parameters
    ----------
    dataframe: pandas.core.frame.DataFrame
           
    Returns
    -------
    pandas.core.series.Series: 
        Returns the modified dataframe.
    """
    
    dataframe['log_premium'] = np.log(dataframe['Annual_Premium'])
    data_mask = dataframe['log_premium'] > dataframe['log_premium'].median()
    dataframe = dataframe[data_mask]
    
    
    return dataframe


# In[3]:


def correct_policy(dataframe):
    dataframe['Policy_Sales_Channel'] = np.where((dataframe['Policy_Sales_Channel'] != 152.0) & (dataframe['Policy_Sales_Channel'] != 26.0) & (dataframe['Policy_Sales_Channel'] != 160.0) & (dataframe['Policy_Sales_Channel'] != 122.0), 'other', dataframe['Policy_Sales_Channel'])
    return dataframe

