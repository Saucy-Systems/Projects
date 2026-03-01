from Engines import database
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

Base= database.Base

class Posts(Base):
    __tablename__= "Posts"
    id= Column(Integer, primary_key=True, index=True)
    title= Column(String)
    body= Column(String)
    user_id= Column(Integer, ForeignKey("Users.id"))

    creator= relationship("Users", back_populates="posts")
    comments= relationship("Comments", back_populates="post", cascade="all, delete")
    likes= relationship("Likes", back_populates="post", cascade="all, delete")
     
    community_id= Column(Integer, ForeignKey("Communities.id")) 
    community= relationship("Community", back_populates="posts")


class Users(Base):
    __tablename__= "Users"
    id= Column(Integer, primary_key=True, index=True)
    name= Column(String)
    email= Column(String)
    password= Column(String)

    posts= relationship("Posts", back_populates="creator")
    comments= relationship("Comments", back_populates="user", cascade="all, delete")
    likes= relationship("Likes", back_populates="user", cascade="all, delete")
    communities= relationship("CommunityMembers", back_populates="user")

class Comments(Base):
    __tablename__ = "Comments"
    id= Column(Integer, primary_key=True, index=True)
    content= Column(String, nullable=False)
    user_id= Column(Integer, ForeignKey("Users.id"))
    post_id= Column(Integer, ForeignKey("Posts.id"))
    parent_id= Column(Integer, ForeignKey("Comments.id"), nullable=True)

    user= relationship("Users", back_populates="comments")
    post= relationship("Posts", back_populates="comments")
    
    parent = relationship("Comments", remote_side=[id], back_populates="replies")
    replies = relationship("Comments", back_populates="parent")

class Likes(Base):
    __tablename__= "Likes"
    user_id= Column(Integer, ForeignKey("Users.id"), primary_key=True)
    post_id= Column(Integer, ForeignKey("Posts.id"), primary_key=True)
    user= relationship("Users", back_populates="likes")
    post= relationship("Posts", back_populates="likes")

class Community(Base):
    __tablename__ = "Communities"
    id= Column(Integer, primary_key=True, index=True)
    name= Column(String, unique=True, nullable=False)
    description= Column(String)
    owner_id= Column(Integer, ForeignKey("Users.id"))
    owner = relationship("Users")
    members= relationship("CommunityMembers", back_populates="community", cascade="all, delete")
    posts= relationship("Posts", back_populates="community", cascade="all, delete")

class CommunityMembers(Base):
    __tablename__ = "CommunityMembers"
    id= Column(Integer, primary_key=True, index=True)
    user_id= Column(Integer,  ForeignKey("Users.id"))
    community_id= Column(Integer, ForeignKey("Communities.id"))

    role= Column(String, default="member")
    total_posts= Column(Integer, default=0)
    contribution_score= Column(Integer, default=0)

    community= relationship("Community", back_populates="members")
    user= relationship("Users", back_populates="communities")
    