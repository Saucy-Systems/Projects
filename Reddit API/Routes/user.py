from fastapi import APIRouter, status, HTTPException, Depends
from Engines import database, oauth2, schemas, models, hashing
from sqlalchemy.orm import Session

router= APIRouter(tags=["User"])
get_db= database.get_db
get_current_user= oauth2.get_current_user

@router.post("/user",response_model=schemas.user_response)
def create_user(request: schemas.user, db: Session= Depends(get_db)):
    password= hashing.Hash.hash(request.password)
    user= models.Users(name= request.name, email= request.email, password=password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.get("/user", response_model=schemas.all_posts_user)
def get_user(id: int, db: Session= Depends(get_db)):
    user= db.query(models.Users).filter(models.Users.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    return user