import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Step 1: Get project root directory (RecallX)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Step 2: Create full path for database file
db_path = os.path.join(BASE_DIR, "data", "memory.db")

# Step 3: Create engine
engine = create_engine(f"sqlite:///{db_path}", connect_args={"check_same_thread": False})

# Step 4: Create session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Step 5: Base class
Base = declarative_base()
