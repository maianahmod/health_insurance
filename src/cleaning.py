
# Basic libraries
from datetime import datetime
#inicial_date = datetime.now()
import pandas as pd
import numpy as np
import datetime
import argparse
from sklearn.preprocessing import OneHotEncoder, StandardScaler



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
    data_mask = dataframe['log_premium'] > dataframe['log_premium'].mean()
    dataframe = dataframe[data_mask]
    dataframe =  dataframe.drop('log_premium', axis = 1)

    return dataframe


def correct_policy(dataframe):
    dataframe['Policy_Sales_Channel'] = np.where((dataframe['Policy_Sales_Channel'] != 152.0) & (dataframe['Policy_Sales_Channel'] != 26.0) & (dataframe['Policy_Sales_Channel'] != 160.0) & (dataframe['Policy_Sales_Channel'] != 122.0), 'other', dataframe['Policy_Sales_Channel'])
    return dataframe


def correct_Vehicle_Age(dataframe):
    dataframe['Vehicle_Age'] = dataframe.Vehicle_Age.map({"< 1 Year": "Vehicle_Age_lower 1 Year", "> 2 Years": "Vehicle_Age_higher 2 Years", "1-2 Year" : "1-2 Year"})
    return dataframe



def main(p_entrada, p_salida):
    ######################################################################################################################################
    # Importo el dataframe
    print("Importando el dataframe")
    now = datetime.datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Son las", current_time)
    df = pd.read_csv(p_entrada)
    print("Dataframe importado")
    
    
    # corrijo columna Annual_Premium
    print("Corrigiendo columna Annual_Premium")
    correct_Annual_Premium(df)
    print("Annual_Premium corregida")
   
    # corrijo columna Policy
    correct_policy(df)
    print("Corrigiendo columna Policy")
    print("Policy corregida")

    # corrijo columna Vehicle_Age
    correct_Vehicle_Age(df)
    print("Corrigiendo columna Vehicle_Age")
    print("Vehicle_Age corregida")

    
    print("dropeando variables que no necesito")
    
    df = df.drop('log_premium', axis = 1)
    df.drop("id", axis = 1, inplace=True)

    print("generando dummies")
    
    df['Driving_License'] = df['Driving_License'].astype(str)
    df['Region_Code'] = df['Region_Code'].astype(str)
    df['Previously_Insured'] = df['Previously_Insured'].astype(str)


    categoricals = ["Gender", "Driving_License", "Region_Code", "Previously_Insured", "Vehicle_Age", "Policy_Sales_Channel", 
               ]

    enc = OneHotEncoder(drop = "first")
    X = df[categoricals]
    enc.fit(X)
    enc.categories_
    dummies = enc.transform(X).toarray()
    
    dummies_df = pd.DataFrame(dummies)
    
    
    
    col_names = [categoricals[i] + '_' + enc.categories_[i] for i in range(len(categoricals))] 
    col_names_drop_first = [sublist[i] for sublist in col_names for i in range(len(sublist)) if i != 0]
    dummies_df.columns = col_names_drop_first
    numericals = ['Age', 'Annual_Premium', 'Vintage', 'Response']
    df = pd.concat([df[numericals], dummies_df], axis = 1)
    
    df.to_csv(p_salida, index = False)
    print("dataframe generado")
    print(df.head())
    print(df.shape)
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--path_entrada", type = str, required = True)
    parser.add_argument("--path_salida", type = str, required = True)
    args = parser.parse_args()
    
    entrada = args.path_entrada
    salida = args.path_salida
  
    
    main(entrada, salida) 
    
    

    
    
