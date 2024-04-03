from unittest.mock import patch, MagicMock, call
from fastapi.testclient import TestClient
import pytest
import cloudpickle

from src.main import create_app

client = TestClient(create_app())

class ModelGenerator:
    def create_strategy(self):
        pass

    def create_model(self):
        pass


@pytest.fixture
def model_generator():
    yield ModelGenerator()

@patch('src.routers.models.mlflow_client')
@patch('src.routers.models.mlflow')
def test_upload_model(mock_mlflow, mock_mlflow_client, model_generator):
    mock_mlflow.pyfunc.log_model.return_value = MagicMock()
    mock_mlflow.start_run.return_value.__enter__.return_value = None
    mock_mlflow.set_experiment.return_value = None

    model_name = "test_model"
    disease = "AML"
    description = "Test description"

    file = cloudpickle.dumps(model_generator)

    response = client.post(
        "/models/upload",
        data={"model_name": model_name, "disease": disease, "description": description},
        files={"file": ("test_file.pkl", file, "application/octet-stream")},
    )
    assert response.status_code == 201, f"Failed with response: {response.text}"

    # Check that the mock functions were called with the correct arguments
    mock_mlflow.set_experiment.assert_called_once_with(model_name)
    mock_mlflow.pyfunc.log_model.assert_called_once()
    mock_mlflow.start_run.assert_called_once_with(run_name=f"upload_{model_name}")

    # Check the arguments of log_model
    log_model_args, log_model_kwargs = mock_mlflow.pyfunc.log_model.call_args
    assert log_model_kwargs["python_model"] is not None
    assert log_model_kwargs["artifact_path"] == "model"
    assert log_model_kwargs["registered_model_name"] == model_name