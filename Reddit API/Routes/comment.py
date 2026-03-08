from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.orm import Session
from Engines import schemas, models, database, oauth2, rate_limiter

router= APIRouter(tags=["Comment"])
get_db= database.get_db
get_current_user= oauth2.get_current_user
rate_limit_user= rate_limiter.token_bucket_rate_limit

@router.post("/post/{post_id}/comments") #id is post id
def create_comment(post_id: int, request: schemas.Comment, db: Session= Depends(get_db), current_user: models.Users= Depends(get_current_user)):

    key = f"tokenbucket:create_comment:user:{current_user.id}:post:{post_id}"

    allowed = rate_limit_user(key=key, capacity=1, refill_rate=0.2)

    if not allowed:
        raise HTTPException(
            status_code=429,
            detail="Too many posts. Slow down."
        )

    comment= models.Comments(content=request.content, user_id= current_user.id, post_id=post_id, parent_id= request.parent_id or None)
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment

@router.get("/post/{post_id}/comments")
def get_comment(post_id: int, db: Session = Depends(get_db)):
    comments = db.query(models.Comments).filter(
        models.Comments.post_id == post_id,
        models.Comments.parent_id.is_(None)
    ).all()

    return comments

@router.get("/post/{post_id}/comments/{c_id}")
def get_replies(post_id: int, c_id: int, db: Session = Depends(get_db)):
    replies = db.query(models.Comments).filter(models.Comments.post_id == post_id, models.Comments.parent_id == c_id).all()
    return replies

@router.delete("/post/{post_id}/comments/{c_id}", status_code=status.HTTP_204_NO_CONTENT) #id is post id
def del_comment(post_id: int, c_id: int, db: Session= Depends(get_db), current_user: models.Users= Depends(get_current_user)):
    comment= db.query(models.Comments).filter(models.Comments.post_id == post_id, models.Comments.id == c_id).first()
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Comment with id {c_id} not found")
    db.delete(comment)
    db.commit()