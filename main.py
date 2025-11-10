import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from bson.objectid import ObjectId

from database import db, create_document, get_documents
from schemas import Question, InterviewTemplate, Interview

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "Interview Builder API"}


@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }
    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️ Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️ Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"
    return response


# --------- Question Endpoints ---------
@app.post("/api/questions", response_model=dict)
def create_question(payload: Question):
    inserted_id = create_document("question", payload)
    return {"id": inserted_id}


@app.get("/api/questions", response_model=List[dict])
def list_questions(category: Optional[str] = None, difficulty: Optional[str] = None, role: Optional[str] = None, q: Optional[str] = None, limit: int = 100):
    filter_dict = {}
    if category:
        filter_dict["category"] = category
    if difficulty:
        filter_dict["difficulty"] = difficulty
    if role:
        filter_dict["role"] = role
    if q:
        filter_dict["$or"] = [
            {"text": {"$regex": q, "$options": "i"}},
            {"tags": {"$elemMatch": {"$regex": q, "$options": "i"}}}
        ]
    docs = get_documents("question", filter_dict, limit)
    # Convert ObjectId
    for d in docs:
        d["id"] = str(d.pop("_id", ""))
    return docs


# --------- Interview Template Endpoints ---------
@app.post("/api/templates", response_model=dict)
def create_template(payload: InterviewTemplate):
    inserted_id = create_document("interviewtemplate", payload)
    return {"id": inserted_id}


@app.get("/api/templates", response_model=List[dict])
def list_templates(role: Optional[str] = None, seniority: Optional[str] = None, limit: int = 100):
    filter_dict = {}
    if role:
        filter_dict["role"] = role
    if seniority:
        filter_dict["seniority"] = seniority
    docs = get_documents("interviewtemplate", filter_dict, limit)
    for d in docs:
        d["id"] = str(d.pop("_id", ""))
    return docs


# --------- Interview Endpoints ---------
@app.post("/api/interviews", response_model=dict)
def create_interview(payload: Interview):
    # If a template is selected but no explicit questions provided, expand later on the client
    inserted_id = create_document("interview", payload)
    return {"id": inserted_id}


@app.get("/api/interviews", response_model=List[dict])
def list_interviews(limit: int = 100):
    docs = get_documents("interview", {}, limit)
    for d in docs:
        d["id"] = str(d.pop("_id", ""))
    return docs


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
