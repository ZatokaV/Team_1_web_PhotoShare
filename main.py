import uvicorn
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy import text
from sqlalchemy.orm import Session

from src.database.connect import get_db
from src.routes import auth, posts, users, transform_posts, rates, comments, search
from src.services.messages_templates import DB_CONFIG_ERROR, DB_CONNECT_ERROR, WELCOME_MESSAGE

app = FastAPI()


@app.get("/api/healthchecker")
def healthchecker(db: Session = Depends(get_db)):
    try:
        result = db.execute(text("SELECT 1")).fetchone()
        if result is None:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=DB_CONFIG_ERROR)
        return {"message": WELCOME_MESSAGE}
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=DB_CONNECT_ERROR)


@app.get("/", name='Home')
def read_root():
    return {"message": "Hello"}


app.include_router(auth.router, prefix='/api')
app.include_router(posts.router, prefix='/api')
app.include_router(users.router, prefix='/api')
app.include_router(transform_posts.router, prefix='/api')
app.include_router(rates.router, prefix='/api')
app.include_router(search.router, prefix='/api')
app.include_router(comments.router, prefix='/api')

if __name__ == '__main__':
    uvicorn.run(app="main:app", reload=True)
