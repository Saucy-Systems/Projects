from fastapi import APIRouter, status, HTTPException, Depends
from Engines import database, oauth2, schemas, models
from sqlalchemy.orm import Session
from typing import List
from Engines import cache, rate_limiter
import json

router= APIRouter(tags=["Post"])
get_db= database.get_db
get_current_user= oauth2.get_current_user
redis_client= cache.redis_client
rate_limit_user= rate_limiter.token_bucket_rate_limit

@router.post("/community/{id}/post", response_model=schemas.post_response)
def create_post(id: int,request: schemas.post, db: Session= Depends(get_db), current_user: models.Users= Depends(get_current_user)):

    key = f"tokenbucket:create_post:user:{current_user.id}"

    allowed = rate_limit_user(key=key, capacity=5, refill_rate=0.2)

    if not allowed:
        raise HTTPException(
            status_code=429,
            detail="Too many posts. Slow down."
        )

    post= models.Posts(title= request.title, body= request.body, user_id= current_user.id, community_id= id)
    db.add(post)
    db.commit()
    db.refresh(post)
    return post

@router.delete("/community/{id}/post/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, post_id: int, db: Session= Depends(get_db), current_user: models.Users= Depends(get_current_user)):
    
    post= db.query(models.Posts).filter(models.Posts.id == post_id, models.Posts.community_id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {post_id} not found")
    
    member= db.query(models.CommunityMembers).filter(models.CommunityMembers.user_id == current_user.id, models.CommunityMembers.community_id == id).first()
    if not member:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not a member of this community")

    if post.user_id == current_user.id or member.role in ["Moderator", "Owner"]:
        db.delete(post)
        db.commit()

        cache_key= f"post:{id}:{post_id}"
        redis_client.delete(cache_key)
        
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have permission to delete this post")
    
@router.put("/community/{id}/post/{post_id}", response_model=schemas.post_response)
def update_post(id: int, request: schemas.post, post_id: int, db: Session= Depends(get_db), current_user: models.Users= Depends(get_current_user)):
    
    post= db.query(models.Posts).filter(models.Posts.id == post_id, models.Posts.user_id == current_user.id, models.Posts.community_id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {post_id} not found")

    post.title= request.title
    post.body= request.body
    db.commit()
    db.refresh(post)

    cache_key= f"post:{id}:{post_id}"
    redis_client.delete(cache_key) # REDIS CLIENT IS SAFE EVEN IF CACHE DOESNT EXIST
    
    return post

@router.get("/community/{id}/post/{post_id}", response_model=schemas.post_response)
def get_post(id: int, post_id: int, db: Session= Depends(get_db), current_user: models.Users= Depends(get_current_user)):

        
    cache_key= f"post:{id}:{post_id}"
    cached_post= redis_client.get(cache_key)
    if cached_post:
        return json.loads(cached_post)
    
    post= db.query(models.Posts).filter(models.Posts.id == post_id, models.Posts.user_id == current_user.id, models.Posts.community_id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {post_id} not found")
    
    redis_client.setex(
        cache_key,
        60,   # TTL → 60 seconds
        json.dumps({
            "title": post.title,
            "body": post.body,
            "creator": {"name": post.creator.name,"email": post.creator.email}
            })
        )
    return post

@router.get("/community/{id}/post",response_model=List[schemas.post_response])
def get_all(id: int, db: Session= Depends(get_db), current_user: models.Users= Depends(get_current_user)):
    post= db.query(models.Posts).filter(models.Posts.user_id == current_user.id).all()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Posts not found")
    return post