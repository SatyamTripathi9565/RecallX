from fastapi import FastAPI, Depends, BackgroundTasks
from pydantic import BaseModel
from sqlalchemy.orm import Session
from fastapi.staticfiles import StaticFiles

from backend.database import SessionLocal, engine
from backend.models import Base, Memory
from backend.ai_engine import summarize_text, generate_answer, text_to_speech

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# 🔥 Serve media (for audio)
app.mount("/media", StaticFiles(directory="media"), name="media")


# =========================
# ✅ Pydantic Model
# =========================
class MemoryInput(BaseModel):
    text: str


# =========================
# ✅ DB Dependency
# =========================
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# =========================
# 🔥 Background Processing
# =========================
def process_memory(mem_id: int, text: str):
    db = SessionLocal()

    try:
        mem = db.query(Memory).filter(Memory.id == mem_id).first()

        if mem:
            mem.summary = summarize_text(text)
            db.commit()

    finally:
        db.close()


# =========================
# ✅ ADD MEMORY (FAST)
# =========================
@app.post("/add")
def add_memory(data: MemoryInput, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):

    # 🔥 Instant save
    mem = Memory(
        content=data.text,
        summary="processing...",
        embedding="",
        tags=""
    )

    db.add(mem)
    db.commit()
    db.refresh(mem)

    # 🔥 Background processing
    background_tasks.add_task(process_memory, mem.id, data.text)

    return {"message": "Saved successfully ✅"}


# =========================
# 💬 CHAT API
# =========================
@app.post("/chat")
def chat(query: str, output_type: str = "text", db: Session = Depends(get_db)):

    memories = db.query(Memory).all()

    # 🔥 Simple context (fast)
    context = "\n".join([m.content for m in memories[:5]])

    answer = generate_answer(query, context)

    response = {
        "answer": answer
    }

    # 🔊 Optional audio
    if output_type == "audio":
        audio_path = text_to_speech(answer)
        response["audio"] = audio_path

    return response


# =========================
# 📋 GET ALL MEMORIES
# =========================
@app.get("/memories")
def all_memories(db: Session = Depends(get_db)):
    memories = db.query(Memory).all()

    return [
        {
            "content": m.content,
            "summary": m.summary
        }
        for m in memories
    ]