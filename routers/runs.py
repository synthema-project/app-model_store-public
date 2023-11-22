from config import client
from starlette.responses import FileResponse
from fastapi import APIRouter

router = APIRouter(
    prefix="/runs",
    tags=["runs"],
    dependencies=None
)


@router.get("/{run_id}")
# async def get_run(run_id: str, current_user=Security(auth.get_current_user)):
async def get_run(run_id: str):
    return client.search_runs(filter_string=f"id = '{run_id}'")


@router.get("/artifacts/{run_id}")
# async def get_run_artifacts(run_id: str, current_user=Security(auth.get_current_user)):
async def get_run_artifacts(run_id: str):
    return client.list_artifacts(run_id=run_id)


@router.get("/artifacts/download/{run_id}", response_class=FileResponse)
# async def download_run_artifacts(run_id: str, current_user=Security(auth.get_current_user)):
async def download_run_artifacts(run_id: str):
    #mlf.set_tracking_uri(f"{mlflow_container_url}")
    resp = client.download_artifacts(run_id=run_id)
    return FileResponse(resp + "/results.npz", filename="results.npz", media_type="application/octet-stream")


@router.get("/metrics/{run_id}")
# async def get_run_metrics(run_id: str, current_user=Security(auth.get_current_user)):
async def get_run_metrics(run_id: str):
    return client.get_metric_history(run_id=run_id)

