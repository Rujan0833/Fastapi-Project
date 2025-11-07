import asyncio # Crucial import for running the async setup function
import os
from collections.abc import AsyncGenerator
import uuid

# --- SQLAlchemy Imports ---
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy import Column, String, Text, DateTime
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime


# Connecting to a DB
DATABASE_URL = "sqlite+aiosqlite:///./test.db"

class Base(DeclarativeBase):
    pass

"""
This class defines the database schema for storing user-submitted posts 
(e.g., images or videos), including file metadata and creation timestamp.
"""
class Post(Base):
    __tablename__ = "posts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    caption = Column(Text)
    url = Column(String,nullable=False)
    file_type = Column(String,nullable=False)
    file_name = Column(String,nullable=False)
    created_at = Column(DateTime,default=datetime.utcnow)

# Set up the asynchronous database connection engine.
engine = create_async_engine(DATABASE_URL, future=True, echo=True)

# Factory to create new transactional database sessions.
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

# creates all the tables for DB by starting the engine
async def create_db_and_tables():
    async with engine.begin() as conn:
        # run_sync is necessary because create_all is a synchronous SQLAlchemy operation
        await conn.run_sync(Base.metadata.create_all)

# get a session that allow us access the DB and write and read asynchronously
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session

if __name__ == "__main__":
    # This block executes the async function when you run the script via: python your_file_name.py
    print("Attempting to create database tables...")
    asyncio.run(create_db_and_tables())
    print("Database setup complete.")