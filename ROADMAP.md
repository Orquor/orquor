# ORQUOR Roadmap

> Plan estratégico trimestral. Cada milestone incluye objetivos medibles (OKRs), dependencias, riesgos y criterios de salida. Repo: [github.com/Orquor/orquor](https://github.com/Orquor/orquor)

---

## Q3 2026 — Piloto Multi-Site & Fundación Academy

**Período:** Julio – Septiembre 2026  
**Foco:** Validación clínica temprana, reclutamiento de verificadores, primera cohorte educativa.

### Objetivos (OKRs)

| KR | Métrica | Meta |
|----|---------|------|
| KR1 | Sitios clínicos activos en piloto | 3+ hospitales/clínicas (Lima) |
| KR2 | Verificadores registrados en plataforma | 100 verificadores onboarded |
| KR3 | Cohort 1 Academy completado | 30 alumnos graduados |
| KR4 | Casos procesados en plataforma | 1,000+ casos verificados |
| KR5 | Precisión del modelo (F1-score) | ≥ 0.85 en validación interna |

### Hitos Detallados

#### M1.1 — Plataforma Multi-Tenant (Semanas 1–4)
- [ ] Arquitectura multi-site: aislamiento de datos por hospital
- [ ] RBAC (roles: admin hospital, verificador, auditor, superadmin)
- [ ] Onboarding automatizado de instituciones (invitación + verificación dominio)
- [ ] Dashboard de métricas por sitio (casos, precisión, tiempo de verificación)
- **Criterio salida:** 2 hospitales onboarded en ambiente staging con datos sintéticos

#### M1.2 — Piloto Clínico (Semanas 5–10)
- [ ] Despliegue producción en 3 hospitales de Lima Metropolitana
- [ ] Integración HL7/FHIR con sistemas hospitalarios existentes
- [ ] Pipeline de ingesta: DICOM + informes radiológicos + notas clínicas
- [ ] Protocolo de validación clínica aprobado por comité de ética local
- [ ] SLA interno: verificación < 4 horas para casos urgentes
- **Criterio salida:** 1,000 casos reales procesados, F1 ≥ 0.85

#### M1.3 — Programa de Verificadores (Semanas 3–12)
- [ ] Plataforma de registro y credentialing de verificadores
- [ ] Sistema de reputación y scoring por precisión
- [ ] Workflow de asignación: caso → especialidad → verificador disponible
- [ ] Panel de ganancias para verificadores (transparencia)
- **Criterio salida:** 100 verificadores activos con ≥ 5 casos completados cada uno

#### M1.4 — ORQUOR Academy Cohort 1 (Semanas 6–12)
- [ ] Curriculum: 6 módulos (IA en salud, verificación clínica, ética, regulación)
- [ ] LMS integrado con certificación digital
- [ ] Mentoría 1:1 con especialistas (mínimo 4 sesiones por alumno)
- [ ] Proyecto final: análisis de 10 casos reales con supervisión
- **Criterio salida:** 30 graduados, NPS ≥ 60, ≥ 80% tasa de finalización

### Dependencias
- Acuerdos institucionales con hospitales de Lima (en curso)
- Contratación de Director Médico (FTE) y Clinical Lead
- Aprobación de protocolo por IRB/CEI local

### Riesgos (Top 3)
1. **Retraso en acuerdos hospitalarios** → mitigación: comenzar con clínicas privadas (menor fricción)
2. **Calidad de datos insuficiente** → mitigación: pipeline de data cleaning + anotación manual inicial
3. **Baja retención de verificadores** → mitigación: incentivos tempranos + comunidad activa (Discord/Slack)

### Presupuesto Q3
| Concepto | Estimado (USD) |
|----------|---------------|
| Infraestructura cloud (GPU + hosting) | $12,000 |
| Personal (5 FTE) | $75,000 |
| Academia (LMS + contenido + mentores) | $18,000 |
| Legal & compliance (Perú) | $10,000 |
| **Total** | **$115,000** |

---

## Q4 2026 — General Availability LATAM & FDA Pre-Submission

**Período:** Octubre – Diciembre 2026  
**Foco:** Lanzamiento comercial en Perú y Colombia, inicio de pathway regulatorio FDA, primeros contratos pagos.

### Objetivos (OKRs)

| KR | Métrica | Meta |
|----|---------|------|
| KR1 | Hospitales con contrato pago | 5 hospitales |
| KR2 | MRR (Monthly Recurring Revenue) | $25,000+ |
| KR3 | FDA pre-submission package | Enviado Q4 |
| KR4 | GA launches | 2 países (Perú + Colombia) |
| KR5 | Casos procesados acumulados | 15,000+ |

### Hitos Detallados

#### M2.1 — GA Perú (Semanas 1–4)
- [ ] Certificación de protección de datos personal (Ley 29733)
- [ ] Contratos SLAs: uptime 99.5%, verificación urgente < 2h
- [ ] Onboarding self-service para hospitales pequeños/medianos
- [ ] Integración con HIS locales (InterSystems, SIS, EsSalud compatibilidad)
- [ ] Pricing público: tiers por volumen de casos + especialidades
- **Criterio salida:** 3 hospitales pagando en Perú

#### M2.2 — GA Colombia (Semanas 5–10)
- [ ] Entidad legal en Colombia (SAS o sucursal)
- [ ] Cumplimiento Habeas Data + circular única SIC
- [ ] Alianza con 1 universidad colombiana (residencia médica)
- [ ] Adaptación de modelos a terminología médica colombiana
- **Criterio salida:** 2 hospitales pagando en Colombia

#### M2.3 — FDA Pre-Submission (Semanas 1–12)
- [ ] Clasificación de dispositivo: SaMD Class II (probable vía De Novo o 510k)
- [ ] Contratación de FDA regulatory consultant (firma USA especializada)
- [ ] Documentación QMS (ISO 13485 gap analysis completado)
- [ ] Pre-submission meeting request (Q-Sub) preparado y enviado
- [ ] Evidencia clínica: estudio retrospectivo con datos de Q3 + Q4
- **Criterio salida:** Q-Sub package enviado a FDA, tracking number asignado

#### M2.4 — Expansión de Verificadores (Continua)
- [ ] Meta: 250 verificadores activos
- [ ] Especialidades cubiertas: radiología, patología, dermatología, oftalmología
- [ ] Programa de referidos para verificadores
- [ ] Tier de verificadores: junior (supervisado) → senior → attending

### Dependencias
- Cierre de ronda pre-seed ($500K-$750K) para financiar Q4 operaciones
- Resultados de piloto Q3 que demuestren eficacia clínica
- Contratación de Head of Sales LATAM

### Riesgos (Top 3)
1. **Rechazo o demora FDA** → mitigación: comenzar parallel path con ANVISA (Brasil) y COFEPRIS (México)
2. **Ciclo de ventas hospitalario largo** → mitigación: modelo freemium (30 días gratis) + caso de negocio ROI claro
3. **Competencia local** → mitigación: diferenciación vía Academy + verificadores certificados

### Presupuesto Q4
| Concepto | Estimado (USD) |
|----------|---------------|
| Infraestructura cloud | $18,000 |
| Personal (10 FTE) | $150,000 |
| FDA consultants + legal USA | $60,000 |
| GA launches (marketing + legal local) | $35,000 |
| Ventas & BD LATAM | $25,000 |
| **Total** | **$288,000** |

---

## Q1 2027 — Expansión Brasil & México + HITRUST + Series A Prep

**Período:** Enero – Marzo 2027  
**Foco:** Entrada a las dos economías más grandes de LATAM, certificación de seguridad, preparación para ronda Serie A.

### Objetivos (OKRs)

| KR | Métrica | Meta |
|----|---------|------|
| KR1 | Países operativos | 4 (PE, CO, BR, MX) |
| KR2 | Hospitales pagando | 20+ |
| KR3 | MRR | $100,000+ |
| KR4 | HITRUST i1 certification | Obtenida |
| KR5 | Series A deck + data room | Completos |
| KR6 | Verificadores | 500+ (multilingüe ES/PT) |

### Hitos Detallados

#### M3.1 — Expansión Brasil (Semanas 1–8)
- [ ] Entidad legal en Brasil (Ltda) con representante legal local
- [ ] Cumplimiento LGPD (Lei Geral de Proteção de Dados)
- [ ] Modelos NLP fine-tuned para portugués médico brasileño
- [ ] Certificación ANVISA inicial (registro de software como dispositivo médico)
- [ ] Alianza con 2 hospitales universitarios (USP, UNIFESP o similar)
- [ ] Contratación de Country Manager Brasil
- **Criterio salida:** 3 hospitales en onboarding en Brasil

#### M3.2 — Expansión México (Semanas 3–10)
- [ ] Registro sanitario COFEPRIS (software dispositivo médico Clase I/II)
- [ ] Entidad legal en México (S. de R.L.)
- [ ] Alianza con sistema IMSS o ISSSTE para piloto institucional
- [ ] Adaptación cultural y terminológica al español mexicano
- **Criterio salida:** 2 hospitales en onboarding en México

#### M3.3 — HITRUST i1 Certification (Semanas 1–12)
- [ ] Gap assessment inicial con firma auditora HITRUST
- [ ] Implementación de controles: 182 requerimientos i1
- [ ] Infraestructura: encriptación end-to-end, audit logging completo
- [ ] Penetration testing externo (tercera parte)
- [ ] Validated assessment + corrective action plan
- **Criterio salida:** HITRUST i1 certification letter emitida

#### M3.4 — Series A Preparation (Semanas 4–12)
- [ ] Métricas de negocio auditables: MRR, churn, CAC, LTV, NRR
- [ ] Financial model 3 años (conservador, base, optimista)
- [ ] Pitch deck refinado con narrative EEUU + LATAM
- [ ] Data room virtual (Docsend o similar) con DD completo
- [ ] Identificación de 20+ VC targets (digital health + LATAM + AI)
- [ ] Legal: cap table limpio, IP assignment verificado, propiedad intelectual registrada
- **Criterio salida:** Roadshow listo para iniciar Q2

### Dependencias
- Éxito de GA en Perú + Colombia (tracción demostrable para inversionistas)
- FDA feedback del Q-Sub (informa narrativa regulatoria)
- Contratación de CFO o Head of Finance

### Riesgos (Top 3)
1. **Complejidad regulatoria Brasil (ANVISA)** → mitigación: socio regulatorio local desde día 1
2. **Burn rate excede runway** → mitigación: modelo de entrada capital-efficient (partners locales absorben costo inicial)
3. **Fragmentación por multilingüe** → mitigación: arquitectura multi-modelo con adaptadores por idioma

### Presupuesto Q1
| Concepto | Estimado (USD) |
|----------|---------------|
| Infraestructura cloud | $30,000 |
| Personal (18 FTE) | $270,000 |
| HITRUST certification | $80,000 |
| Expansión BR + MX (legal + entidad) | $45,000 |
| Series A prep (legal, financial, DD) | $35,000 |
| **Total** | **$460,000** |

---

## Q2 2027 — U.S. Market Entry & Scaling

**Período:** Abril – Junio 2027  
**Foco:** Entrada al mercado estadounidense, escalar a 50 hospitales totales, levantar Serie A.

### Objetivos (OKRs)

| KR | Métrica | Meta |
|----|---------|------|
| KR1 | Hospitales totales (todos los países) | 50 |
| KR2 | Hospitales en EEUU | 3+ pilotos pagos |
| KR3 | MRR | $250,000+ |
| KR4 | Verificadores totales | 1,000+ |
| KR5 | Serie A | Primer close ($5M-$8M) |
| KR6 | FDA 510(k) submission | Enviado (o De Novo aceptado) |

### Hitos Detallados

#### M4.1 — U.S. Entity & Operations (Semanas 1–4)
- [ ] Delaware C-Corp establecida
- [ ] Cuenta bancaria USA + procesador de pagos (Stripe)
- [ ] Contratación: Head of U.S. Operations, Clinical Advisor (MD USA)
- [ ] Oficina virtual o espacio en digital health hub (Nashville, Boston, o SF)
- [ ] Seguro de responsabilidad profesional (medical malpractice + cyber)

#### M4.2 — U.S. Pilot Hospitals (Semanas 2–10)
- [ ] Identificación de 5-8 hospitales target (community hospitals, rural health systems)
- [ ] Value proposition: reducción de costos de verificación 40-60% vs radiologists externos
- [ ] HIPAA compliance completo + BAA (Business Associate Agreements)
- [ ] Integración con EHRs: Epic (App Orchard), Cerner, Meditech
- [ ] Pilot: 3 hospitales con 90 días de prueba paga
- **Criterio salida:** 3 hospitales EEUU en piloto pago, feedback loop establecido

#### M4.3 — FDA Submission & Clearance Path (Semanas 1–12)
- [ ] QMS ISO 13485 certificado + 21 CFR Part 820 compliant
- [ ] Estudio clínico prospectivo (o retrospectivo amplio) con datos multi-continentales
- [ ] 510(k) submission con predicate device identificado (o De Novo si no existe)
- [ ] Contratación de regulatory affairs manager in-house (USA)
- **Criterio salida:** FDA submission completo bajo review

#### M4.4 — Scaling to 50 Hospitals (Continua)
- [ ] Acelerar LATAM: 35 hospitales en PE/CO/BR/MX
- [ ] EEUU: 5 hospitales al cierre del trimestre
- [ ] Resto: early pilots en Chile o Argentina
- [ ] Customer success team: 1 CSM por cada 10 hospitales
- [ ] NRR (Net Revenue Retention) objetivo: ≥ 110%

#### M4.5 — Series A Close (Semanas 4–12)
- [ ] Roadshow activo: pitch a 30+ fondos
- [ ] Lead investor identificado y term sheet firmado (semana 8-10)
- [ ] Due diligence completado
- [ ] Primer close: $5M-$8M (tramo inicial)
- **Criterio salida:** Wire transfer recibido, runway extendido a 24+ meses

### Dependencias
- FDA pre-submission feedback de Q4 2026 (crítico para 510k)
- Serie A cierre exitoso para financiar expansión USA
- HITRUST certification (habilita contratos enterprise en USA)

### Riesgos (Top 3)
1. **FDA clearance demorado** → mitigación: operar bajo enforcement discretion inicialmente, parallel path con CLIA lab partnership
2. **No lograr lead investor para Serie A** → mitigación: bridge round de insiders + revenue financing
3. **Competencia USA establecida** → mitigación: foco en nichos desatendidos (rural hospitals, tele-radiology overflow)

### Presupuesto Q2
| Concepto | Estimado (USD) |
|----------|---------------|
| Infraestructura cloud | $50,000 |
| Personal (30 FTE) | $450,000 |
| FDA submission + clinical study | $150,000 |
| USA market entry (legal + entidad + hiring) | $60,000 |
| Series A (legal, DD, roadshow) | $50,000 |
| **Total** | **$760,000** |

---

## Resumen Financiero (Runway Planning)

| Trimestre | Burn Rate (USD) | Hito de Financiamiento |
|-----------|----------------|------------------------|
| Q3 2026 | $115,000 | Pre-seed ($750K) cerrado antes |
| Q4 2026 | $288,000 | — |
| Q1 2027 | $460,000 | Bridge o notas convertibles si es necesario |
| Q2 2027 | $760,000 | Serie A primer close ($5M-$8M) |

**Runway estimado con pre-seed de $750K + revenue:** ~3 trimestres (hasta Q1 2027).  
**Serie A necesaria antes de Q2 2027** para financiar expansión USA sin disrupción.

---

## Métricas Clave de Éxito (North Star)

| Fecha | Hospitales | MRR | Verificadores | Países |
|-------|-----------|-----|---------------|--------|
| Fin Q3 2026 | 3 (piloto) | $0 | 100 | 1 (PE) |
| Fin Q4 2026 | 8 | $25K | 250 | 2 (PE, CO) |
| Fin Q1 2027 | 20 | $100K | 500 | 4 (PE, CO, BR, MX) |
| Fin Q2 2027 | 50 | $250K | 1,000 | 5+ (PE, CO, BR, MX, US) |

---

## Glosario

| Término | Definición |
|---------|-----------|
| **GA** | General Availability — lanzamiento comercial abierto |
| **HITRUST i1** | Certificación de seguridad de información para healthcare (182 controles) |
| **FDA 510(k)** | Vía regulatoria para dispositivos médicos con predicate sustancialmente equivalente |
| **Q-Sub** | FDA Pre-Submission — reunión/revisión previa a la submission formal |
| **MRR** | Monthly Recurring Revenue — ingreso recurrente mensual |
| **NRR** | Net Revenue Retention — retención neta de ingresos (expansión - churn) |
| **SaMD** | Software as a Medical Device — clasificación regulatoria |
| **ANVISA** | Agência Nacional de Vigilância Sanitária (Brasil) |
| **COFEPRIS** | Comisión Federal para la Protección contra Riesgos Sanitarios (México) |

---

*Última actualización: Mayo 2026. Este roadmap es un documento vivo sujeto a revisión trimestral.*
