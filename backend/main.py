from fastapi import FastAPI
from sqlalchemy.sql import text
from sqlalchemy.ext.asyncio import AsyncSession
from database import engine, Base, async_sessionmaker
from routers import clients
import uvicorn

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app = FastAPI()

app.include_router(clients.router)

@app.on_event("startup")
async def startup_event():
    await create_tables()

@app.get("/")
async def root():
    return {"message": "Backend is running!"}

@app.get("/healthcheck")
async def healthcheck():
    try:
        async with async_sessionmaker() as session:
            await session.execute(text("SELECT 1"))  
        return {"status": "ok", "database": "connected"}
    except Exception as e:
        return {"status": "error", "database": str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)