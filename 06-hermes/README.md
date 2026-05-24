# Orquor Hermes — Multi-Agent Orchestration Bootstrap

Implementación inicial de los 6 sub-agentes HERMES descritos en el Canvas `orquor-hermes-arquitectura.canvas.tsx`. Diseñados para operar Orquor con headcount mínimo (1–4 humanos) mientras los sub-agentes manejan operaciones rutinarias supervisadas.

## Arquitectura

```
hermes/
├── orchestrator.py            # Coordinador central
├── shared_memory.py           # MEMORY.md compartida + persistence
├── sub_agents/
│   ├── ops_monitor_bot.py     # Sprint 1 — observabilidad (DEPENDENCIA DE TODOS)
│   ├── watchtower_bot.py      # OSINT continuo (Capa Negra)
│   ├── recruiter_bot.py       # Pipeline de intérpretes certificados
│   ├── sales_bot.py           # Cultivación de assets B2B
│   ├── compliance_watcher_bot.py  # HIPAA, Ley 29733, LGPD monitoring
│   └── content_bot.py         # Distribución de contenido multicanal
├── verifiers/
│   ├── translation_verifiers.py   # Verifiers outcome-based para Orquor Clinical
│   └── shared_verifiers.py        # Verifiers comunes (auth, audit, format)
├── memory/
│   ├── MEMORY.md              # Memoria persistente compartida
│   └── lessons_learned.md     # Cross-task patterns
└── requirements.txt
```

## Filosofía de diseño

Adaptado directamente de la disciplina OpenClaw Atlas de Freddy:

1. **Outcome-based verifiers**: cada sub-agente entrega outputs verificados por pytest antes de comprometerse
2. **MEMORY.md persistente**: cada sub-agente lee + escribe en memoria compartida
3. **Decision tree de feedback** CONTESTED / ALIGNED de 9 reglas
4. **Handoff humano explícito**: cada sub-agente conoce su gating de escalación
5. **Sin trace-based rubrics**: los verifiers chequean outputs, no caminos

## Quick start

```bash
cd 06-hermes
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.example .env
# Editar .env con ANTHROPIC_API_KEY, OPENAI_API_KEY, etc.

# Correr verifiers
pytest verifiers/

# Iniciar el orquestador (modo dry-run)
python orchestrator.py --dry-run
```

## Sub-agentes — orden de implementación

| # | Sub-agente | Sprint | Por qué |
|---|---|---|---|
| 1 | **Ops-Monitor-Bot** | Sprint 1 (Día 0–15) | Sin observabilidad no podemos verificar el resto |
| 2 | **Watchtower-Bot** | Sprint 2 (Día 15–30) | OSINT continuo desde temprano = ventaja acumulativa |
| 3 | **Recruiter-Bot** | Sprint 3 (Día 30–45) | Resuelve el cuello de botella humano identificado |
| 4 | **Sales-Bot** | Sprint 4 (Día 45–60) | Sales motion estructurado con cultivación 3–6 meses |
| 5 | **Compliance-Watcher** | Sprint 5 (Día 60–75) | Antes del primer hospital pagado |
| 6 | **Content-Bot** | Sprint 6 (Día 75–90) | Distribución orgánica del whitepaper + Academy |

## Costo operativo estimado

- **LLM calls**: USD 800–1,400/mes (Claude Sonnet 4.5 como default, GPT-5 fallback)
- **Infraestructura**: USD 280/mes (Postgres + Qdrant self-hosted + Temporal Cloud free tier inicial)
- **Tooling**: USD 200/mes (LangSmith, MCPs, third-party APIs)
- **Total operando los 6 sub-agentes**: USD 1,280–1,880/mes

Comparado con el costo equivalente humano (USD 24,000+/mes para hacer las mismas tareas con 4 personas en Perú): **factor 15× de palanca**.
