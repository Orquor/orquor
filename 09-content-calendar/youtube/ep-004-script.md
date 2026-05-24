# YouTube Episode 4 — "¿Por qué LATAM para healthcare AI?"

**Length target**: 8 minutos · **Hook**: 0:00–0:20 · **Body**: 0:20–6:45 · **CTA**: 6:45–8:00
**Idioma**: Español (LATAM)

---

## [0:00–0:20] HOOK

| TIMESTAMP | VISUAL | AUDIO |
|-----------|--------|-------|
| 0:00–0:20 | Freddy a cámara. Detrás, un mapa de América Latina en pantalla. Marcadores en Lima, São Paulo, CDMX, Bogotá, Buenos Aires. | "Cada vez que un VC de Silicon Valley me pregunta dónde está basado Orquor y le digo Lima, Perú, hay una pausa. Luego la misma pregunta: ¿por qué healthcare AI desde LATAM? En los próximos ocho minutos voy a responder esa pregunta. Y cuando termine, vas a entender por qué LATAM es el mejor lugar del mundo para construir, probar y escalar inteligencia artificial para salud." |

## [0:20–1:30] EL CONTEXTO — Healthcare AI no es un problema de Silicon Valley

| TIMESTAMP | VISUAL | AUDIO |
|-----------|--------|-------|
| 0:20–0:55 | Slide con dos columnas. Izquierda: "Silicon Valley" con íconos de hospitales modernos, seguros privados, inglés monolingüe. Derecha: "LATAM" con íconos de hospitales públicos, multilenguaje (español, portugués, quechua, guaraní), diversidad regulatoria. | "Healthcare AI se ha construido mayoritariamente en Estados Unidos, para Estados Unidos. Eso tiene sentido comercial, pero produce sistemas que asumen cosas que no son ciertas en el resto del mundo. Asumen un solo idioma. Asumen un solo framework regulatorio. Asumen infraestructura de fibra en cada hospital. Asumen presupuestos de developed-world. LATAM rompe todos esos supuestos. Y romper supuestos es exactamente lo que necesitas para construir tecnología que funcione en el mundo real." |
| 0:55–1:30 | Mapa de LATAM con íconos de diversidad: banderas de Perú, Brasil, México, Colombia, Argentina, Chile. Datos en overlay: "660M de habitantes", "33 países", "Español + Portugués + 500+ lenguas indígenas", "Sistemas de salud públicos, privados y mixtos". | "América Latina son seiscientos sesenta millones de personas. Dos idiomas dominantes, más de quinientas lenguas indígenas vivas. Sistemas de salud que van desde el SUS brasileño — el sistema público más grande del hemisferio sur — hasta seguros privados de alta complejidad en Ciudad de México. Regulaciones que incluyen la LGPD brasileña, la ley peruana de protección de datos, y GDPR para cualquier dato de ciudadano europeo. Esto no es un borde. Es el campo de prueba más complejo que existe para healthcare AI." |

## [1:30–3:00] RAZÓN 1 — La necesidad real

| TIMESTAMP | VISUAL | AUDIO |
|-----------|--------|-------|
| 1:30–2:15 | Slide con estadísticas: "30% de hospitales públicos en LATAM sin acceso a interpretación médica profesional", "45% de pacientes indígenas no reciben explicación en su idioma", "Barrera lingüística = 2.3x más riesgo de evento adverso (estudio OMS)". | "Primera razón: la necesidad es real y urgente. En Estados Unidos, la interpretación médica es un problema de compliance y costo. En LATAM, es un problema de acceso. El treinta por ciento de los hospitales públicos de la región no tiene acceso a interpretación médica profesional. Cuando un paciente quechua-hablante llega a emergencias en Cusco, o un guaraní-hablante a un hospital en Paraguay, la comunicación depende de un familiar, un enfermero bilingüe que no está disponible, o simplemente no ocurre. La OMS documenta que la barrera lingüística multiplica por 2.3 el riesgo de evento adverso. Esto no es solamente ineficiencia. Es vidas." |
| 2:15–3:00 | Corte a Freddy a cámara. | "Cuando construyes para resolver esto, el diseño es diferente. No estás optimizando para ahorrarle veinte dólares por consulta a un hospital de Miami. Estás diseñando para que un doctor en Puno pueda explicarle una dosis de insulina a una paciente que solo habla quechua. Ese constraint de necesidad real produce mejores decisiones de producto. Elimina features innecesarias. Te obliga a que cada componente funcione en condiciones de conectividad limitada, bajos recursos y máxima criticidad. Eso hace mejor a la tecnología." |

## [3:00–4:30] RAZÓN 2 — Diversidad regulatoria como ventaja

| TIMESTAMP | VISUAL | AUDIO |
|-----------|--------|-------|
| 3:00–3:45 | Slide con logos de regulaciones: "HIPAA (USA)", "GDPR (EU)", "LGPD (Brasil)", "Ley 29733 (Perú)", "Ley de Protección de Datos Personales (México)", "Ley 1581 (Colombia)". Flechas cruzadas entre ellas. | "Segunda razón: la diversidad regulatoria. Una healthcare AI entrenada solo para HIPAA es frágil. Cuando llega GDPR o LGPD, hay que rehacer la arquitectura de datos. LATAM te obliga a cumplir múltiples regulaciones desde el día uno. La LGPD brasileña es una de las más estrictas del mundo — comparable a GDPR. Perú tiene la ley 29733 con requerimientos específicos de datos sensibles de salud. México, Colombia, Argentina, cada uno con su marco. Si diseñas para cumplir el máximo común denominador de todas estas regulaciones simultáneamente, el resultado es un sistema más robusto." |
| 3:45–4:30 | Diagrama de arquitectura mostrando capa de compliance multi-jurisdiccional: una traducción pasa por verificadores de PHI para HIPAA, verificadores de datos sensibles para LGPD, verificadores de consentimiento para GDPR. Todo en la misma pipeline. | "En Orquor, nuestra suite de verificadores incluye chequeos específicos por jurisdicción. El mismo utterance se verifica contra HIPAA si el hospital es de un país que lo referencia, contra LGPD si es Brasil, contra GDPR si el paciente es ciudadano europeo. Esta capacidad no es un nice-to-have. Es el resultado de haber nacido en un entorno donde múltiples regulaciones aplican desde el inicio. Una startup de San Francisco no encuentra esto hasta su expansión internacional. Nosotros lo tenemos en el ADN del producto." |

## [4:30–5:45] RAZÓN 3 — Talento y costo

| TIMESTAMP | VISUAL | AUDIO |
|-----------|--------|-------|
| 4:30–5:10 | Mapa de LATAM con íconos de universidades: USP, UNAM, UNI, UBA, Uniandes. Overlay: "Top 100 global en CS/AI", "Costo de talento técnico: 40–60% menor que US/Europe". | "Tercera razón: el talento. Brasil, México, Argentina y Perú producen ingenieros de primer nivel en inteligencia artificial. La USP en São Paulo, la UNAM en CDMX, la Universidad de Buenos Aires. Son instituciones con décadas de tradición en ciencias de la computación. Pero el costo de contratar ese talento es cuarenta a sesenta por ciento menor que en Estados Unidos o Europa. Y no es outsourcing. Es construir el equipo core en la región, entendiendo la región, viviendo la región." |
| 5:10–5:45 | Freddy a cámara. Slide con team photo de Orquor (placeholder). | "En Orquor, nuestro equipo está en Lima, São Paulo y remoto por Latinoamérica. El ingeniero que diseña el verificador para terminología farmacológica en español creció hablando español y portugués. Entiende los falsos amigos entre los dos idiomas. Sabe que 'embarazada' en español no es 'embarrassed' en inglés pero tampoco es 'grávida' en un contexto clínico portugués. Ese conocimiento no se adquiere en un curso de localización. Se vive. Tener al equipo en la región donde se usa el producto no es una decisión de costo. Es una decisión de calidad." |

## [5:45–6:45] RAZÓN 4 — El momento

| TIMESTAMP | VISUAL | AUDIO |
|-----------|--------|-------|
| 5:45–6:20 | Slide con línea de tiempo: "2019–2023: Digitalización masiva de historias clínicas en LATAM (Brasil SUS digital, México expediente clínico electrónico, Perú HIS-MINSA)" → "2024–2026: Regulación de IA en salud (Brasil PL 2338/23, Perú reglamento de telemedicina)" → "2026: Ventana de adopción". | "Cuarta razón: el momento es ahora. En los últimos cinco años, los sistemas de salud latinoamericanos han completado una digitalización masiva. Brasil digitalizó el SUS. México impulsó el expediente clínico electrónico nacional. Perú implementó el sistema HIS-MINSA. Por primera vez, la infraestructura digital existe. Al mismo tiempo, los marcos regulatorios para IA en salud están emergiendo — la PL 2338 en Brasil, el reglamento de telemedicina en Perú. La ventana de adopción es 2026 a 2028. Los sistemas que se implementen en esa ventana definirán el estándar para la próxima década." |
| 6:20–6:45 | Freddy a cámara. Cierre del argumento. | "LATAM no es un mercado secundario para healthcare AI. Es el mercado primario para el tipo de healthcare AI que funciona en el mundo real. Multilingüe. Multi-regulatorio. Con restricciones de conectividad y presupuesto. Si tu sistema funciona en un hospital público de la selva peruana y en un hospital privado de São Paulo, funciona en cualquier lado. En Orquor no construimos para LATAM a pesar de ser de LATAM. Construimos para LATAM porque somos de LATAM. Y creemos que lo que construimos aquí es lo que el mundo va a necesitar." |

## [6:45–8:00] CTA

| TIMESTAMP | VISUAL | AUDIO |
|-----------|--------|-------|
| 6:45–7:30 | Freddy a cámara. Lower third: "orquor.com/whitepaper". | "Tres cosas. Uno: si eres healthcare professional en LATAM y quieres ver cómo ACTO aplica a tu hospital, escríbeme. No importa si es público o privado. Dos: si eres ingeniero o investigador en IA y estás en LATAM, estamos contratando. El equipo está en Lima pero trabajamos remoto. Buscamos gente que entienda la región. Tres: el episodio cinco es algo que no he visto hacer a ninguna startup de healthcare AI. Voy a entrevistar a un intérprete médico real. Alguien que lleva quince años interpretando en hospitales. Sin filtro. Vamos a hablar de lo que la tecnología no entiende todavía. Suscríbete." |
| 7:30–8:00 | End frame: Logo de Orquor + URL + "Estamos en Lima. Construimos para LATAM." + "Próximo episodio: Entrevista con un intérprete médico real." | "Soy Freddy. Orquor está en Lima, Perú. Si quieres ver cómo la IA para salud se construye desde Latinoamérica, quédate. Lo mejor está por venir." |

---

## Production notes

- B-roll: Mapa interactivo de LATAM con marcadores, calles de Lima (Miraflores/Barranco), oficina de Orquor, pantallas con código, estadísticas animadas, gráficos regulatorios.
- Camera: iPhone 15 Pro, 4K, locked focus.
- Audio: Rode Wireless ME. Verificar -16 LUFS.
- Lighting: Key Aputure MC 5600K, fill softbox.
- Background: Oficina con vista a ciudad LATAM. Auténtico, no set genérico.
- Editing: Descript. Auto-captions en español. Música de fondo sutil con carácter latinoamericano (sin caer en cliché).
- Lower third intro: "Freddy | Fundador, Orquor — Lima, Perú" — 4 segundos.

## Distribution

- YouTube main upload (16:9), publicar Día 17 a las 09:00 UTC-5
- Clip vertical de 60s del segmento [1:30–2:15] (estadísticas de necesidad real — alto impacto emocional)
- LinkedIn carousel con las 4 razones, publicar Día 18
- X thread (x-twitter/dia-017.md), publicar Día 18
- Clip específico para TikTok/Reels del segmento [0:00–0:20] (hook de VC + Lima)
