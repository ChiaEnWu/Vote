from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 先開放全部，作業很方便
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 假資料：投票候選人與票數
votes = {
    "A": 0,
    "B": 0,
    "C": 0
}

class VoteRequest(BaseModel):
    candidate: str


@app.get("/")
def hello():
    return {"message": "Welcome to the Voting API"}


@app.get("/results")
def get_results():
    return votes


@app.post("/vote")
def vote(data: VoteRequest):
    candidate = data.candidate.upper()

    if candidate not in votes:
        return {"error": "Candidate does not exist"}

    votes[candidate] += 1
    return {"message": f"Vote recorded for {candidate}", "current_votes": votes[candidate]}


@app.post("/reset")
def reset_votes():
    for key in votes:
        votes[key] = 0
    return {"message": "All votes reset to 0", "results": votes}
