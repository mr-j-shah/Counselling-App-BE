from fastapi import FastAPI
from app.db.session import engine
from app.db.base import Base
from app.api.v1.api import api_router

app = FastAPI(
    title="AuraMind API",
    description="Backend for counselling app",
    version="1.0.0",
)

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.include_router(api_router)
