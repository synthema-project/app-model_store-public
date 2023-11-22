from config import client, mlf
import pickle
from fastapi import APIRouter, UploadFile, File

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


@router.post("/{model_name}")
# async def create_model(model_name: str , file: UploadFile = File(...), current_user=Security(auth.get_current_user)):
async def create_model(model_name: str, file: UploadFile = File(...)):
    py_model = file.file.read()
    model = pickle.loads(py_model)
    mlf.pyfunc.log_model(
         python_model=model,
         artifact_path="model",
         registered_model_name=model_name,
     )
    return f'Model \'{model_name}\' registered'
