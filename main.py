from fastapi import FastAPI, HTTPException
import requests
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
#initialize app
app = FastAPI()
#request can be taekn from here
class AgentCreateRequest(BaseModel):
    provider: str
    agent_name: str
    description: str
    voice: str

VAPI_API_KEY = "80379222-af58-4a71-8159-5cb59bbb517b"
RETELL_API_KEY = "key_01d8e1c05936f502425881514291"
#the agent for user i/p
@app.post("/create-agent")
def create_agent(request: AgentCreateRequest):
    if request.provider.lower() == "vapi":
        return create_vapi_agent(request)
    elif request.provider.lower() == "retell":
        return create_retell_agent(request)
    else:
        raise HTTPException(status_code=400, detail="Invalid provider specified")

def create_vapi_agent(request: AgentCreateRequest):
    url = "https://api.vapi.ai/assistants"
    headers = {
        "Authorization": f"Bearer {VAPI_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "name": request.agent_name,
        "description": request.description,
        "voice": request.voice,
        "transcription_provider": "deepgram"
    }
    response = requests.post(url, json=data, headers=headers)
    if response.status_code != 201:
        raise HTTPException(status_code=response.status_code, detail=response.text)
    return response.json()

def create_retell_agent(request: AgentCreateRequest):
    url = "https://api.retellai.com/agents"
    headers = {
        "Authorization": f"Bearer {RETELL_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "name": request.agent_name,
        "voice_id": request.voice,
        "model": "gpt-3.5-turbo",
        "description": request.description,
    }
    response = requests.post(url, json=data, headers=headers)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)
    return response.json()
