import os
from datetime import datetime
from pathlib import Path
from fastapi.datastructures import UploadFile
from fastapi.param_functions import File
from fastapi import APIRouter
from starlette.responses import JSONResponse, StreamingResponse
from . import temp_dir, transform

router = APIRouter(prefix='/utils')


@router.post('/video2mp3/')
async def video2mp3(file: UploadFile = File(...)):
    temp_file = os.path.join(temp_dir, file.filename)
    try:
        f = open(temp_file, 'wb')
        f.write(file.file.read())
        filename = transform.video2mp3(temp_file)
        return JSONResponse({'file': filename})
    except BaseException as e:
        return JSONResponse({'message': 'transform video error'},
                            status_code=500)
    finally:
        file.file.close()


@router.get('/tempfile/')
async def tempfile(filename: str):
    file_path = Path(temp_dir, filename)
    if os.path.exists(file_path):
        file = open(file_path, 'rb')
        return StreamingResponse(file, media_type='audio/mpeg')
    return JSONResponse({'message': 'file not exists.'}, status_code=404)


@router.get('/time/')
def time_get():
    return JSONResponse(
        {'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S %f')})
