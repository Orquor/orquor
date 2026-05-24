# YouTube Episode 3 — "Whitepaper ACTO explicado en 10 minutos"

**Length target**: 10 minutos · **Hook**: 0:00–0:20 · **Body**: 0:20–8:30 · **CTA**: 8:30–10:00
**Idioma**: Español (LATAM)

---

## [0:00–0:20] HOOK

| TIMESTAMP | VISUAL | AUDIO |
|-----------|--------|-------|
| 0:00–0:20 | Freddy a cámara. Fondo neutro. En sus manos, una copia impresa del whitepaper ACTO con portada visible. | "Hay un documento que va a cambiar cómo los hospitales compran tecnología de traducción médica. Se llama ACTO — Auditable Clinical Translation Orchestration. En los próximos diez minutos voy a explicártelo completo. Sin marketing. Sin slides genéricos. El whitepaper real, las siete métricas, la arquitectura, y por qué lo publicamos en arXiv en vez de patentarlo. Quédate. Esto le importa a cualquiera que toque datos clínicos." |

## [0:20–1:30] CONTEXTO — ¿Por qué existe este whitepaper?

| TIMESTAMP | VISUAL | AUDIO |
|-----------|--------|-------|
| 0:20–0:45 | Freddy a cámara. Corte a slide con título: "El problema: dos mercados que fallan". | "En el episodio uno definí ACTO como la categoría que debería existir en healthcare AI. En el episodio dos mostré el código de los verificadores. Hoy voy al origen: el whitepaper que estamos publicando en arXiv. ¿Por qué un whitepaper? Porque el mercado de interpretación médica está fracturado. Tienes interpretación humana remota — precisa pero lenta y costosa. Tienes traducción por IA — rápida y barata pero sin trazabilidad. Nadie ofrece las tres cosas simultáneamente: velocidad, costo y defensibilidad legal." |
| 0:45–1:30 | Corte a gráfico de dos ejes: Eje X = "Costo por minuto", Eje Y = "Defensibilidad legal". Dos puntos graficados: VRI (alto costo, baja defensibilidad) y AI-only (bajo costo, nula defensibilidad). Un tercer punto parpadea en el centro: ACTO. | "El whitepaper propone una tercera categoría. No es un producto. Es una especificación. Define qué significa 'traducción clínica auditable' como categoría de ingeniería, no como claim de marketing. Cualquier vendor puede construir contra esta especificación. Cualquier hospital puede usarla para evaluar proveedores. Cualquier regulador puede referenciarla. Eso es lo que hace un whitepaper técnico bien escrito: crea el campo de juego." |

## [1:30–4:00] LOS SIETE EJES DE ACTO

| TIMESTAMP | VISUAL | AUDIO |
|-----------|--------|-------|
| 1:30–2:00 | Slide con título: "ACTO — 7 Ejes de Desempeño Simultáneo". Siete íconos enumerados. | "El corazón del whitepaper son los siete ejes. No son aspiracionales. Son medibles. Cada eje tiene una métrica concreta, un umbral cuantitativo y un método de verificación. Si un sistema no cumple los siete simultáneamente, no es ACTO. Punto." |
| 2:00–2:40 | Slide: Eje 1 "Latencia < 2s al primer token" con un cronómetro animado. Eje 2 "Costo $0.20–$0.80/min" con gráfico de barras comparativas. | "Eje uno: latencia. Menos de dos segundos al primer token. Esto viene de estudios de flujo conversacional en trauma. Si la traducción tarda más de dos segundos, el ritmo clínico se rompe. Eje dos: costo. Entre veinte y ochenta centavos de dólar por minuto. Un orden de magnitud debajo del VRI humano. Un orden de magnitud arriba del AI-only porque incluye verificación. Ese diferencial paga la defensibilidad." |
| 2:40–3:20 | Slide: Eje 3 "Medical WER ≤ 5%" con heatmap de errores. Eje 4 "COMET-22 ≥ 0.86" con gráfico de dispersión. | "Eje tres: medical word error rate menor o igual al cinco por ciento. No es WER genérico. Es WER sobre corpus clínicos con terminología farmacológica, anatómica y de procedimientos. Eje cuatro: fidelidad de traducción. COMET-22 en 0.86 o superior. COMET es el estándar de evaluación de traducción neuronal que correlaciona con juicio humano. 0.86 es el umbral donde los clínicos bilingües dejan de detectar diferencias significativas." |
| 3:20–4:00 | Slide: Eje 5 "Audit log criptográfico por utterance" con ícono de candado y blockchain. Eje 6 "Adaptación de registro por especialidad" con íconos de ER, Farmacia, Psiquiatría. Eje 7 "Defensibilidad legal: HIPAA, LPDP, LGPD, GDPR" con logos de las regulaciones. | "Eje cinco: el audit log. Cada utterance genera una entrada con timestamp criptográfico — RFC 3161 u OpenTimestamps anclado a Bitcoin. Eje seis: adaptación de registro. La forma de traducir en Emergencias no es la misma que en Farmacia. El sistema debe detectar la especialidad y adaptar el tono, vocabulario y estructura. Eje siete: defensibilidad matemática ante HIPAA, la ley peruana 29733, la LGPD brasileña y GDPR. Si tu abogado no puede defender la traducción en corte, no es ACTO." |

## [4:00–6:00] LA ARQUITECTURA — El orquestador y los agentes

| TIMESTAMP | VISUAL | AUDIO |
|-----------|--------|-------|
| 4:00–4:45 | Diagrama de arquitectura: cinco cajas conectadas por un hexágono central etiquetado "Orchestrator". Las cajas: ASR Agent, Translation Agent, Verifier Suite (60+), Crypto Audit Primitive, Human Interpreter Pool. Flechas de datos entre ellas. | "Ahora la arquitectura. Esto es lo que hace que ACTO no sea 'traducción rápida con extras'. Es un sistema multi-agente con un orquestador central. El orquestador recibe audio del micrófono del clínico. Lo pasa al agente ASR. El transcript pasa al agente de traducción, que aplica adaptación de registro según la especialidad detectada. La traducción candidata pasa por la suite de verificación — sesenta verificadores, cada uno chequeando una propiedad específica. Si el score ponderado cruza el umbral, se entrega. Si no, el orquestador reintenta con la señal de fallo como feedback o escala a un intérprete humano." |
| 4:45–5:30 | Zoom al hexágono del Orchestrator. Animación de flujo: utterance entra → ASR → MT → Verifiers → decisión de gating → entrega o escalación. | "El orquestador es el componente que no existe en ningún otro producto del mercado. No es un modelo de lenguaje. Es un motor de decisión determinista que recibe resultados estructurados de los verificadores, computa una suma ponderada, y toma una decisión binaria: entregar o escalar. Cada decisión queda registrada en el audit log. Esto es lo que convierte una traducción en un evento auditable." |
| 5:30–6:00 | Zoom a la caja "Verifier Suite". Muestra los nombres de 10 verificadores de ejemplo: `verify_dosage_preserved`, `verify_no_phi_leakage`, `verify_negation_preserved`, `verify_controlled_substance_match`, `verify_register_formal_clinical`, `verify_numeric_consistency`, `verify_medication_name_match`, `verify_allergy_preserved`, `verify_abbreviation_expansion`, `verify_consent_language_match`. | "Los verificadores son el componente más novedoso del whitepaper. No son modelos. Son tests deterministas — código que corre después del modelo. Cada uno chequea una propiedad específica. Si un verificador falla, devuelve un peso firmado y una razón estructurada. El whitepaper incluye la taxonomía completa de verificadores organizada por especialidad clínica y severidad de fallo." |

## [6:00–7:30] EL PRIMITIVO CRIPTOGRÁFICO — La capa legal

| TIMESTAMP | VISUAL | AUDIO |
|-----------|--------|-------|
| 6:00–6:45 | Diagrama de flujo del audit log: utterance → entrada de log (session_id, utterance_id, audio_blob_ref, asr_transcript, translation, verifier_results, timestamp) → OpenTimestamps → Bitcoin blockchain. | "Esta es la parte del whitepaper que más preguntas genera en las demos con hospitales. El primitivo criptográfico. Cada utterance genera una entrada de log. Esa entrada contiene: ID de sesión, ID de utterance, referencia al blob de audio encriptado, transcript del ASR, traducción, resultados de los verificadores, y un timestamp de una autoridad de timestamping externa. OpenTimestamps ancla esto a la blockchain de Bitcoin. RFC 3161 usa una CA comercial." |
| 6:45–7:30 | Corte a Freddy a cámara. Slide detrás: "Sin dependencia de Orquor para verificación futura." | "Lo importante: el hospital no depende de Orquor para verificar sus logs en el futuro. Si Orquor desaparece, si cambia de infraestructura, si es adquirida, el hospital sigue pudiendo demostrar la integridad de sus traducciones. Un auditor independiente puede verificar el anclaje en Bitcoin sin pedirnos permiso. Esto es lo que significa 'matemáticamente defendible'. No es un claim. Es una propiedad criptográfica. El whitepaper dedica una sección entera a los vectores de ataque y cómo el diseño los mitiga." |

## [7:30–8:30] POR QUÉ ABIERTO — La estrategia

| TIMESTAMP | VISUAL | AUDIO |
|-----------|--------|-------|
| 7:30–8:00 | Freddy a cámara. Slide con texto: "arXiv. Sin patente. Sin trademark." | "El whitepaper va a arXiv. No estamos patentando la categoría. No estamos registrando el término ACTO como marca. Esto es contraintuitivo para una startup. Lo sé. Pero la categoría no debería pertenecer a un solo vendor. Si ACTO es propiedad de Orquor, los hospitales dependen de nosotros para la definición. Si ACTO es abierto, los hospitales pueden exigir conformidad con ACTO en sus RFPs. Los reguladores pueden señalar ACTO como estándar de referencia. Los competidores pueden construir implementaciones de ACTO. Y nosotros competimos siendo la mejor implementación." |
| 8:00–8:30 | Slide con comparación: "Modelo propietario → moat de marketing (frágil)" vs "Modelo abierto → moat de implementación (defendible)". | "El whitepaper no es un documento de producto. Es un documento de categoría. Define el problema, los ejes, la arquitectura de referencia, y deja la implementación abierta. Cualquiera puede construir contra ACTO. Nosotros ya lo estamos haciendo. Cuando un hospital decida comprar un sistema ACTO, la pregunta no será '¿quién tiene la marca?' sino '¿quién tiene la mejor implementación?' Ahí es donde queremos estar." |

## [8:30–10:00] CTA

| TIMESTAMP | VISUAL | AUDIO |
|-----------|--------|-------|
| 8:30–9:15 | Freddy a cámara. Lower third: "orquor.com/whitepaper". | "Tres cosas que puedes hacer. Uno: si trabajas en informática clínica, procurement hospitalario o derecho sanitario, el whitepaper completo estará en orquor.com/whitepaper apenas se publique en arXiv. Suscríbete para recibirlo. Dos: si estás construyendo algo adyacente a esto — incluso si compite directamente con nosotros — ponte en contacto. Prefiero que la categoría emerja de forma coordinada. Tres: suscríbete. El episodio cuatro va a ser 'Por qué LATAM es el lugar correcto para healthcare AI'. Es un take que no he visto a nadie hacer." |
| 9:15–10:00 | End frame: Logo de Orquor + URL + "Próximo episodio: ¿Por qué LATAM?" | "Soy Freddy. Construimos Orquor en Lima. Operamos en toda América Latina. Si algo te quedó del whitepaper, escríbeme. Si estás en un hospital y quieres ver cómo ACTO aplica a tu caso específico, agenda una demo. Vemos esto en el próximo episodio." |

---

## Production notes

- B-roll: Whitepaper impreso en close-up, diagrama de arquitectura animado, captura de arXiv submission page, terminal mostrando OpenTimestamps verification, gráficos de los 7 ejes con animación.
- Camera: iPhone 15 Pro, 4K, locked focus.
- Audio: Rode Wireless ME. Verificar -16 LUFS.
- Lighting: Key Aputure MC 5600K, fill softbox.
- Background: Warm gray. Mesa con laptop y copia del whitepaper.
- Editing: Descript. Auto-captions en español. Lower-thirds para métricas clave.
- Lower third intro: "Freddy | Fundador, Orquor" — 4 segundos.

## Distribution

- YouTube main upload (16:9), publicar Día 10 a las 09:00 UTC-5
- Clip vertical de 60s del segmento [6:45–7:30] (la explicación de independencia criptográfica)
- LinkedIn carousel con los 7 ejes de ACTO, publicar Día 11
- X thread (x-twitter/dia-010.md), publicar Día 11
