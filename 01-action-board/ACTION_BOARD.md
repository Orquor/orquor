# ACTION BOARD — Tablero del despertar

Este es el primer archivo que abres al despertar. Lista priorizada de acciones que el asesor no puede ejecutar por ti (requieren tus credenciales, tu cuerpo en el mundo real, o decisiones intuitivas tuyas). Todo lo demás ya está construido.

Cada acción tiene: prioridad, tiempo estimado, costo, bloqueadores, qué desbloquea.

---

## P0 — HOY (día 0, 4–6 horas reales)

### A0.1 Comprar el cinturón de dominios `orquor` — 45 minutos, USD 60–180
- Registrar en **Hostinger Domain Registrar** (stack ya activo de Fred):
  - `orquor.com` (~USD 10/año con plan de hosting, ~USD 14/año standalone)
  - `orquor.ai` (~USD 75/año — TLD premium)
  - `orquor.health` (~USD 80/año — TLD restringido)
  - `orquor.io` (~USD 40/año)
  - `orquor.co` (~USD 28/año)
  - `orquor.app` (~USD 18/año)
- Activar **DNSSEC** en hPanel → Domains → DNS
- Activar **WHOIS Privacy** (gratis incluido con Hostinger)
- Habilitar 2FA del hPanel antes de cualquier otra acción
- **Bloquea**: todo lo demás. No avanza nada sin dominios fijos.
- **Desbloquea**: deploy de web, email transaccional, OAuth migration, sales material.

### A0.2 Crear handles sociales `@orquor` — 45 minutos, USD 0
- X (Twitter): `@orquor` o `@orquorai`
- LinkedIn Company Page: `Orquor`
- YouTube: canal `Orquor`
- Instagram: `@orquor`
- TikTok: `@orquor`
- GitHub Organization: `orquor`
- Discord server: `orquor.gg/community`
- Email founder: `freddy@orquor.com` (Google Workspace USD 6/usuario/mes una vez tengas DNS)
- **Bloquea**: lanzamiento social
- **Desbloquea**: cada canal de Content Calendar

### A0.3 Iniciar registro de marca ORQUOR en INDECOPI — 90 minutos, USD 720
- Acceder a [INDECOPI > Marcas](https://www.indecopi.gob.pe/dsd) y crear cuenta
- Registrar marca denominativa ORQUOR en clases Niza:
  - **9** (software, hardware)
  - **35** (servicios empresariales, publicidad)
  - **42** (SaaS, I+D científico, hosting)
  - **44** (servicios médicos)
- Costo aproximado: PEN ~680 por clase × 4 = PEN 2,720 (~USD 720)
- Plazo de aprobación: 6–8 meses
- **Bloquea**: trademark defense para EE.UU. eventual
- **Desbloquea**: protección legal de la marca, prerequisito para Ley 29733 strict compliance

---

## P1 — ESTA SEMANA (días 1–7)

### A1.1 Migración técnica de iteramed.sbs → clinical.orquor.com — 8 horas técnicas
- Seguir `10-migration-runbook/RUNBOOK.md` paso a paso
- DNS Cloudflare apuntando a IP actual del A100 Hyperstack
- SSL Let's Encrypt automático vía Cloudflare
- 301 redirect permanente de toda la zona `.sbs` → `clinical.orquor.com`
- Migrar Google OAuth client (nuevos `redirect_uri`)
- Email transactional con Resend (`noreply@orquor.com`)
- Comunicación a usuarios existentes (template en `10-migration-runbook/email-template-migration.md`)
- **Bloquea**: cualquier RFP o pitch a hospital serio
- **Desbloquea**: marca presentable a clientes B2B

### A1.2 Publicar landing en `orquor.com` — 30 minutos
- Sitio en `04-web/index.html` listo
- Deploy en **Hostinger Web Hosting** (Premium o Business):
  - hPanel → Files → File Manager → `public_html/`
  - Eliminar el `index.html` default
  - Subir el contenido completo de `04-web/`
  - Verificar acceso en `https://orquor.com`
- Activar **SSL gratis Let's Encrypt** en hPanel → Security → SSL (1 click)
- **Desbloquea**: link a compartir en pitches y outreach

### A1.3 Publicar whitepaper ACTO — 2 horas
- Texto completo en `03-whitepaper-acto/whitepaper-acto.md`
- **PDF ya generado** en `03-whitepaper-acto/whitepaper-acto.pdf` (60 KB, listo para distribuir)
- **DOCX ya generado** en `03-whitepaper-acto/whitepaper-acto.docx` (22 KB, para inversores que prefieran)
- **HTML standalone** en `03-whitepaper-acto/whitepaper-acto.html` (para blog post directo)
- Subir PDF a arXiv (cat: cs.CL, cs.LG) — primera publicación define la categoría
- Subir PDF también a `public_html/whitepaper-acto.pdf` en Hostinger para enlace directo
- Postear en blog de Orquor (subdominio `blog.orquor.com` o `/blog`)
- Anunciar en X + LinkedIn (copy ya redactado en `09-content-calendar/`)
- **Desbloquea**: dominancia memética; cualquier competidor tiene que explicarse en tu vocabulario

### A1.4 Iniciar cultivación de 3 prospects priority 1 — Sesión Semana 1
- Abrir `08-prospects/CR-01-clinica-biblica.md`, `08-prospects/CR-02-cima-san-jose.md`, `08-prospects/CO-01-fundacion-cardioinfantil.md`
- Identificar el "asset" (decision-maker) en LinkedIn
- Engagement ambiental: comentar 1 post de cada uno con sustancia técnica
- Compartir el whitepaper ACTO con caption específico
- NO HACER outbound directo — la cultivación es de 3–6 meses
- **Desbloquea**: pipeline de primer hospital pagado en mes 5–7

### A1.5 Empezar publicación diaria de contenido — Día 1
- Calendario en `09-content-calendar/CALENDAR.md`
- LinkedIn: post Día 1 ya redactado en `09-content-calendar/linkedin/dia-001.md`
- X: hilo Día 1 en `09-content-calendar/x-twitter/dia-001.md`
- YouTube: script Episodio 1 en `09-content-calendar/youtube/ep-001-script.md`
- **Desbloquea**: distribución orgánica, leads inbound, autoridad

---

## P2 — PRÓXIMAS 4 SEMANAS

### A2.1 Compliance Ley 29733 + HIPAA-ready — 40 horas + USD 4–8k
- Política de privacidad: template en `07-legal/privacy-policy-ley-29733.md`
- HIPAA BAA template: `07-legal/baa-template.md` — pasar por abogado de healthcare US
- Registro ARCO en MINJUS (Perú)
- Audit logs con cryptographic timestamping (RFC 3161 vía OpenTimestamps)
- Encryption at-rest + in-transit documentado

### A2.2 Infra N+1 con segundo A100 — 1 semana + USD 940/mes adicional
- Contratar A100 reservado en **Lambda Labs** US-West (Lambda firma BAA, Hyperstack no por default)
- Configurar failover activo-pasivo
- Status page público (Better Uptime USD 24/mes o Instatus USD 20/mes)
- Documentar SLA 99.9% año 1

### A2.3 Producir primer benchmark publicable — 3 semanas
- Dataset de evaluación 500-1000 ejemplos por especialidad clínica
- Medir WER médico vs Whisper Large v3 baseline
- COMET de traducción ES médico vs DeepL, NLLB-200
- Publicar metodología + resultados en arXiv (segundo paper)
- Usar las skills de Freddy en rubrics outcome-based + verifiers pytest

### A2.4 Primer encuentro real con prospect — Mes 1
- Conferencia objetivo: **Medical Tourism Association Annual Congress** (target Nov 2026 si es CR) o **eHealth Latin America** o **SUMA Health Latin America**
- Ir físicamente. Aprovechar la cultivación previa para encuentros agendados.
- No pitch — elicitation primero, problema antes de solución

### A2.5 Aplicar a ProInnovate / Innóvate Perú — 2 semanas
- Programa: PIPEI o Reto Bio Tecnología
- Hasta USD 140k no reembolsables
- Aplicar con thesis: "Evaluación rigurosa de modelos de lenguaje médicos con verifiers outcome-based — capacidad técnica peruana sovereign"

---

## P3 — PRÓXIMOS 90 DÍAS

### A3.1 Definir y trademark del término categórico ACTO
- Whitepaper ya publicado (P1)
- Trademark del término "Auditable Clinical Translation Orchestration" + acrónimo ACTO en USPTO + INDECOPI + WIPO
- Costo: USD 2,500–4,000 con abogado de IP
- Cultivar 3 voces de industria (analista, CMO de hospital reconocido, profesor PUCP) para que usen el término orgánicamente

### A3.2 Reclutamiento del primer co-founder técnico
- Profile: senior ML engineer con experiencia en ASR/MT + interés en healthcare
- Vesting 4 años con cliff 1 año
- Equity 8–15% según seniority y momento de ingreso
- Plan: comunidad PUCP, UTEC, redes Stripe alumni LATAM

### A3.3 Aplicar a Anthropic Safety Grants
- Thesis: "Verifier-backed clinical translation as a high-stakes eval frontier"
- Conecta con tu experiencia OpenClaw Atlas directamente
- Path: partnership@anthropic.com

### A3.4 Conversaciones iniciales con Salkantay y Kayyak Ventures
- NO pitch. Coffee chat. Construir relación.
- Mostrar ACTO whitepaper + benchmarks publicados + revenue inicial CR/CO
- Path: warm intro via Endeavor Perú network o Stanford LatAm

---

## Bloqueos críticos identificados (mitigar inmediatamente)

| Bloqueo | Mitigación |
|---|---|
| Hyperstack no firma BAA | Migrar GPU secundaria a Lambda Labs (P2.2) |
| ITERAMED.com tomado por consultora de química US | Marca ORQUOR ya elegida y validada en 4 sistemas. No revisar. |
| Sin abogado de healthcare US | Contactar firmas especializadas: Foley & Lardner, Polsinelli, Manatt. Consulta inicial USD 500–1500 |
| Capital limitado para los primeros 6 meses | ProInnovate + ingreso de Outlier/Scale freelance + revenue de Orquor Academy primer trimestre |

---

## Métricas que el asesor monitoreará al regresar

- ¿Dominios comprados? (sí/no)
- ¿Whitepaper publicado en arXiv? (link)
- ¿Landing deployada en orquor.com? (link)
- ¿Cuántos posts de LinkedIn publicados?
- ¿Cuántos prospects en cultivación activa?
- ¿Migración técnica ejecutada?

Al regresar, decir: **"Asesor, dame el siguiente movimiento basado en estado actual"** y se reactiva el sistema con datos nuevos.
