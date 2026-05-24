# ORQUOR — Distribución de Agentes Autónomos
# Sistema de 3 agentes trabajando en paralelo

## Arquitectura

```
┌──────────────────────────────────────────┐
│              HERMES (DeepSeek)            │
│         Orquestador + Infraestructura     │
│         WSL Ubuntu 26.04                 │
└──────────────────────────────────────────┘
                    │
        ┌───────────┼───────────┐
        ▼           ▼           ▼
┌───────────┐ ┌───────────┐ ┌───────────┐
│  CLAUDE   │ │   QWEN    │ │  HERMES   │
│ Opus 4.7  │ │  2.5 7B   │ │ DeepSeek  │
│  Cursor   │ │  Ollama   │ │   WSL     │
│  Windows  │ │  Windows  │ │  Ubuntu   │
│  GPU: ❌  │ │ GPU: ✅   │ │  GPU: ❌  │
└───────────┘ └───────────┘ └───────────┘
```

## Roles y Responsabilidades

### CLAUDE (Opus 4.7 — Cursor)
**Rol:** Arquitecto y Constructor Principal
**Fortaleza:** Razonamiento profundo, código complejo, diseño estratégico

**Tareas asignadas:**
- ✅ Documentos estratégicos (whitepaper, brand, pitch)
- ✅ Código complejo (orchestrator, verifiers, sub-agentes)
- ✅ Templates legales
- ✅ Landing pages (HTML/CSS)
- ✅ Contenido de alto valor (LinkedIn, YouTube scripts)
- 🔄 Deploy landing page (Bloque 6)
- 🔄 Optimizar whitepaper para arXiv (Bloque 7)
- 🔄 GitHub profile README + CONTRIBUTING + LICENSE (Bloque 8)
- 🔄 Scripts de automatización (Bloque 9)

**Regla:** Claude construye. No ejecuta. No monitorea. Solo crea archivos.

---

### QWEN (2.5 7B — Ollama/GPU)
**Rol:** Agente Local de Bajo Costo
**Fortaleza:** Español nativo, disponible 24/7, sin costo de API

**Tareas asignadas:**
- Traducción ES↔EN de documentos
- Revisión ortográfica y gramatical de contenido en español
- Generación de variantes de posts (A/B testing)
- Respuestas a preguntas frecuentes
- Resúmenes de documentos
- Clasificación de prospectos
- Validación de consistencia de marca (voice & tone)
- Primer filtro de emails entrantes

**Regla:** Qwen es rápido y barato. Usarlo para tareas repetitivas en español.

---

### HERMES (DeepSeek — WSL)
**Rol:** Orquestador + Infraestructura + Automatización
**Fortaleza:** Acceso a terminal, archivos, redes, APIs

**Tareas asignadas:**
- Coordinación de agentes (este documento)
- Instalación y configuración de herramientas
- Deploy y CI/CD (GitHub Actions, Docker)
- Monitoreo del sistema (health checks, backups)
- Automatización de creación de cuentas
- Verificación de integridad del proyecto
- Gestión de credenciales y seguridad
- Comunicación con APIs externas

**Regla:** Hermes no construye documentos. Orquesta, configura, monitorea.

---

## Protocolo de Comunicación

### Hermes → Claude
- Archivo `NEXT_TASKS.md` en la raíz del proyecto
- O vía Cursor Composer (Ctrl+L) si Cursor está activo
- Claude lee NEXT_TASKS.md al iniciar sesión

### Hermes → Qwen
- API REST: `http://localhost:11434/api/generate`
- Desde WSL vía `test_qwen.py` en Windows
- Modelo: `qwen2.5:7b`

### Qwen → Hermes
- Respuesta por stdout del script
- Resultados guardados en `09-content-calendar/qwen-output/`

---

## Prioridades AHORA

| # | Agente | Tarea | Prioridad |
|---|--------|-------|-----------|
| 1 | Fred | Crear GitHub Organization | 🔴 AHORA |
| 2 | Fred | Activar webmail Hostinger | 🔴 AHORA |
| 3 | Claude | Bloques 6-9 (NEXT_TASKS.md) | 🟡 Paralelo |
| 4 | Qwen | Revisar ortografía contenido LinkedIn | 🟡 Paralelo |
| 5 | Hermes | Deploy landing + verificar todo | 🟡 Paralelo |
