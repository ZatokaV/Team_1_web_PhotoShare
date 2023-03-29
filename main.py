import uvicorn
from fastapi import FastAPI

app = FastAPI()


@app.get("/", name='Home')
def read_root():
    """
    The read_root function returns a dictionary with the key &quot;message&quot; and value &quot;Hello&quot;.
    :return: A dictionary
    """
    return {"message": "Hello"}


if __name__ == '__main__':
    uvicorn.run(app="main:app", reload=True)
