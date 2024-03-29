# -*- coding: utf-8 -*-
"""test_sber_task.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1DzPbKCBma1GA2RPIMnQW3MLc82-tnS2l
"""

# src/test.py
import pandas as pd
import sqlite3
from catboost import CatBoostClassifier
from sklearn.metrics import f1_score

def load_and_combine_test_data(analysis_url, info_url):
    diabets_analysis_test = pd.read_csv(analysis_url)
    diabets_info_test = pd.read_csv(info_url)

    conn_test = sqlite3.connect(':memory:')
    diabets_info_test.to_sql('diabets_info_test', conn_test, index=False, if_exists='replace')
    diabets_analysis_test.to_sql('diabets_analysis_test', conn_test, index=False, if_exists='replace')

    query_test = """
    SELECT *
    FROM diabets_analysis_test
    JOIN diabets_info_test ON diabets_analysis_test.id = diabets_info_test.id
    """
    full_df_test = pd.read_sql_query(query_test, conn_test)
    conn_test.close()

    full_df_test.drop('id', axis=1, inplace=True)

    return full_df_test

def preprocess_test_data(df_test):
    df_test['pressure'] = df_test['pressure'].str.replace('\\', '/')
    df_test[['pressure1', 'pressure2']] = df_test['pressure'].str.split('/', expand=True)
    df_test['pressure1'] = pd.to_numeric(df_test['pressure1'], errors='coerce')
    df_test['pressure2'] = pd.to_numeric(df_test['pressure2'], errors='coerce')
    df_test['weight'].fillna(0, inplace=True)
    df_test['gender'] = df_test['gender'].replace({'f': 'female', 'm': 'male'})

    # Удаление столбца 'id', если он есть

    return df_test

def evaluate_model(model, X_test, y_test):
    y_pred = model.predict(X_test)
    f1 = f1_score(y_test, y_pred)
    print(f"f1_score на тестовой выборке: {f1:.4f}")

def main():
    analysis_url_test = 'https://raw.githubusercontent.com/Falconwatch/Hometasks/main/diabets/data/raw/diabetes_test_analysis.csv'
    info_url_test = 'https://raw.githubusercontent.com/Falconwatch/Hometasks/main/diabets/data/raw/diabetes_test_info.csv'

    full_df_test = load_and_combine_test_data(analysis_url_test, info_url_test)
    full_df_test = preprocess_test_data(full_df_test)

    X_test = full_df_test.drop(['diabetes', 'pressure'], axis=1)
    y_test = full_df_test['diabetes']

    loaded_model = CatBoostClassifier()
    loaded_model.load_model('catboost_best_model.cbm')

    evaluate_model(loaded_model, X_test, y_test)

if __name__ == "__main__":
    main()
