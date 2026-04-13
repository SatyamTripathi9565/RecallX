from fastapi import UploadFile, File
from fastapi import FastAPI
from database import memory_collection, recording_collection
from pydantic import BaseModel


app = FastAPI()

# =========================
# ✅ Pydantic Model
# =========================
class MemoryInput(BaseModel):
    text: str


# =========================
# 🏠 HOME
# =========================
@app.get("/")
def home():
    return {"message": "Server running 🚀"}


# =========================
# ➕ ADD MEMORY
# =========================
@app.post("/add")
def add_memory(data: MemoryInput):
    memory_collection.insert_one({
        "content": data.text
    })
    return {"message": "Saved ✅"}


# =========================
# 📋 GET ALL MEMORIES
# =========================
@app.get("/memories")
def all_memories():
    memories = list(memory_collection.find({}, {"_id": 0}))
    return memories


# =========================
# 🔍 SEARCH
# =========================
@app.get("/search")
def search(query: str):
    memories = list(memory_collection.find({}, {"_id": 0}))

    results = [
        m for m in memories
        if query.lower() in m["content"].lower()
    ]

    return results


# =========================
# ❌ DELETE MEMORY
# =========================
@app.delete("/delete/{content}")
def delete_memory(content: str):
    memory_collection.delete_one({"content": content})
    return {"message": "Deleted ✅"}



@app.post("/upload_recording")
async def upload_recording(file: UploadFile = File(...)):
    content = await file.read()

    recording_collection.insert_one({
        "filename": file.filename,
        "data": content
    })

    return {"message": "Recording saved 🎥"}