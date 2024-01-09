import pandas as pd
import numpy as np
import hanzidentifier
import pickle
import os 
from datetime import datetime, timedelta
from apify_client import ApifyClient


def run_apify(api_key, urls, reviews_count,  test_apifyapi):
    client = ApifyClient(api_key)
    # Run the actor and wait for it to finish
    print(urls)
    run_input = {
        "language": "en",
        "maxReviews": reviews_count,
        "personalData":False,
        "startUrls": urls,
        "reviewsSort": "newest"

    }
    run = None
    if not test_apifyapi:
        run = client.actor("compass/google-maps-reviews-scraper").call(run_input=run_input)
    return run, client


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

if __name__ == '__main__':

    df = pd.DataFrame({"place_id": ["111", "111", "111", "111", "555",
                            "666", "777", "888", "999"],
                    "lang": ["en", "zh", "ja", "ko", "two",
                            "one", "one", "two", "two"],
                    "phone": ["09187", "09187", "09187", "09187",
                            "-", "-", "-", "-",
                            "large"],
                    "lang_count": [1, 2, 2, 3, 3, 4, 5, 6, 7],
                    })

    df = pd.read_csv('file (4).csv')

    pv = pivottable(df, 'lang_count', 'place_id', 'lang_x', np.sum)
    # print(pv)
    df = df.drop_duplicates(subset='place_id')
    # print(df)

    merged_df = pd.merge(df, pv, on='place_id', how='left')
    merged_df = merged_df.drop(columns=['lang_x', 'lang_count'])
    print(merged_df)

    merged_df.to_csv('merged_df_test.csv', index=False)


    text = 'いいサービスですね 服務很好'
    print(hanzidentifier.has_chinese(text))
    print(hanzidentifier.is_simplified(text))

