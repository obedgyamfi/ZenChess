from fastapi import FastAPI
from api.routes import evaluator_routes
from db.database import Base, engine
# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="ZenChess API", version="1.0")

# Register routes
app.include_router(evaluator_routes.router, prefix="/api/v1", tags=["Evaluator"])

@app.get("/")
def root():
    return {"status": "ZenChess API running"}
