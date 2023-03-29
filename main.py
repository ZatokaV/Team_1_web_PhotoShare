import uvicorn
from fastapi import FastAPI

app = FastAPI()


@app.get("/", name='Home')
def read_root():
    return {"message": "Hello"}


if __name__ == '__main__':
    uvicorn.run(app="main:app", reload=True)
