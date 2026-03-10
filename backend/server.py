import os
import json
import httpx
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables from .env file
load_dotenv()

app = FastAPI()

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration
GEMINI_KEY = os.getenv("GEMINI_API_KEY")
OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
MODEL = "phi3" # Fallback Ollama model

if GEMINI_KEY:
    genai.configure(api_key=GEMINI_KEY)
    print("--- SYSTEM: Using Google Gemini API ---")
else:
    print("--- SYSTEM: Gemini Key not found. Using Local Ollama ---")

class PromptRequest(BaseModel):
    system: str
    prompt: str

async def stream_gemini(system_prompt, user_prompt):
    model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=system_prompt)
    response = model.generate_content(user_prompt, stream=True)
    for chunk in response:
        if chunk.text:
            yield chunk.text

async def stream_ollama(system_prompt, user_prompt):
    full_prompt = f"{system_prompt}\n\nUser: {user_prompt}\nAssistant:"
    payload = {
        "model": MODEL,
        "prompt": full_prompt,
        "stream": True
    }
    async with httpx.AsyncClient(timeout=60.0) as client:
        async with client.stream("POST", OLLAMA_URL, json=payload) as response:
            if response.status_code != 200:
                raise HTTPException(status_code=500, detail="Ollama Error")
            async for line in response.aiter_lines():
                if line:
                    data = json.loads(line)
                    yield data.get("response", "")
                    if data.get("done"):
                        break

@app.post("/generate")
async def generate(request: PromptRequest):
    try:
        if GEMINI_KEY:
            return StreamingResponse(stream_gemini(request.system, request.prompt), media_type="text/plain")
        else:
            return StreamingResponse(stream_ollama(request.system, request.prompt), media_type="text/plain")
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health():
    return {"status": "ok", "mode": "Gemini" if GEMINI_KEY else "Ollama"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
