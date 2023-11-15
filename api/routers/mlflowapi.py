from fastapi import status, APIRouter, Depends, HTTPException, Security, File, UploadFile, Request
from starlette.responses import FileResponse
import config
# from helpers import auth, logger
import pickle
import mlflow as mlf
# log = logger.setup_applevel_logger()

router = APIRouter(
    prefix="/mlflow",
    tags=["mlflow"],
    dependencies=None
)

mlflow_container_url = "http://synthema-mlflow"
# mlflow_container_url = config.MLFLOW_URL

mlf.set_tracking_uri(mlflow_container_url)


@router.get("/models")
# async def get_models(current_user=Security(auth.get_current_user)):
async def get_models():
    mlf.set_tracking_uri(f"{mlflow_container_url}:5002/")
    return mlf.search_registered_models()


@router.get("/models/{model_name}")
# async def get_model(model_name: str, current_user=Security(auth.get_current_user)):
async def get_model(model_name: str):
    return mlf.search_registered_models(filter_string=f"name = '{model_name}'")


@router.post("/models/{model_name}")
# async def create_model(model_name: str , file: UploadFile = File(...), current_user=Security(auth.get_current_user)):
async def create_model(model_name: str , file: UploadFile = File(...)):
    mlf.set_tracking_uri(f"{mlflow_container_url}:5000/")
    py_model = file.file.read()
    model = pickle.loads(py_model)
    mlf.pyfunc.log_model(
         python_model=model,
         artifact_path="model",
         registered_model_name=model_name,
     )
    return f'Model \'{model_name}\' registered'


@router.get("/experiments")
# async def get_experiments(current_user=Security(auth.get_current_user)):
async def get_experiments():
    return mlf.search_experiments()


@router.get("/experiments/{experiment_id}")
# async def get_experiment_by_id(experiment_id, current_user=Security(auth.get_current_user)):
async def get_experiment_by_id(experiment_id):
    return mlf.search_experiments(filter_string=f"id = '{experiment_id}'")


@router.get("/experiments/name/{experiment_name}")
# async def get_experiment_by_name(experiment_name: str, current_user=Security(auth.get_current_user)):
async def get_experiment_by_name(experiment_name: str):
    return mlf.search_experiments(filter_string=f"name = '{experiment_name}'")


@router.get("/experiment/runs/{experiment_id}")
# async def get_experiment_runs(experiment_id: str, current_user=Security(auth.get_current_user)):
async def get_experiment_runs(experiment_id: str):
    runs = mlf.search_runs(experiment_ids=[experiment_id], output_format="list")
    return runs


@router.get("/runs/{run_id}")
# async def get_run(run_id: str, current_user=Security(auth.get_current_user)):
async def get_run(run_id: str):
    return mlf.search_runs(filter_string=f"id = '{run_id}'")

#
# @routers.get("/artifacts")
# async def get_artifact(current_user=Security(auth.get_current_user)):
#     mlflow_url = config.MLFLOW_URL+"/api/2.0/preview/mlflow/artifacts/list"
#     resp = requests.get(mlflow_url)
#     return resp.json()


@router.get("/artifacts/{run_id}")
# async def get_run_artifacts(run_id: str, current_user=Security(auth.get_current_user)):
async def get_run_artifacts(run_id: str):
    return mlf.MlflowClient().list_artifacts(run_id=run_id)


@router.get("/artifacts/download/{run_id}", response_class=FileResponse)
# async def download_run_artifacts(run_id: str, current_user=Security(auth.get_current_user)):
async def download_run_artifacts(run_id: str):
    mlf.set_tracking_uri(f"{mlflow_container_url}:5002/")
    resp = mlf.artifacts.download_artifacts(run_id=run_id)
    return FileResponse(resp + "/results.npz", filename="results.npz", media_type="application/octet-stream")


@router.get("/metrics/{run_id}")
# async def get_run_metrics(run_id: str, current_user=Security(auth.get_current_user)):
async def get_run_metrics(run_id: str):
    return mlf.MlflowClient().get_metric_history(run_id=run_id)
