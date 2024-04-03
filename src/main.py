import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.routers import models, experiments, runs


def create_app():
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
    async def root():
        return {"message": "Pong"}

    return app


def startup_app(app, port: int):
    uvicorn.run(app, host='0.0.0.0', port=port)


if __name__ == "__main__":
    app, log = create_app()
    startup_app(app, port=80)
