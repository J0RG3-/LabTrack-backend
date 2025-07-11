import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.routes.api_router import api_router
from config import settings as cf


def create_app() -> FastAPI:
    app = FastAPI(
        title=cf.PROJECT_NAME,
    )

    origins = [
    "http://localhost:5173",
]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # if cf.BACKEND_CORS_ORIGINS:
    #     app.add_middleware(
    #         CORSMiddleware,
    #         allow_origins=[str(origin) for origin in cf.BACKEND_CORS_ORIGINS],
    #         allow_credentials=True,
    #         allow_methods=["*"],
    #         allow_headers=["*"],
    #     )

    app.include_router(api_router)

    return app


app = create_app()

if __name__ == "__main__":
    host = "localhost"
    port = 8000
    uvicorn.run(app, host=host, port=port)
