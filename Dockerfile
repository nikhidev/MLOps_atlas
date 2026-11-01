
# syntax=docker/dockerfile:1.7

FROM python:3.11-slim

WORKDIR /app

COPY flask_app/ /app/

RUN pip install --no-cache-dir -r requirements.txt

RUN python -m nltk.downloader stopwords wordnet

RUN mkdir -p /models

# Download matching vectorizer securely from DagsHub
RUN --mount=type=secret,id=capstone_test,env=CAPSTONE_TEST \
    python -c "import os, mlflow, shutil; token=os.environ['CAPSTONE_TEST']; os.environ['MLFLOW_TRACKING_USERNAME']=token; os.environ['MLFLOW_TRACKING_PASSWORD']=token; mlflow.set_tracking_uri('https://dagshub.com/nikhidev/MLOps_atlas.mlflow'); client=mlflow.tracking.MlflowClient(); versions=client.search_model_versions(\"name='my_model'\"); latest=max(versions,key=lambda v:int(v.version)); path=mlflow.artifacts.download_artifacts(run_id=latest.run_id,artifact_path='preprocessing/vectorizer.pkl'); shutil.copy2(path,'/models/vectorizer.pkl')"

EXPOSE 5000

# CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--timeout", "120", "app:app"]


# CMD ["python", "app.py"]

# Production
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--timeout", "120", "app:app"]