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
    Receive the dataframe and replace in the gender column 1 with m and 2 with f.
    
    Parameters
    ----------
    dataframe: pandas.core.frame.DataFrame
           
    Returns
    -------
    pandas.core.series.Series: 
        Returns the modified dataframe.
    """
    
    dataframe['log_premium'] = np.log(dataframe['Annual_Premium'])
    data_mask = dataframe['log_premium'] > 9
    dataframe = dataframe[data_mask]
    
    
    return dataframe

