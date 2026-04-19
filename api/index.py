from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from groq import Groq
import os

app = FastAPI()
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# Grand UI with updated prompt logic
HTML_CONTENT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Stealth.js | Industrial Humanizer</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-[#0f172a] text-slate-200 selection:bg-blue-500/30">
    <div class="max-w-6xl mx-auto px-6 py-12">
        <h1 class="text-3xl font-black italic mb-8 text-white">STEALTH<span class="text-blue-500">.JS.ORG</span></h1>
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-px bg-slate-800 rounded-3xl overflow-hidden shadow-2xl">
            <div class="bg-[#0f172a] p-8">
                <textarea id="input" class="w-full h-[400px] bg-transparent outline-none resize-none text-lg" placeholder="Paste AI text..."></textarea>
            </div>
            <div class="bg-[#111c33] p-8">
                <div id="output" class="w-full h-[400px] text-slate-400 text-lg overflow-y-auto italic">Humanized output...</div>
            </div>
        </div>
        <button onclick="process()" id="btn" class="w-full mt-8 py-5 bg-blue-600 rounded-xl font-black text-white hover:bg-blue-500 transition-all">
            BYPASS AI DETECTION (V2)
        </button>
    </div>
    <script>
        async function process() {
            const input = document.getElementById('input').value;
            const output = document.getElementById('output');
            const btn = document.getElementById('btn');
            if(!input) return;
            btn.innerText = "SCRUBBING AI FINGERPRINTS...";
            try {
                const response = await fetch('/api/humanize', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({text: input})
                });
                const data = await response.json();
                output.innerText = data.result;
                output.classList.remove('italic', 'text-slate-400');
            } catch (e) { output.innerText = "ENGINE ERROR."; }
            finally { btn.innerText = "BYPASS AI DETECTION (V2)"; }
        }
    </script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
async def serve_home():
    return HTML_CONTENT

@app.post("/api/humanize")
async def humanize(request: Request):
    try:
        data = await request.json()
        text = data.get("text", "")
        
        # AGGRESSIVE HUMANIZATION PROMPT
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are a human editor. Rewrite the input text to be casual and natural. Use contractions. Avoid 'seismic shift', 'landscape', or 'unlocking'. Use simpler words. Vary sentence length (one short, one long). Make it sound like a person explained it in a quick voice note."},
                {"role": "user", "content": f"Rewrite this to be 100% human and informal: {text}"}
            ],
            temperature=1.1 # Increased randomness
        )
        return {"result": response.choices[0].message.content}
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)
