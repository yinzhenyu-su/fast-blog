from routes import utils, user
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.requests import Request
from db import database, metadata, engine

metadata.create_all(engine)

app = FastAPI(title="BGM.FUN",
              description="BGM.FUN back support.",
              version="0.0.1")


@app.on_event('startup')
async def startup():
    await database.connect()


@app.on_event('shutdown')
async def shutdown():
    await database.disconnect()


origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(utils.router)
app.include_router(user.router)


@app.exception_handler(exc_class_or_status_code=404)
def err_404(request: Request, exc):
    return JSONResponse({'message': 'resource not found'}, status_code=404)


@app.get('/')
def root():
    return JSONResponse({'message': 'hello world'})
