from fastapi import FastAPI

from .routers import encoder_router, health_router

app = FastAPI(title="SPLADE Encoder API")

# Include routers
app.include_router(encoder_router)
app.include_router(health_router)
