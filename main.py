from config import HOST, PORT, TRACKING_URI

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from helpers import logger
from routers import models, experiments, runs


def create_app():
    log = logger.setup_applevel_logger("main.py")

    log.warning(HOST)
    log.warning(PORT)
    log.warning(TRACKING_URI)

    app = FastAPI(
        swagger_ui_init_oauth={
            "usePkceWithAuthorizationCodeGrant": True
        }
    )

    app.include_router(models.router)
    app.include_router(experiments.router)
    app.include_router(runs.router)

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

    return app, log


def startup_app(app):
    uvicorn.run(app, host=HOST, port=PORT)


if __name__ == "__main__":
    app, log = create_app()
    startup_app(app)
