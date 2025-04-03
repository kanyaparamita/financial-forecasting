from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

app = FastAPI(
    title="Financial Forecasting API",
    description="API for financial forecasting models",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Financial Forecasting API is running"}

@app.get("/health")
async def health_check():
    return JSONResponse(
        content={"status": "healthy"},
        status_code=200
    ) 