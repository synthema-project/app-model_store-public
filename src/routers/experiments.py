from config import client
from fastapi import APIRouter

router = APIRouter(
    prefix="/experiments",
    tags=["experiments"],
    dependencies=None
)


@router.get("/")
# async def get_experiments(current_user=Security(auth.get_current_user)):
async def get_experiments():
    return client.search_experiments()


@router.get("/{experiment_id}")
# async def get_experiment_by_id(experiment_id, current_user=Security(auth.get_current_user)):
async def get_experiment_by_id(experiment_id):
    return client.get_experiment(experiment_id)


@router.get("/name/{experiment_name}")
# async def get_experiment_by_name(experiment_name: str, current_user=Security(auth.get_current_user)):
async def get_experiment_by_name(experiment_name: str):
    return client.get_experiment_by_name(experiment_name)


@router.get("/runs/{experiment_id}")
# async def get_experiment_runs(experiment_id: str, current_user=Security(auth.get_current_user)):
async def get_experiment_runs(experiment_id: str):
    return client.search_runs(experiment_ids=experiment_id)
