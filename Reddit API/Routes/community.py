from fastapi import APIRouter, status, HTTPException, Depends
from Engines import schemas, models, database, oauth2
from sqlalchemy.orm import Session

router= APIRouter(tags=["Community"])

get_db= database.get_db
get_current_user= oauth2.get_current_user

@router.post("/community", response_model=schemas.CommunityResponse)
def create_community(request: schemas.Community, db: Session= Depends(get_db), current_user: models.Users= Depends(get_current_user)):
    community= models.Community(name= request.name, description= request.description, owner_id= current_user.id)
    db.add(community)
    db.commit()
    db.refresh(community)
    owner= models.CommunityMembers(user_id= current_user.id, community_id=community.id, role="Owner" )
    db.add(owner)
    db.commit()
    db.refresh(owner)
    return community

@router.post("/community/{id}/join")
def join_community(id:int, db: Session= Depends(get_db), current_user: models.Users= Depends(get_current_user)):
    member= models.CommunityMembers(user_id= current_user.id, community_id=id )
    db.add(member)
    db.commit()
    db.refresh(member)
    return member

@router.put("/community/{id}/update")
def update(request: schemas.Community,id:int, db: Session= Depends(get_db), current_user: models.Users= Depends(get_current_user)):

    community= db.query(models.Community).filter(models.Community.id == id).first()
    if not community:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Community not found")
    if current_user.id == community.owner_id:
        community.name= request.name
        community.description= request.description
        db.commit()
        db.refresh(community)
        return community
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not Allowed for this action")
    
@router.delete("/community/{id}/delete", status_code=status.HTTP_204_NO_CONTENT)
def destroy(id: int, db: Session = Depends(get_db), current_user: models.Users = Depends(get_current_user)):
    community = db.query(models.Community).filter(models.Community.id == id).first()

    if not community:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Community not found")

    if current_user.id != community.owner_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not allowed for this action")

    db.delete(community)
    db.commit()

@router.put("/community/{id}/promote/{user_id}")
def promote(user_id: int, id: int, db: Session = Depends(get_db), current_user: models.Users = Depends(get_current_user)):
    community= db.query(models.Community).filter(models.Community.id == id).first()
    if not community:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Community not found")
    if current_user.id != community.owner_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not allowed for this action")
    promote_user= db.query(models.CommunityMembers).filter(models.CommunityMembers.user_id == user_id, models.CommunityMembers.community_id == id).first()
    promote_user.role = "Moderator"
    db.commit()
    db.refresh(promote_user)
    return promote_user
    