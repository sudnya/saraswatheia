# main.py
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
import mm_embedder.models.token as token
from fastapi.middleware.cors import CORSMiddleware
from mm_embedder.database.database import Base, engine, SessionLocal

API_BASE = "/api/v0"

app = FastAPI()

# Dependency to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

'''
@app.post(API_BASE+"/token")
def create_token(item: tokens.Tokens, db: Session = Depends(get_db)):
    db_item = tokens.Tokens(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    #return db_item
    return {"message": "Student created successfully"}

@app.get(API_BASE+"/token/{token_id}")
def read_items(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(tokens.Tokens).offset(skip).limit(limit).all()
'''

@app.post(API_BASE+"/token")
async def create_token(user_token: token.Token, db: Session = Depends(get_db)):
    #db_item = token.Tokens(**token.dict())
    print(user_token.dict())
    # Create entry in database
    db_item = token.TokenDB(**user_token.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return {f"message": "Token created successfully {db_item}"}


Base.metadata.create_all(bind=engine)
# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)