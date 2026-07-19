from fastapi import FastAPI
from agents.optimize import app as optimize_app

# Ithu thaan main gateway
app = FastAPI(title="City Pollution OS")

# Unga Optimization Agent-a mount pandrom
app.mount("/optimize", optimize_app)

@app.get("/")
def root():
    return {"message": "City Pollution OS is live! Agents connected."}
