import urllib.request, json

def qwen(prompt, system="Eres un asistente de marketing B2B para ORQUOR. Responde en español, tono profesional y técnico. Sin florituras."):
    data = json.dumps({"model":"qwen2.5:7b", "prompt":f"{system}\n\n{prompt}", "stream":False}).encode()
    req = urllib.request.Request("http://localhost:11434/api/generate", data=data, headers={"Content-Type":"application/json"})
    with urllib.request.urlopen(req, timeout=180) as r:
        return json.loads(r.read()).get("response","")

tasks = [
    ("BLOG_POST", "Escribe un post de blog de 300 palabras sobre por que la traduccion medica con IA necesita verificacion auditoria (ACTO). Titulo sugerido: 'Mas alla de la traduccion: por que cada output medico necesita un verifier'."),
    ("LINKEDIN_DRAFT", "Escribe un post de LinkedIn (800 chars max) sobre la importancia de la infraestructura de agentes autonomos verificables en healthcare. Incluye un llamado a la accion para seguir a ORQUOR."),
    ("FAQ", "Genera 5 preguntas frecuentes (FAQ) sobre interpretacion medica con IA, con respuestas cortas de 2-3 oraciones cada una. Las preguntas deben ser las que haria un hospital considerando comprar ORQUOR Clinical."),
]

for task_type, prompt in tasks:
    print(f"\n{'='*50}")
    print(f"QWEN generando: {task_type}")
    print(f"{'='*50}")
    result = qwen(prompt)
    print(result[:600])
    print("...")

print("\n✅ Qwen completó 3 tareas de contenido.")
