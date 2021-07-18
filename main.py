from routes import utils
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.requests import Request

app = FastAPI(title="BGM.FUN",
              description="BGM.FUN back support.",
              version="0.0.1")

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(utils.router)


@app.exception_handler(exc_class_or_status_code=404)
def err_404(request: Request, exc):
    return JSONResponse({'message': 'resource not found'}, status_code=404)


@app.get('/')
def root():
    return JSONResponse({'message': 'hello world'})


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=4000)
