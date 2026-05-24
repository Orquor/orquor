import urllib.request, json, sys, glob

def qwen(prompt, system=""):
    full = f"{system}\n\n{prompt}" if system else prompt
    data = json.dumps({"model":"qwen2.5:7b", "prompt":full, "stream":False}).encode()
    req = urllib.request.Request("http://localhost:11434/api/generate", data=data, headers={"Content-Type":"application/json"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.loads(r.read()).get("response","")

# Revisar contenido de LinkedIn
import os
base = r"C:\Users\frefe\OneDrive\Desktop\START UP\orquor\09-content-calendar\linkedin"
files = sorted(glob.glob(os.path.join(base, "*.md")))[:5]  # primeros 5

for f in files:
    name = os.path.basename(f)
    with open(f, "r", encoding="utf-8") as fh:
        content = fh.read()
    
    prompt = f"Revisa este post de LinkedIn para ORQUOR. Detecta errores ortograficos, gramaticales, o de tono. Sugiere mejoras concretas. Se breve.\n\n---\n{content[:1500]}"
    
    print(f"\n=== {name} ===")
    result = qwen(prompt, "Eres un revisor de contenido para ORQUOR, una empresa de tecnologia medica. Responde en español.")
    print(result[:400])
    print("---")
