import pandas as pd
import numpy as np
import pickle
import os 
from datetime import datetime, timedelta


def get_config_param(name):
     keys = pd.read_csv('config_params.csv')
     try:
        return keys[keys['key_name'] == str.lower(name)].iloc[0]['value']
     except:
        return False

def reload(folder_path, file_name):
    file_path = f'{folder_path}/{file_name}'
    with open(f'{file_path}', 'rb') as file:
        return pickle.load(file)

def save_api_result(folder_path, file_name, result):
    if not os.path.exists(folder_path):
            os.makedirs(folder_path)

    file_path = f'{folder_path}/{file_name}'

    with open(f'{file_path}', 'wb') as file:
        pickle.dump(result, file)


def pivottable(df, values, index, columns, aggfunc):
    table = pd.pivot_table(df, values=values, index=[index],
                       columns=[columns], aggfunc=aggfunc,fill_value='')
    return table

def convert_df(df):
   return df.to_csv(index=False).encode('utf-8')

def get_timestamp():
   return datetime.now().strftime("%Y%m%d%H%M%S")
