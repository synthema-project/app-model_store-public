from typing import Literal

import cloudpickle
from starlette.responses import Response
from fastapi import APIRouter, UploadFile, File, HTTPException, Form

from src.config import mlflow_client, mlflow

router = APIRouter(prefix="/models", tags=["models"], dependencies=None)


@router.get("/")
async def get_models():
    return mlflow_client.search_registered_models()


@router.get("/{model_name}")
async def get_model(model_name: str):
    return mlflow_client.search_registered_models(
        filter_string=f"name = '{model_name}'"
    )


@router.get("/{model_name}/versions")
async def get_model_versions(model_name: str):
    return mlflow_client.search_model_versions(filter_string=f"name = '{model_name}'")


@router.post("/upload", status_code=201)
async def upload_model(
    model_name: str = Form(),
    disease: Literal["AML", "SCD"] = Form(),
    description: str = Form(),
    file: UploadFile = File(...),
):
    mlflow.set_experiment(model_name)
    py_model = file.file.read()
    model = cloudpickle.loads(py_model)
    if not hasattr(model, "create_strategy") or not hasattr(model, "create_model"):
        raise HTTPException(
            422,
            "could not find one of [create_strategy, create_model] as methods of the uploaded pickle",
        )

    run_name = f"upload_{model_name}"

    with mlflow.start_run(run_name=run_name):
        model_info: mlflow.models.model.ModelInfo = mlflow.pyfunc.log_model(
            python_model=model,
            artifact_path="model",
            registered_model_name=model_name,
        )

    model_meta = mlflow_client.get_latest_versions(model_name, stages=["None"])
    version = model_meta[0].version
    mlflow_client.update_model_version(model_name, version, description)
    tags = {"disease": disease, "trained": False}
    for key, value in tags.items():
        mlflow_client.set_model_version_tag(model_name, version, key, value)
    return {
        "detail": f"Model '{model_name}' registered.",
        "model_uuid": model_info.model_uuid,
        "run_id": model_info.run_id,
        "model_uri": model_info.model_uri,
    }


@router.get("/download/{model_name}/{version}")
async def download_model(model_name: str, version: int):
    uri = mlflow_client.get_model_version_download_uri(model_name, str(version))
    model = mlflow.pyfunc.load_model(uri).unwrap_python_model()
    ser_model = cloudpickle.dumps(model)
    return Response(content=ser_model, media_type="application/octet-stream")


@router.delete("/{model_name}/versions/{version}")
async def delete_model_version(model_name: str, version: int):
    try:
        # Delete specific model version
        mlflow_client.delete_model_version(model_name, version)
        return {"detail": f"Model version {version} of model '{model_name}' has been deleted."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error deleting model version: {str(e)}")


@router.delete("/{model_name}")
async def delete_model(model_name: str):
    try:
        # Delete the entire registered model (and all its versions)
        mlflow_client.delete_registered_model(model_name)
        return {"detail": f"Model '{model_name}' and all its versions have been deleted."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error deleting model: {str(e)}")
