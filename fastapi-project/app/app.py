from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException

from app.db import create_db_and_tables
from app.schemas import PostCreate, PostResponse


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield

app = FastAPI()

text_posts = {
    1: {"title": "New Post", "content": "Cool test post"},
    2: {"title": "Python Tricks", "content": "List comprehensions make loops shorter and cleaner."},
    3: {"title": "Linux Life", "content": "Learning terminal shortcuts makes you feel like a hacker."},
    4: {"title": "Tech News", "content": "AI models keep getting faster and more efficient every year."},
    5: {"title": "Gaming Vibes", "content": "Finally hit 120 FPS on my favorite shooter!"},
    6: {"title": "Ubuntu Setup", "content": "Installed new drivers and performance feels smoother."},
    7: {"title": "Coffee Time", "content": "Coding at 2 AM with a fresh espresso — pure bliss."},
    8: {"title": "Coding Goals", "content": "Building a personal portfolio site using Flask."},
    9: {"title": "Bug Hunt", "content": "Spent an hour fixing a missing comma. Classic."},
    10: {"title": "Random Thought", "content": "Dark mode makes everything 10x cooler."},
    11: {"title": "Weekend Plans", "content": "Trying out a new Linux distro just for fun."},
}

@app.get("/posts")
def get_all_posts(limit: int = None):
    if limit:
        return list(text_posts.values())[:limit]
    return text_posts

@app.get("/posts/{post_id}")
def get_single_post(post_id: int) -> PostResponse:
    if post_id not in text_posts:
        raise HTTPException(status_code=404, detail="Post not found",)
    return text_posts.get(post_id)

@app.post("/posts")
def create_post(post: PostCreate) -> PostResponse:
    new_post = {"title": post.title, "content": post.content}
    text_posts[max(text_posts.keys()) + 1] = {"title": post.title, "content": post.content}
    return new_post

