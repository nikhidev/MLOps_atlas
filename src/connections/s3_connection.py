
import os
import boto3
import pandas as pd

from io import BytesIO
from botocore.exceptions import ClientError, BotoCoreError
from src.logger import logging
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file


class s3_operations:
    def __init__(
        self,
        bucket_name=None,
        aws_access_key=None,
        aws_secret_key=None,
        region_name=None,
    ):
        self.bucket_name = (
            bucket_name or os.getenv("AWS_BUCKET_NAME")
        )
        region_name = (
            region_name or os.getenv("AWS_REGION", "us-east-1")
        )

        if not self.bucket_name:
            raise ValueError("AWS_BUCKET_NAME is not configured")

        # Prefer explicitly supplied credentials; otherwise let
        # boto3 use its standard credential provider chain.
        client_kwargs = {"region_name": region_name}

        if aws_access_key and aws_secret_key:
            client_kwargs["aws_access_key_id"] = aws_access_key
            client_kwargs["aws_secret_access_key"] = aws_secret_key

        self.s3_client = boto3.client("s3", **client_kwargs)

        logging.info("Data ingestion from S3 bucket initialized")

    def fetch_file_from_s3(self, file_key):
        """Fetch a CSV file from S3 and return a DataFrame."""
        try:
            logging.info(
                f"Fetching file '{file_key}' "
                f"from S3 bucket '{self.bucket_name}'..."
            )

            response = self.s3_client.get_object(
                Bucket=self.bucket_name,
                Key=file_key,
            )

            df = pd.read_csv(BytesIO(response["Body"].read()))

            logging.info(
                f"Successfully fetched '{file_key}' "
                f"with {len(df)} records."
            )
            return df

        except (ClientError, BotoCoreError, pd.errors.ParserError):
            logging.exception(
                f"Failed to fetch or parse '{file_key}' from S3"
            )
            raise


if __name__ == "__main__":
    ingestion = s3_operations()
    df = ingestion.fetch_file_from_s3("data.csv")
    print(f"Data fetched with {len(df)} records.")
    print(df.head())
