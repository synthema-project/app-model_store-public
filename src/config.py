import mlflow
import os

def load_mlflow_client():
    MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI")
    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
    return mlflow.MlflowClient(tracking_uri=MLFLOW_TRACKING_URI)

mlflow_client = load_mlflow_client()
