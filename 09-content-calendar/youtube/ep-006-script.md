# YouTube Episode 6 — "Modelos de lenguaje en healthcare: lo que todo hospital debe saber"

**Length target**: 10 minutos · **Hook**: 0:00–0:25 · **Body**: 0:25–8:30 · **CTA**: 8:30–10:00
**Idioma**: Español (LATAM)

---

## [0:00–0:25] HOOK

| TIMESTAMP | VISUAL | AUDIO |
|-----------|--------|-------|
| 0:00–0:25 | Freddy a cámara. Fondo neutro. En pantalla detrás, tres logos: GPT, Claude, Gemini — con una X roja sobre cada uno. | "GPT no está listo para tu hospital. Claude no está listo para tu hospital. Gemini no está listo para tu hospital. Y no es por lo que crees. No es porque alucinan — aunque alucinan. No es porque no saben medicina — aunque no saben tanta como parece. Es porque un modelo de lenguaje es un componente, no una solución. Y en healthcare, tratar un componente como una solución es lo que convierte un error de traducción en un evento adverso. En los próximos diez minutos te voy a explicar qué puede y qué no puede hacer un LLM en un hospital. Sin hype. Sin miedo. Con ingeniería." |

## [0:25–1:30] CONTEXTO — El estado real de los LLMs en healthcare (2026)

| TIMESTAMP | VISUAL | AUDIO |
|-----------|--------|-------|
| 0:25–0:55 | Slide con timeline: "2022: ChatGPT", "2023: GPT-4 + healthcare startups", "2024: Primeros incidentes documentados", "2025: Reguladores empiezan a preguntar", "2026: El mercado se parte en dos". | "Hagamos un poco de historia. En 2022 ChatGPT aparece. En 2023, docenas de startups ponen un wrapper de GPT-4 sobre flujos clínicos y levantan millones. En 2024, los primeros incidentes documentados: traducciones que omiten negaciones, resúmenes clínicos que inventan diagnósticos, asistentes que confunden dosis. En 2025, los reguladores empiezan a preguntar: ¿quién firma esto? ¿Dónde está el audit trail? En 2026, el mercado se parte en dos: los que tratan al LLM como producto final y los que lo tratan como lo que realmente es — un motor probabilístico que necesita verificación externa." |
| 0:55–1:30 | Slide con dos columnas. Izquierda: "LLM como producto" (ícono de chat directo, peligro). Derecha: "LLM como componente" (ícono de sistema multi-agente con verificación, seguridad). | "Un modelo de lenguaje es una distribución de probabilidad sobre secuencias de tokens. No sabe qué es verdad. No sabe qué es una dosis. No sabe qué es una contraindicación. Sabe qué token es más probable que siga a otro token dado un contexto. Eso es suficiente para muchas tareas. No es suficiente cuando la diferencia entre 'administrar 5 mg' y 'administrar 50 mg' es una demanda por negligencia. O un paciente muerto. En healthcare, el output de un LLM nunca debería ser el output final. Debería ser un output candidato que pasa por una capa de verificación antes de tocar a un paciente." |

## [1:30–3:15] LOS CUATRO FRACASOS — Por qué los LLMs fallan en clínica

| TIMESTAMP | VISUAL | AUDIO |
|-----------|--------|-------|
| 1:30–2:00 | Slide: "Fracaso 1: Alucinación semántica." Ejemplo en pantalla: "El paciente presenta dolor torácico" → traducción del LLM: "El paciente presenta dolor de pecho." La palabra "torácico" tachada y reemplazada. | "Fracaso uno: alucinación semántica. El modelo no 'sabe' que 'dolor torácico' y 'dolor de pecho' no son lo mismo en un contexto clínico. Uno es un término técnico con implicaciones diagnósticas. El otro es lenguaje coloquial. El modelo no está razonando sobre medicina. Está prediciendo el token más probable. Si en sus datos de entrenamiento 'chest pain' se traduce más frecuentemente como 'dolor de pecho' que como 'dolor torácico', eso es lo que vas a obtener. Y en una historia clínica, ese coloquialismo degrada la precisión del registro." |
| 2:00–2:30 | Slide: "Fracaso 2: Pérdida de entidades numéricas." Ejemplo: "Administer 2.5 mg of warfarin" → "Administrar 2 mg de warfarina." El ".5" desaparecido en rojo. | "Fracaso dos: pérdida de entidades numéricas. Este es el más peligroso. Los LLMs tokenizan números de formas impredecibles. '2.5' puede ser un token o tres tokens dependiendo del tokenizador. En traducción, es común que el modelo redondee, omita decimales o convierta unidades sin advertirlo. 'Administer 2.5 mg' se convierte en 'Administrar 2 mg'. La diferencia es una sobredosis de warfarina. Esto no es un bug ocasional. Es una propiedad estadística del modelo. Sin un verificador determinista que compare entidades numéricas entre source y target, no hay forma de garantizar que esto no ocurra." |
| 2:30–3:00 | Slide: "Fracaso 3: Negación fantasma." Ejemplo: "Patient does NOT have a penicillin allergy" → "El paciente tiene alergia a la penicilina." La palabra "NOT" desaparecida, la traducción invertida en rojo. | "Fracaso tres: negación fantasma. La partícula de negación es pequeña, fácil de omitir, y su pérdida invierte completamente el significado clínico. 'No tiene alergia' se convierte en 'tiene alergia'. 'No administrar' se convierte en 'administrar'. Los LLMs actuales han mejorado en preservar negaciones simples, pero en oraciones subordinadas complejas — 'el paciente refiere que el médico anterior indicó que no se administrara' — la negación frecuentemente se desplaza o desaparece. En traducción médica, una negación perdida no es un error de estilo. Es una contraindicación fabricada." |
| 3:00–3:15 | Slide: "Fracaso 4: Desalineación regulatoria." Íconos de HIPAA, GDPR, LGPD. Un candado roto al lado de "LLM endpoint". | "Fracaso cuatro: desalineación regulatoria. Un LLM corriendo en un endpoint de API es una caja negra. No sabes qué datos se loguean, dónde se almacenan, quién tiene acceso. Si envías información de paciente a un endpoint de terceros sin un BAA — Business Associate Agreement — estás en incumplimiento de HIPAA. Si el endpoint está fuera de tu jurisdicción, estás potencialmente violando leyes de residencia de datos. Esto no es un problema del modelo. Es un problema de arquitectura. Y la mayoría de las implementaciones hospitalarias de LLMs en 2026 todavía no lo han resuelto." |

## [3:15–5:00] EL ENFOQUE ACTO — Modelos como componentes, no como soluciones

| TIMESTAMP | VISUAL | AUDIO |
|-----------|--------|-------|
| 3:15–3:45 | Diagrama de arquitectura ACTO simplificado: Audio → ASR Agent → Translation Agent → Verifier Suite → Orchestrator → Entrega/Escalación. El Translation Agent está rodeado de un recuadro punteado etiquetado "LLM (componente, no producto)". | "En Orquor no vendemos un modelo de lenguaje. Vendemos un sistema que contiene modelos de lenguaje como componentes. Esa diferencia es fundamental. El LLM hace una cosa: generar una traducción candidata. Nada más. No decide si la traducción es correcta. No decide si se entrega. No decide si escala a un humano. Esas decisiones las toma el orquestador, basado en los resultados de los verificadores. El LLM es un generador de hipótesis. El verificador es el que decide si la hipótesis se acepta." |
| 3:45–4:20 | Diagrama expandido: el Translation Agent se desglosa en tres sub-componentes: "Prompt Engineering" (system prompt con contexto clínico), "Register Detection" (detección automática de especialidad), "Glossary Injection" (glosario de términos médicos con traducciones verificadas). | "Además, el LLM dentro de ACTO no es un LLM genérico con un prompt de 'traduce esto'. El agente de traducción tiene tres capas. Uno: prompt engineering clínico — el system prompt incluye la especialidad detectada, el contexto del utterance anterior, y reglas explícitas de preservación de entidades. Dos: detección de registro — el orquestador identifica si estás en Emergencias, Farmacia o Psiquiatría y el LLM recibe esa señal. Tres: glossary injection — un glosario curado de términos médicos con traducciones verificadas se inyecta en el contexto. Esto reduce la varianza del modelo en terminología de alto riesgo." |
| 4:20–5:00 | Slide comparativa: "LLM solo" vs "LLM + Verificadores". Izquierda: accuracy 92%, sin audit trail, sin defensa legal. Derecha: accuracy 99.4% (post-verificación), audit trail completo, defendible. | "La diferencia cuantitativa importa. Un LLM de traducción médica de última generación opera con un COMET-22 alrededor de 0.82 a 0.84. Con glossary injection, prompt engineering y adaptación de registro, subimos a 0.86–0.88. Con la suite de verificadores detectando y corrigiendo fallos puntuales — negaciones, dosis, nombres de fármacos — el output final está por encima de 0.90. Pero esa mejora no viene del modelo. Viene de la arquitectura alrededor del modelo. El LLM es necesario. No es suficiente." |

## [5:00–6:30] VERIFICADORES — La capa que falta en todas partes

| TIMESTAMP | VISUAL | AUDIO |
|-----------|--------|-------|
| 5:00–5:30 | Pantalla con código Python. Se muestra el output de 3 verificadores ejecutándose sobre una traducción candidata. Uno en verde (PASS), dos en rojo (FAIL) con razón estructurada. | "Los verificadores son la capa que transforma un LLM de juguete a un sistema clínico. En este momento, en nuestra suite de producción, hay sesenta y dos verificadores. Cada uno chequea una propiedad. Si falla, devuelve peso firmado y razón estructurada. Si pasa, devuelve confirmación. El orquestador suma los pesos. Si el resultado neto supera el umbral de gating, la traducción se entrega. Si no, el sistema reintenta con la señal de fallo como feedback o escala a intérprete humano." |
| 5:30–6:00 | Slide con ejemplos de verificadores agrupados por categoría: "Seguridad" (dosage, allergy, controlled_substance), "Precisión" (negation, numeric_consistency, medication_name), "Legal" (no_PHI_leakage, consent_language), "Estilo" (register_formal, abbreviation_expansion). | "Los verificadores se agrupan en cuatro familias. Seguridad: verifican que dosis, alergias y sustancias controladas se preserven exactamente. Un fallo aquí es peso +5 — catastrófico. Precisión: negaciones, consistencia numérica, nombres de medicamentos. Peso +3 — error clínico significativo. Legal: verifica que no se filtre información de paciente protegida, que el lenguaje de consentimiento esté presente cuando corresponde. Peso +4 — riesgo de compliance. Estilo: registro clínico apropiado, expansión de abreviaturas, tono. Peso +1 — calidad. Esta taxonomía permite que el orquestador tome decisiones con granularidad clínica, no solamente binaria." |
| 6:00–6:30 | Freddy a cámara. Slide detrás: "Los verificadores no son un modelo. Son tests deterministas." | "Y aquí está lo importante: los verificadores no son otro modelo de lenguaje. Son tests deterministas. Código que corre en tu infraestructura. Si quieres auditar por qué una traducción específica fue aceptada o rechazada, el log te muestra exactamente qué verificador falló, con qué razón, y qué peso aportó. No es una caja negra. Es un sistema de decisión auditable. Si un hospital quiere añadir sus propios verificadores — por ejemplo, verificar que los nombres de sus médicos no aparezcan en las traducciones — puede hacerlo. La suite es extensible. Esto es arquitectura abierta, no modelo propietario." |

## [6:30–7:45] CÓMO EVALUAR — Preguntas que todo hospital debe hacer

| TIMESTAMP | VISUAL | AUDIO |
|-----------|--------|-------|
| 6:30–7:00 | Slide: "5 preguntas para un vendor de AI clínica." Lista numerada. | "Si estás en un hospital evaluando cualquier herramienta que use modelos de lenguaje — traducción, resumen clínico, asistente de diagnóstico — haz estas cinco preguntas. Primera: ¿el modelo corre on-premise o en tu nube, o estás enviando datos de paciente a un endpoint de terceros? Si es lo segundo, necesitas ver el BAA. Segunda: ¿tienes verificadores deterministas post-modelo o el output del LLM va directo al clínico? Si va directo, estás a un token de distancia de un evento adverso. Tercera: ¿el sistema genera un audit log por utterance con timestamp criptográfico? Si no, no tienes defensa legal." |
| 7:00–7:45 | Freddy a cámara. | "Cuarta: ¿puedo inspeccionar los verificadores? No el modelo — los verificadores. Si el vendor te dice que los verificadores son propietarios y no se comparten, pregúntate qué están ocultando. Los verificadores deberían ser deterministas y auditables. Si no te los muestran, no puedes confiar en ellos. Quinta: ¿qué pasa cuando el sistema falla? ¿Hay un pathway de escalación a humano? ¿Cuánto tarda? ¿Queda registrado? Si el vendor no tiene respuesta para el caso de fallo, no tiene un producto clínico. Tiene un demo." |

## [7:45–8:30] LATAM — El riesgo es más alto, el margen de error es cero

| TIMESTAMP | VISUAL | AUDIO |
|-----------|--------|-------|
| 7:45–8:30 | Mapa de LATAM con hospitales rurales. Superposición de texto: "Sin audit trail = sin defensa legal = sin adopción." | "En LATAM el estándar es más alto, no más bajo. Un hospital público en Perú o Brasil no puede darse el lujo de un error de traducción que termine en un evento adverso. No porque sean más frágiles — porque tienen menos margen político y financiero para absorber un escándalo. Si un LLM traduce mal una dosis y el paciente sufre daño, el hospital no puede decir 'fue la IA'. El hospital es responsable. El director médico es responsable. Sin audit trail, sin verificadores, sin trazabilidad criptográfica, ese hospital está indefenso. En LATAM, la exigencia no es menor que en Estados Unidos. Es mayor. Porque hay menos red de contención." |

## [8:30–10:00] CTA

| TIMESTAMP | VISUAL | AUDIO |
|-----------|--------|-------|
| 8:30–9:15 | Freddy a cámara. Lower third: "orquor.com". | "Tres cosas. Una: si trabajas en informática clínica, TI hospitalaria o compliance y quieres ver cómo nuestros verificadores detectan estos fallos en tiempo real, agenda una demo técnica en orquor.com. Te muestro el código. Te muestro los sesenta y dos verificadores. Te muestro el audit log. Sin marketing. Dos: si estás construyendo herramientas de AI para healthcare — en LATAM o donde sea — y quieres hablar de arquitectura de verificación, escríbeme. Esta capa debería ser estándar en la industria. Mientras más construyamos con verificación, más seguro es el ecosistema para todos." |
| 9:15–10:00 | End frame: Logo de Orquor + URL + "Próximo episodio: El futuro de la interpretación médica." | "Tres: suscríbete. El próximo episodio es 'El futuro de la interpretación médica'. Vamos a proyectar cinco años hacia adelante: qué sobrevive, qué desaparece, y dónde encaja el intérprete humano en un mundo con IA. Soy Freddy. Construimos Orquor en Lima. Operamos en toda América Latina. Si estás evaluando modelos de lenguaje para tu hospital, no compres magia. Compra arquitectura. Nos vemos el próximo martes." |

---

## Production notes

- B-roll: Terminal con verificadores corriendo en Python, captura de pantalla de audit log, diagramas de arquitectura animados, close-up de código, mapa de LATAM.
- Camera: iPhone 15 Pro main lens, 4K, locked focus on face.
- Audio: Rode Wireless ME clip mic. Verify mono channel, -16 LUFS.
- Lighting: Key light Aputure MC at 5600K, fill from softbox window-left.
- Background: Warm gray. Monitor con código visible detrás de Freddy.
- Editing: Descript. Auto-captions en español. Lower-thirds para términos técnicos.
- Lower third intro: "Freddy | Fundador, Orquor" — 4 segundos.
- Música: Solo en intro y outro. Silencio durante los segmentos técnicos.

## Distribution

- YouTube main upload (16:9), publicar Día 31 a las 09:00 UTC-5
- Clip vertical de 60s del segmento [5:00–5:45] (explicación de las 4 familias de verificadores)
- LinkedIn carousel con las "5 preguntas para un vendor de AI clínica", publicar Día 32
- X thread (x-twitter/dia-031.md), publicar Día 32
- Newsletter: incluir las 5 preguntas como checklist descargable.
