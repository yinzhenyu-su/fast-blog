from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def root_get():
    return {
        'message': 'hello world!'
    }

if __name__=='__main__':
    import uvicorn
    uvicorn.run(app,host="localhost",port=8000)