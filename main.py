import os
import pathlib
from typing import Optional
from fastapi import FastAPI,File,UploadFile
from fastapi.responses import JSONResponse, FileResponse
from datetime import datetime
import tempfile

from starlette.responses import Response, StreamingResponse

from utils.transform import FTransform

app = FastAPI()
transform = FTransform()
temp_dir = tempfile.mktemp()
os.mkdir(temp_dir)
print('testset')
class Time():
    time = ''
    def __init__(self, time: str):
        self.time = time

@app.get('/')
def root_get():
    return {
        'message': 'hello world!'
    }

@app.post('/mp4tomp3/')
def mp4tomp3(file: UploadFile=File(...)):
    temp_file = os.path.join(temp_dir, file.filename)
    with open(temp_file, 'wb') as f:
        f.write(file.file.read())
        (abs_path, filename) = transform.mp42mp3(temp_file)
        return JSONResponse({
            'file': filename
        })

@app.get('/tempfile/')
def tempfile(filename: Optional[str] = None):
    file_path = pathlib.Path(temp_dir,filename)
    if filename:
        if os.path.exists(file_path):
            file = open(file_path, 'rb')
            return StreamingResponse(file, media_type='audio/mpeg')
        return JSONResponse({
            'message': 'file not exists.'
        }, status_code=404)

@app.get('/time/')
def time_get():
    return JSONResponse(Time(datetime.now().strftime('%Y-%m-%d %H:%M:%S %f')).__dict__)

if __name__=='__main__':
    import uvicorn
    uvicorn.run(app,host="0.0.0.0",port=8000)