# from fastapi import FastAPI
# from app.api.estimate import router as estimate_router
# from app.api.explain import router as explain_router 
# app = FastAPI(
#     title="AI Planning Service",
#     version="1.0.0"
# )

# @app.get("/health")
# def health_check():
#     return {"status": "ok"}




# app = FastAPI(title="AI Service")

# app.include_router(estimate_router, prefix="/api")
# app.include_router(explain_router, prefix="/ai") 



from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.estimate import router as estimate_router
from app.api.explain import router as explain_router

app = FastAPI(
    title="AI Planning Service",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development, allow all. In production, list specific domains.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health_check():
    return {"status": "ok"}

app.include_router(estimate_router, prefix="/api")
app.include_router(explain_router, prefix="/ai")
