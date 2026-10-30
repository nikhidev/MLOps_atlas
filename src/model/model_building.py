import numpy as np 
import pandas as pd 
import pickle
from sklearn.linear_model import LogisticRegression
import yaml
from src.logger import logging
import os
def load_data(file_path:str) -> pd.DataFrame:
    """" load the data from CSV file and return a pandas DataFrame."""
    try:
        df = pd.read_csv(file_path)
        logging.info(f"Data loaded successfully from {file_path}")
        return df
    except pd.errors.ParserError as e:
        logging.error(f"Error parsing the CSV file: {e}")
        raise
    except Exception as e:
        logging.error(f"An error occurred while loading the data: {e}")
        raise
def train_model(X_train: pd.DataFrame, y_train: pd.Series) -> LogisticRegression:
    """Train a logistic regression model."""
    try:
        logging.info("Training the logistic regression model...")
        model = LogisticRegression(C=1,solver='liblinear', penalty='l2', max_iter=1000)
        model.fit(X_train, y_train)
        logging.info("Model training completed successfully.")
        return model
    except Exception as e:
        logging.error(f"An error occurred during model training: {e}")
        raise
def save_model(model: LogisticRegression, model_path: str) -> None:
    """Save the trained model to a file."""
    try:
        with open(model_path, 'wb') as file:
            pickle.dump(model, file)
        logging.info(f"Model saved successfully to {model_path}")
    except Exception as e:
        logging.error(f"An error occurred while saving the model: {e}")
        raise

def main():
    try:
        train_data = load_data('./data/processed/train_bow.csv') 
        X_train = train_data.iloc[:, :-1].values
        y_train = train_data.iloc[:, -1].values


        clf = train_model(X_train, y_train)
        os.makedirs('./models', exist_ok=True)
        save_model(clf, './models/model.pkl')
    except Exception as e:
        logging.error(f"An error occurred in the main function: {e}")
        raise

if __name__ == "__main__":
    main()    