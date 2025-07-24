from fastapi import FastAPI, Query
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from .db_faiss import NovelDB

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

db = NovelDB("../data/novels.json")

class SearchResult(BaseModel):
    id: str
    title: str
    intro: str
    url: str
    score: float

@app.get("/search", response_model=list[SearchResult])
def search(q: str = Query(..., description="검색어 문장"), top_k: int = 5):
    return db.search(q, top_k=top_k) 