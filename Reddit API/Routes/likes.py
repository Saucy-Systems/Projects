from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.orm import Session
from Engines import database, models, oauth2, cache
import json

router= APIRouter(tags=["Like"])
get_db= database.get_db
get_current_user= oauth2.get_current_user
redis_client= cache.redis_client

@router.post("/post/{post_id}/likes")
def like(post_id: int, db: Session= Depends(get_db), current_user: models.Users= Depends(get_current_user)):
    like= db.query(models.Likes).filter(models.Likes.post_id == post_id, models.Likes.user_id == current_user.id).first()
    if like:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Post is already Liked")
    new_like= models.Likes(post_id= post_id, user_id= current_user.id)
    db.add(new_like)
    db.commit()
    db.refresh(new_like)
    
    cache_key= f"Likes:{post_id}"
    redis_client.delete(cache_key)
    
    return {"message":"Post is liked"}

@router.delete("/posts/{post_id}/likes")
def unlike(post_id: int, db: Session= Depends(get_db), current_user: models.Users= Depends(get_current_user)):
    like= db.query(models.Likes).filter(models.Likes.post_id == post_id, models.Likes.user_id == current_user.id).first()
    if not like:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Like not found")
    db.delete(like)
    db.commit()

    cache_key= f"Likes:{post_id}"
    redis_client.delete(cache_key)

    return {"message":"Post is unliked"}

@router.get("/post/{post_id}/likes/count")
def get_likes(post_id: int, db: Session= Depends(get_db)):

    cache_key= f"Likes:{post_id}"
    cache_likes= redis_client.get(cache_key)
    if cache_likes:
        return json.loads(cache_likes)

    likes_count= db.query(models.Likes).filter(models.Likes.post_id == post_id).count()

    redis_client.setex(cache_key, 50, json.dumps({"likes":likes_count})
    )
    
    return {"likes":likes_count}