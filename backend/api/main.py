from contextlib import asynccontextmanager
from fastapi import FastAPI

from api.routers import checkpoints, llms, mcps
from backend.db.session import engine
from backend.db.models import SQLModel


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    yield


app = FastAPI(
    swagger_ui_parameters={"tryItOutEnabled": True},
    lifespan=lifespan,
)
app.include_router(llms.router, prefix="/v1")
app.include_router(mcps.router, prefix="/v1")
app.include_router(checkpoints.router, prefix="/v1")
