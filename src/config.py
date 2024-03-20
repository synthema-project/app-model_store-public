import mlflow as mlf
import os

MLFLOW_TRACKING_URI = os.environ['MLFLOW_TRACKING_URI']
MLFLOW_PROXY_PORT = int(os.environ['MLFLOW_PROXY_PORT'])


mlf.set_tracking_uri(MLFLOW_TRACKING_URI)
client = mlf.MlflowClient(tracking_uri=MLFLOW_TRACKING_URI)
