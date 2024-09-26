from fastapi.testclient import TestClient
import cloudpickle
import pytest

from src.main import create_app

client = TestClient(create_app())


@pytest.fixture(scope="module")
def test_upload_model(model_generator, mock_mlflow_uri):
    model_name = "jenkins_test_model"
    disease = "AML"
    description = "Test description"

    file = cloudpickle.dumps(model_generator)


    response = client.post(
        "/models/upload",
        data={"model_name": model_name, "disease": disease, "description": description},
        files={"file": ("test_file.pkl", file, "application/octet-stream")},
    )
    assert response.status_code == 201, f"Failed with response: {response.text}"
    assert response.json()["detail"] == f"Model '{model_name}' registered."
    yield

def test_download_model(test_upload_model, mock_mlflow_uri):
    model_name = "jenkins_test_model"
    response = client.get(f"/models/download/{model_name}/1")
    assert response.status_code == 200

def test_get_model(test_upload_model, mock_mlflow_uri):
    model_name = "jenkins_test_model"
    response = client.get(f"/models/{model_name}")
    assert response.status_code == 200

def test_get_model_versions(test_upload_model, mock_mlflow_uri):
    model_name = "jenkins_test_model"
    response = client.get(f"/models/{model_name}/versions")
    assert response.status_code == 200