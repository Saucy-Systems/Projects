from fastapi import FastAPI
from Engines import database
from Routes import authentication, post, user, likes, comment, community

app = FastAPI()

app.include_router(authentication.router)
app.include_router(post.router)
app.include_router(user.router)
app.include_router(comment.router)
app.include_router(likes.router)
app.include_router(community.router)

database.Base.metadata.create_all(database.engine)