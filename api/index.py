from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from groq import Groq
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# SECURE: Look for key in environment variables
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

@app.get("/")
async def serve_home():
    return FileResponse('public/index.html')

@app.post("/api/humanize")
async def humanize(request: Request):
    try:
        data = await request.json()
        text = data.get("text", "")
        if not text:
            return JSONResponse({"result": "No text provided."})

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are a professional human rewriter. Output only the humanized text."},
                {"role": "user", "content": text}
            ],
            temperature=0.85
        )
        return {"result": response.choices[0].message.content}
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)
