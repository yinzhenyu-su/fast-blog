import os
from fastapi import FastAPI,File,UploadFile
from fastapi.responses import JSONResponse, FileResponse
from datetime import datetime
import tempfile
from utils.transform import FTransform

app = FastAPI()
transform = FTransform()
class Time():
    time = ''
    def __init__(self, time: str):
        self.time = time

@app.get('/')
def root_get():
    return {
        'message': 'hello world!'
    }

@app.post('/mp4-to-mp3')
def mp42mp3(file: UploadFile=File(...)):
    temp_dir = tempfile.mktemp()
    temp_file = os.path.join(temp_dir, file.filename)
    os.mkdir(temp_dir)
    with open(temp_file, 'wb') as f:
        f.write(file.file.read())
    
    (abs_path,filename) = transform.mp42mp3(temp_file)
    return FileResponse(path=abs_path,filename=filename, headers={'keep-alive': 'timeout=120'})
    

@app.get('/time')
def time_get():
    return JSONResponse(Time(datetime.now().strftime('%Y-%m-%d %H:%M:%S %f')).__dict__)

if __name__=='__main__':
    import uvicorn
    uvicorn.run(app,host="0.0.0.0",port=8000)