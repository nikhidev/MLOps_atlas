import numpy as np 
import pandas as pd
import sys

# from src.features.feature_engineering import load_params
pd.set_option('future.no_silent_downcasting', True)


import os
from sklearn.model_selection import train_test_split
import yaml
import logging
from src.logger import logging
from src.connections import s3_connection



def load_params(params_path: str) -> dict:
    """Load parameters from a YAML file."""
    try:
        with open(params_path, 'r') as file:
            params = yaml.safe_load(file)
        logging.debug('Parameters retrieved from %s', params_path)
        return params
    except FileNotFoundError:
        logging.error('File not found: %s', params_path)
        raise
    except yaml.YAMLError as e:
        logging.error('YAML error: %s', e)
        raise
    except Exception as e:
        logging.error('Unexpected error: %s', e)
        raise

def load_data(data_url:str) -> pd.DataFrame:
    """ Load the data from CSV file and return a pandas DataFrame."""

    try:
        df = pd.read_csv(data_url)
        logging.info(f"Data loaded successfully from {data_url}")
        return df
    except pd.errors.ParserError as e:
        logging.error(f"Error parsing the CSV file: {e}")
        raise
    except Exception as e:
        logging.error(f"An error occurred while loading the data: {e}")
        raise

def preprocess_data(df:pd.DataFrame)-> pd.DataFrame:
    """Preprocess the data"""    

    try:
        logging.info("Starting data preprocessing...")
        final_df = df[df['sentiment'].isin(['positive', 'negative'])]
        final_df['sentiment'] = final_df['sentiment'].map({'positive': 1, 'negative': 0})
        logging.info("Data preprocessing completed successfully.")
        return final_df
    except KeyError as e:
        logging.error(f"KeyError: {e}. Please ensure the 'sentiment' column exists in the DataFrame.")
        raise
    except Exception as e:
        logging.error(f"An error occurred during data preprocessing: {e}")
        raise

def save_data(train_data: pd.DataFrame, test_data: pd.DataFrame, data_path: str) -> None:
    """Save the train and test datasets."""
    try:
        raw_data_path = os.path.join(data_path, 'raw')
        os.makedirs(raw_data_path, exist_ok=True)
        train_data.to_csv(os.path.join(raw_data_path, "train.csv"), index=False)
        test_data.to_csv(os.path.join(raw_data_path, "test.csv"), index=False)
        logging.debug('Train and test data saved to %s', raw_data_path)
    except Exception as e:
        logging.error('Unexpected error occurred while saving the data: %s', e)
        raise


# def main():
#     try:
#         # params = load_params(params_path='params.yaml')
#         # test_size = params['data_ingestion']['test_size']
#         test_size = 0.2
        
#         # df = load_data(data_url='https://raw.githubusercontent.com/vikashishere/Datasets/refs/heads/main/data.csv')
#         s3 = s3_connection.s3_operations("bucket-name", "accesskey", "secretkey")
#         df = s3.fetch_file_from_s3("data.csv")



#         final_df = preprocess_data(df)
#         train_data, test_data = train_test_split(final_df, test_size=test_size, random_state=42)
#         save_data(train_data, test_data, data_path='./data')
#     except Exception as e:
#         logging.error('Failed to complete the data ingestion process: %s', e)
#         print(f"Error: {e}")

# if __name__ == '__main__':
#     main()    

from src.connections.s3_connection import s3_operations
from src.logger import logging


if __name__ == "__main__":
    try:
        logging.info("Starting data ingestion process...")
        params = load_params(params_path='params.yaml')
        test_size = params['data_ingestion']['test_size']
        # test_size = 0.2

        ingestion = s3_operations(
            bucket_name="mlops-atlas1234",
            region_name="us-east-1"
        )

        df = ingestion.fetch_file_from_s3("data.csv")
        # df = load_data(data_url='https://raw.githubusercontent.com/vikashishere/Datasets/refs/heads/main/data.csv')
        print("\nData fetched successfully!")
        print("Shape:", df.shape)

        print("\nFirst 5 rows:")
        print(df.head())
        logging.info("Dataset shape: %s", df.shape)

        # Preprocess dataset
        final_df = preprocess_data(df)

        # Split into training and testing datasets
        train_data, test_data = train_test_split(
            final_df,
            test_size=test_size,
            random_state=42
        )
        save_data(
            train_data,
            test_data,
            data_path="./data"
        )

        logging.info("Data ingestion completed successfully.")
        logging.info("Training samples: %s", len(train_data))
        logging.info("Testing samples: %s", len(test_data))

        print("Data ingestion completed successfully!")
        print("Training data:", train_data.shape)
        print("Testing data:", test_data.shape)
        print("Saved to data/raw/train.csv and data/raw/test.csv")

    except Exception as e:
        logging.exception("Failed to complete the data ingestion process")
        raise



    except Exception as e:
        logging.exception("Failed to complete the data ingestion process")
        print(f"Error: {e}")