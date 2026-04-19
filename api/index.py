from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from groq import Groq
import os

app = FastAPI()
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# Grand UI embedded directly to prevent path errors
HTML_CONTENT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Stealth.js | Industrial Humanizer</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-[#0f172a] text-slate-200 font-sans selection:bg-blue-500/30">
    <div class="max-w-6xl mx-auto px-6 py-12">
        <div class="flex flex-col md:flex-row justify-between items-center mb-12 border-b border-slate-800 pb-8">
            <div>
                <h1 class="text-3xl font-black tracking-tighter text-white italic">STEALTH<span class="text-blue-500">.JS.ORG</span></h1>
                <p class="text-slate-500 text-sm font-medium uppercase">Industrial Grade Humanizer</p>
            </div>
        </div>
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-px bg-slate-800 border border-slate-800 rounded-3xl overflow-hidden shadow-2xl">
            <div class="bg-[#0f172a] p-8">
                <textarea id="input" class="w-full h-[400px] bg-transparent text-slate-300 outline-none resize-none text-lg" placeholder="Paste AI text here..."></textarea>
            </div>
            <div class="bg-[#111c33] p-8">
                <div id="output" class="w-full h-[400px] text-slate-400 text-lg overflow-y-auto italic">Humanized output will appear here...</div>
            </div>
        </div>
        <button onclick="process()" id="btn" class="w-full mt-8 py-5 bg-blue-600 rounded-xl font-black text-white hover:bg-blue-500 shadow-xl transition-all">
            BYPASS AI DETECTION
        </button>
    </div>
    <script>
        async function process() {
            const input = document.getElementById('input').value;
            const output = document.getElementById('output');
            const btn = document.getElementById('btn');
            if(!input) return;
            btn.innerText = "RUNNING STEALTH PROTOCOLS...";
            try {
                const response = await fetch('/api/humanize', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({text: input})
                });
                const data = await response.json();
                output.innerText = data.result || "Error processing.";
                output.classList.remove('italic', 'text-slate-400');
                output.classList.add('text-slate-200');
            } catch (e) {
                output.innerText = "CORE ENGINE ERROR.";
            } finally {
                btn.innerText = "BYPASS AI DETECTION";
            }
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
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are a professional human rewriter. Output only the humanized text with natural rhythm."},
                {"role": "user", "content": text}
            ],
            temperature=0.9
        )
        return {"result": response.choices[0].message.content}
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)
