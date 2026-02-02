from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from app.services.agent import ask_agent
from contextlib import asynccontextmanager
from app.services.agent import create_github_agent
from dotenv import load_dotenv
load_dotenv(".env")
GITHUB_AGENT = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    #initializing the agent one time for application use
    GITHUB_AGENT = await create_github_agent()
    yield

app = FastAPI(title="Github Agent", lifespan=lifespan)

class ChatRequest(BaseModel):
    message: str
    session_id: str

@app.post("/chat")
def chat_endpoint(request: ChatRequest):
    #using session id as thread id
    response = ask_agent(request.message, request.session_id, GITHUB_AGENT)
    return {"reply": response}

#serving UI
app.mount("/", StaticFiles(directory="app/static", html=True), name="static")
