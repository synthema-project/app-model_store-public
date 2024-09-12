import shutil
import pytest
from mlflow.pyfunc import PythonModel
import os

from src import config


def pytest_addoption(parser):
    parser.addoption("--env", action="store", default="local", help="Environment to run tests in: localhost or kubernetes")

def test_bucket_name():
    assert os.getenv('MLFLOW_S3_BUCKET') == 'cloud-bucket-name'

@pytest.fixture(scope="session")
def monkeysession(request):
    mp = pytest.MonkeyPatch()
    yield mp
    mp.undo()

@pytest.fixture(scope="session")
def mock_mlflow_uri(monkeysession, pytestconfig):
    env = pytestconfig.getoption("--env")
    if env == "local":
        config.mlflow_client = config.load_mlflow_client()
        yield
        shutil.rmtree("mlruns")
    elif env == "local-k8":
        raise NotImplementedError("Kubernetes environment not implemented")
    elif env == "cloud":
        # Set environment variables for cloud testing
        monkeysession.setenv("MLFLOW_S3_BUCKET", "mlflow")
        monkeysession.setenv("MLFLOW_TRACKING_URI", "s3://mflow")
        # Debugging: Print the environment variables
        print(f"MLFLOW_S3_BUCKET: {os.getenv('MLFLOW_S3_BUCKET')}")
        print(f"MLFLOW_TRACKING_URI: {os.getenv('MLFLOW_TRACKING_URI')}")
        test_bucket_name()
        yield
    else:
        raise ValueError(f"Unknown environment: {env}")


@pytest.fixture(scope="session")
def model_generator():
    class ModelGenerator(PythonModel):
        def create_strategy(self):
            pass

        def create_model(self):
            pass

    yield ModelGenerator()
