from fastapi import FastAPI, Security
from fastapi.middleware.cors import CORSMiddleware
from helpers import logger
from routers import mlflowapi
log = logger.setup_applevel_logger("main.py")
app = FastAPI(
    swagger_ui_init_oauth={
        "usePkceWithAuthorizationCodeGrant": True
    }
)

# app.include_router(users.router)
# app.include_router(tasks.router)
# app.include_router(datasets.router)
# app.include_router(nodes.router)
app.include_router(mlflowapi.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/")
async def root(
        # current_user=Security(auth.get_current_user, scopes=["/admin"])
):
    # print(current_user, flush=True)
    return {"message": "Pong"}


