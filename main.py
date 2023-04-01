import uvicorn
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy import text
from sqlalchemy.orm import Session

from src.database.connect import get_db
from src.services.messages_templates import DB_CONFIG_ERROR, DB_CONNECT_ERROR, WELCOME_MESSAGE
from src.routes.transform_posts import router as transform_image

app = FastAPI()

app.include_router(transform_image, prefix='/api')
@app.get("/api/healthchecker")
def healthchecker(db: Session = Depends(get_db)):
    try:
        result = db.execute(text("SELECT 1")).fetchone()
        print(result)
        if result is None:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=DB_CONFIG_ERROR)
        return {"message": WELCOME_MESSAGE}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=DB_CONNECT_ERROR)


@app.get("/", name='Home')
def read_root():
    return {"message": "Hello"}


if __name__ == '__main__':
    uvicorn.run(app="main:app", reload=True)
