# main.py

# 1. Import the database creation function
from app.db import create_db_and_tables # Adjust the import path if needed (e.g., from db_setup import ...)

from fastapi import FastAPI
import uvicorn

# Initialize your FastAPI app
app = FastAPI()

# 2. Register the function to run at startup
@app.on_event("startup")
async def startup_event():
    # Await the function call to ensure tables are created before the server accepts requests
    await create_db_and_tables()
    print("Database tables checked/created.")

# ... Define your routes here ...

# You can keep the uvicorn execution block, but uv run handles this:
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)