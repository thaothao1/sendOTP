from fastapi import FastAPI
import uvicorn
from utils.dbUtil import database
from auth import router as auth_router 
from otps import router as opt_router

app = FastAPI(
    docs_url="/docs",
    redoc_url="/redocs",
    title= "FastAPI (Python)",
    description="FastAPI Framework , high performance, <br>"
                "easy to learn , fast to code , ready for production",
    version="1.0",
    openapi_url="/openapi.json"
)

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()



@app.get("/hello")
def hello():
    return "hello coder"

app.include_router(auth_router.router , tags=["Auth"])
app.include_router(opt_router.router , tags=["OTP"])

if __name__ =="__main__":
    uvicorn.run(app, port=8001)