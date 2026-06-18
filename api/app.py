from fastapi import FastAPI

app = FastAPI(title="IT Training API", version="0.1.0")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/")
def root():
    return {"service": "it-training-api", "docs": "/docs"}


from routes import training as training_routes
app.include_router(training_routes.router)
