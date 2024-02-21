from typing import Literal
import cloudpickle

from starlette.responses import StreamingResponse, Response

from config import client, mlf
import pickle
from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from helpers import logger

log = logger.setup_applevel_logger("router-models")


router = APIRouter(
    prefix="/models",
    tags=["models"],
    dependencies=None
)


@router.get("/")
# async def get_models(current_user=Security(auth.get_current_user)):
async def get_models():
    return client.search_registered_models()


@router.get("/{model_name}")
# async def get_model(model_name: str, current_user=Security(auth.get_current_user)):
async def get_model(model_name: str):
    return client.search_registered_models(filter_string=f"name = '{model_name}'")


@router.get("/{model_name}/versions")
# async def get_model(model_name: str, current_user=Security(auth.get_current_user)):
async def get_model_versions(model_name: str):
    return client.search_model_versions(filter_string=f"name = '{model_name}'")


@router.post("/upload/{model_name}", status_code=201)
async def upload_model(
        model_name: str,
        disease: Literal["AML", "SCD"] = Form(),
        description: str = Form(),
        trained: bool = Form(),
        file: UploadFile = File(...)
):
    mlf.set_experiment(model_name)
    py_model = file.file.read()
    model = pickle.loads(py_model)
    if not trained:
        if not hasattr(model, "create_strategy") or not hasattr(model, "create_model"):
            raise HTTPException(
                422,
                "could not find one of [create_strategy, create_model] as methods of the uploaded pickle"
            )
    if not trained:
        run_name = f"upload_{model_name}"
    else:
        run_name = f"trained_{model_name}"

    with mlf.start_run(run_name=run_name):
        model_info: mlf.models.model.ModelInfo = mlf.pyfunc.log_model(
            python_model=model,
            artifact_path="model",
            registered_model_name=model_name,
        )

    model_meta = client.get_latest_versions(model_name, stages=["None"])
    version = model_meta[0].version
    client.update_model_version(model_name, version, description)
    tags = {
        "disease": disease,
        "trained": trained,
        "run_id": model_info.run_id,
        "utc_time_created": model_info.utc_time_created
    }
    for key, value in tags.items():
        client.set_model_version_tag(model_name, version, key, value)
    # client.set_model_version_tag(model_name, version, "disease", disease)
    # client.set_model_version_tag(model_name, version, "trained", trained)
    return {
        "detail": f"Model \'{model_name}\' registered.",
        "model_uuid": model_info.model_uuid,
        "run_id": model_info.run_id,
        "model_uri": model_info.model_uri
    }


@router.get("/download/{model_name}/{version}")
async def download_model(model_name: str, version: int):
    uri = client.get_model_version_download_uri(model_name, str(version))
    model = mlf.pyfunc.load_model(uri).unwrap_python_model()
    ser_model = cloudpickle.dumps(model)
    return Response(content=ser_model, media_type="application/octet-stream")
