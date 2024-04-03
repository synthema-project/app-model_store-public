import shutil
import pytest
from mlflow.pyfunc import PythonModel

from src import config


def pytest_addoption(parser):
    parser.addoption("--env", action="store", default="local", help="Environment to run tests in: localhost or kubernetes")

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
        # mock_uri = "http://mlflow-service.namespace.svc.cluster.local"
        # monkeypatch.setenv("MLFLOW_TRACKING_URI", mock_uri)
        # config.mlflow_client = config.load_mlflow_client()
        # yield mock_uri
        raise NotImplementedError("Kubernetes environment not implemented")
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
