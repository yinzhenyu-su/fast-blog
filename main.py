from logging import error
import os
import pathlib
from typing import Optional
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from datetime import datetime
import tempfile
from starlette.requests import Request

from starlette.responses import Response, StreamingResponse

from utils.transform import FTransform

app = FastAPI(title="BGM.FUN",
              description="BGM.FUN back support.",
              version="0.0.1")
transform = FTransform()
temp_dir = tempfile.mktemp()
os.mkdir(temp_dir)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Time():
    time = ''

    def __init__(self, time: str):
        self.time = time


@app.exception_handler(exc_class_or_status_code=404)
def err_404(request: Request, exc):
    return JSONResponse({'message': 'resource not found'}, status_code=404)


@app.get('/')
def root_get():
    return {'message': 'hello world!'}


@app.post('/video2mp3/', response_class=JSONResponse)
async def video2mp3(file: UploadFile = File(...)):
    temp_file = os.path.join(temp_dir, file.filename)
    try:
        f = open(temp_file, 'wb')
        f.write(file.file.read())
        filename = transform.video2mp3(temp_file)
        return JSONResponse({'file': filename})
    except error:
        return JSONResponse({'message': 'transform video error'},
                            status_code=500)
    finally:
        file.file.close()


@app.get('/tempfile/')
async def tempfile(filename: str):
    file_path = pathlib.Path(temp_dir, filename)
    if os.path.exists(file_path):
        file = open(file_path, 'rb')
        return StreamingResponse(file, media_type='audio/mpeg')
    return JSONResponse({'message': 'file not exists.'}, status_code=404)


@app.get('/time/')
def time_get():
    return JSONResponse(
        Time(datetime.now().strftime('%Y-%m-%d %H:%M:%S %f')).__dict__)


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=4000)
