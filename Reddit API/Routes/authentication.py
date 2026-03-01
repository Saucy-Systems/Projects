from Engines import models, database, jwt_token, hashing
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

router= APIRouter(tags=["Authentication"])
get_db= database.get_db

@router.post("/login")
def login(request: OAuth2PasswordRequestForm= Depends(), db: Session= Depends(get_db)):
  user= db.query(models.Users).filter(models.Users.email == request.username).first()
  
  if not user:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials")
    
  if not hashing.Hash.verify(user.password,request.password):
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Incorrect Password")
  
  access_token= jwt_token.create_access_token(data={"sub": user.email})
  return {"access_token": access_token, "type": "bearer"}