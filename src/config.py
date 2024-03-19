import mlflow as mlf
import os

TRACKING_URI = os.environ['TRACKING_URI']
HOST = os.environ['HOST']
PORT = int(os.environ['PORT'])


mlf.set_tracking_uri(TRACKING_URI)
client = mlf.MlflowClient(tracking_uri=TRACKING_URI)
