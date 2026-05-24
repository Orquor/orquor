import urllib.request, json

data = json.dumps({"model":"qwen2.5:7b", "prompt":"Hola, eres el agente local de ORQUOR. Preséntate brevemente en español.", "stream":False}).encode()

req = urllib.request.Request("http://localhost:11434/api/generate", data=data, headers={"Content-Type":"application/json"})
with urllib.request.urlopen(req, timeout=60) as r:
    d = json.loads(r.read())
    print(d.get("response","")[:500])
    dur = d.get("total_duration",0)/1e9
    tok = d.get("eval_count",0)
    print(f"\n{dur:.1f}s | {tok} tokens | {tok/dur:.0f} tok/s" if dur > 0 else "")
