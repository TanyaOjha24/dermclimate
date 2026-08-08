from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI

from bootstrap.application import create_dermclimate_service
from api.endpoints.health import router as health_router
from api.endpoints.chat import router as chat_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Initialize the DermClimate application once when FastAPI starts.
    """

    load_dotenv()

    app.state.dermclimate = create_dermclimate_service()

    print("DermClimate API started.")

    yield

    print("DermClimate API stopped.")


app = FastAPI(
    title="DermClimate API",
    description="AI-powered climate-aware skincare analysis platform",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(health_router)
app.include_router(chat_router)

