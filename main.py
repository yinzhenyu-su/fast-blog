from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from datetime import datetime

app = FastAPI()

class Time():
    time = ''
    def __init__(self, time: str):
        self.time = time

@app.get('/')
def root_get():
    return {
        'message': 'hello world!'
    }

@app.get('/time')
def time_get():
    return ORJSONResponse(Time(datetime.now().strftime('%Y-%m-%d %H:%M:%S %f')).__dict__)

if __name__=='__main__':
    import uvicorn
    uvicorn.run(app,host="localhost",port=8000)