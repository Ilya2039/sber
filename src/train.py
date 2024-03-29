# -*- coding: utf-8 -*-
"""train.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1DzPbKCBma1GA2RPIMnQW3MLc82-tnS2l
"""

# src/train.py
import pandas as pd
from sklearn.model_selection import train_test_split, ParameterGrid
from catboost import CatBoostClassifier
from sklearn.metrics import f1_score

def load_preprocessed_data(filename):
    return pd.read_csv(filename)

def train_and_evaluate_model(X_train, y_train, X_valid, y_valid, cat_features):
    param_grid = {
        'learning_rate': [0.1],
        'depth': [7, 8],
        'iterations': [500, 1000],
        'l2_leaf_reg': [5, 10],
        'border_count': [96, 128],
    }
    best_score = 0
    best_params = None
    best_model = None

    for params in ParameterGrid(param_grid):
        model = CatBoostClassifier(**params, cat_features=cat_features, verbose=0)
        model.fit(X_train, y_train, eval_set=(X_valid, y_valid), early_stopping_rounds=50)
        preds = model.predict(X_valid)
        score = f1_score(y_valid, preds)
        if score > best_score:
            best_score = score
            best_params = params
            best_model = model

    print(f"Best F1 Score: {best_score}")
    print(f"Best Parameters: {best_params}")
    return best_model

def main():
    full_df = load_preprocessed_data('preprocessed_data.csv')
    X = full_df.drop(['diabetes', 'pressure'], axis=1)
    y = full_df['diabetes']
    cat_features = ['cholesterol', 'gluc', 'gender']

    X_train, X_valid, y_train, y_valid = train_test_split(X, y, test_size=0.3, random_state=42)
    best_model = train_and_evaluate_model(X_train, y_train, X_valid, y_valid, cat_features)

    if best_model:
        best_model.save_model('catboost_best_model.cbm')

if __name__ == "__main__":
    main()
