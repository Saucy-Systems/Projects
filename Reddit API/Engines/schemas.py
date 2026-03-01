from pydantic import BaseModel
from typing import Optional, List
from pydantic import BaseModel

class post(BaseModel):
    title: str
    body: str

class post_user(post):
   class Config:
      orm_mode= True

class user(BaseModel):
    name: str
    email: str
    password: str

class user_response(BaseModel):
   name: str
   email: str
   class Config:
      orm_mode= True

class all_posts_user(BaseModel):
   name: str
   email: str
   posts: List[post_user] = []
   class Config:
      orm_mode=True

class post_response(BaseModel):
   title: str
   body: str
   creator: user_response
   class Config:
      orm_mode= True

class Login(BaseModel):
   username: str
   password: str

class Token(BaseModel):
   access_type: str
   token_type: str

class TokenData(BaseModel):
   email: Optional[str]= None

class Comment(BaseModel):
    content: str
    parent_id: Optional[int] = None

class CommentResponse(BaseModel):
    id: int
    content: str
    replies: List["CommentResponse"] = []

    class Config:
        orm_mode = True

class Community(BaseModel):
   name: str
   description: str

class CommunityResponse(BaseModel):
   id: int
   name: str
   description: str
   class Config:
      orm_mode= True

