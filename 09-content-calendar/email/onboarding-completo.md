# Email Sequence — Onboarding Completo de Intérpretes (3 Emails)

**Trigger**: Intérprete contratado. Contrato firmado, BAA firmado, background check aprobado, documentación fiscal y bancaria en orden.
**Sequence**: 3 emails enviados con intervalo automático. Email 2 se dispara 3 días después de que Email 1 es abierto (o en día 4 si no hay confirmación de lectura). Email 3 se dispara en día 10.
**From**: `freddy@orquor.com`
**Language**: Español (LATAM)

---

## Email 1 — Bienvenida y primeros accesos (Día 0)

**Subject**: Bienvenido/a a ORQUOR, [First Name]

Hola [First Name],

Bienvenido/a a ORQUOR. Me alegra que estés acá.

Te escribo directamente porque los primeros días importan. Quiero que sepas exactamente qué esperar y que tengas una persona real al otro lado si algo no funciona. Esa persona soy yo por ahora. Cuando tengas mentor asignado —esta semana— te lo presento y él o ella pasa a ser tu primer punto de contacto.

**Lo que recibirás en las próximas 24 horas (emails separados, en este orden):**

1. **Cuenta ORQUOR** — Tu correo `[firstname]@orquor.com` con credenciales temporales. Cámbialas al primer login.
2. **Acceso a la consola** — `console.orquor.com`. Ahí verás tu dashboard, tu calendario de shifts, tu historial de sesiones, y el training center.
3. **Signal handle** — Nuestro canal de comunicación operativa. No usamos Slack para on-call; usamos Signal. Es más rápido y más seguro para comunicación clínica urgente.
4. **Documentación legal** — Copia firmada de tu BAA y tu contrato. Solo para tus registros. Ya están en nuestro sistema.

**Tu mentor/a será [Mentor Name].**

[Mentor Name] es intérprete médico/a certificado/a con [X] años de experiencia y fue quien verificó tu certificación en el proceso de selección. Él/Ella ya conoce tu perfil. Agenda una llamada de 30 minutos con [Mentor Name] esta semana. No es evaluación. Es para conocerse y resolver tus primeras preguntas.

**Lo que esperamos de ti esta primera semana:**

- Iniciar sesión en la consola y completar el tour guiado (15 minutos).
- Leer la Sección 4 del whitepaper ACTO: explica el rol del intérprete en la arquitectura. Está en `orquor.com/whitepaper-acto.pdf`.
- Agendar tu llamada con [Mentor Name].
- Configurar tu disponibilidad de shifts en la consola (así el scheduler te asigna correctamente).

Si algo no funciona, respondes a este correo. Lo leo en menos de 24 horas.

Bienvenido/a. En serio.

Freddy
Fundador, ORQUOR
freddy@orquor.com · orquor.com
Lima, Perú

---

## Email 2 — Observación y entrenamiento (Día 3–4)

**Subject**: Tus próximos 10 días en ORQUOR, [First Name]

Hola [First Name],

Ya deberías tener acceso a la consola y haber completado el tour guiado. Si no, avísame ahora y lo resolvemos.

Este email cubre lo que viene en los próximos 10 días: la fase de observación.

**Días 4–10: Modo observación**

Vas a observar sesiones reales en modo lectura. No interpretas. No intervienes. Estás en la sala virtual como observador/a silencioso/a.

Lo que verás:
- Cómo el motor de traducción procesa una consulta en vivo.
- Qué sucede cuando un verificador dispara una alerta (verás el flag, el motivo, y la decisión del orchestrator).
- Cómo el intérprete humano recibe una sesión escalada: qué información ve, qué herramientas tiene, cómo corrige.
- Cómo se construye el audit log por utterance.

Al final de esta fase deberías poder responder dos preguntas sin dudar:

1. *"¿Qué hace el orchestrator cuando un verificador falla?"*
2. *"¿Qué información contiene el audit log de una sesión y cómo se firma criptográficamente?"*

Si el día 10 no puedes responderlas con confianza, [Mentor Name] te hace una sesión uno-a-uno de 45 minutos. Sin costo para ti. Sin vergüenza. Preferimos invertir el tiempo ahora que corregir después.

**Acceso al Training Center**

En la consola, en la pestaña "Training", encontrarás:
- Simulaciones grabadas con traducciones reales anonimizadas (10 casos, urgencias y consulta externa).
- Ejercicios de decisión: "¿Qué harías si el verificador V23 dispara una alerta de dosis pediátrica?"
- El manual del intérprete ORQUOR (PDF interactivo, ~40 páginas).

Dedícale 2–3 horas distribuidas en la semana. No es un examen. Es para que llegues al día 11 con contexto real.

**Una cosa más**

En estos 10 días de observación, tu compensación es la acordada como "training rate" en tu contrato. Al pasar a producción plena (día 21), aplica la tarifa completa. Queremos que sepas que valoramos tu tiempo, incluso cuando estás aprendiendo el sistema.

Cualquier cosa, aquí estoy.

Freddy

---

## Email 3 — Entrada a producción y soporte continuo (Día 10)

**Subject**: Estás listo/a para producción, [First Name]

Hola [First Name],

Hoy termina tu fase de observación. [Mentor Name] me confirma que estás listo/a para la siguiente etapa: práctica supervisada. Y en 10 días más, producción plena.

Este es el plan.

**Días 11–20: Práctica supervisada**

Empiezas a manejar sesiones escaladas reales, con [Mentor Name] monitoreando en segundo plano. Cada traducción que produces queda registrada y [Mentor Name] la revisa dentro de 24 horas.

Lo que estamos midiendo en esta fase no es si eres buen intérprete (ya sabemos que sí, por eso te contratamos). Estamos midiendo dos cosas:

1. **Tasa de acuerdo** entre tu traducción y la traducción sugerida por el motor. Esperamos que tengas acuerdos altos —y divergencias cuando corresponde. Las divergencias documentadas son el training data más valioso que tenemos. Si corregiste al motor, explícalo en el campo de notas de la consola. Eso alimenta el modelo.

2. **Tiempo de respuesta.** El SLA para sesiones escaladas es 20 segundos desde que el orchestrator te asigna la utterance hasta que produces la traducción. En esta fase no hay penalización por excederlo. Es para que te acostumbres al ritmo.

**Día 21: Producción plena**

A partir del día 21:
- Eres nodo primario en el grafo de ruteo. Las sesiones escaladas te llegan directamente, sin mentor monitoring.
- Tu tarifa pasa a la tasa de producción plena (`[Production Rate]`, según tu contrato).
- Tus métricas de calidad y tiempo de respuesta se reportan mensualmente en tu dashboard, con fines de mejora continua, no de vigilancia. No hay quotas punitivas. Si tus métricas bajan, investigamos juntos qué está pasando antes de tomar cualquier decisión.

**Lo que quiero que sepas ahora que estás por entrar a producción**

Construimos ORQUOR con una hipótesis: que el intérprete humano, cuando está bien apoyado por tecnología, hace un trabajo más especializado, más valioso y mejor pagado. No menos trabajo. Mejor trabajo.

Los intérpretes en ORQUOR manejan menos minutos totales que en un call center de interpretación tradicional. Pero cada minuto que manejan es de alta consecuencia clínica. Y su trabajo queda documentado en un audit log que cualquier comité de calidad hospitalaria puede revisar. Eso es respaldo profesional real.

**Soporte continuo**

Tienes tres canales de soporte:
- **Operativo urgente**: Signal, canal de on-call. Respuesta en menos de 5 minutos.
- **Técnico / consola**: `soporte@orquor.com`. Respuesta en menos de 4 horas hábiles.
- **Profesional / mentoring**: Tu mentor asignado. Agenda sesiones 1:1 cuando quieras. No hay límite.

**Una invitación**

Si después de 60 días en producción quieres contribuir al diseño del producto —nuevos verificadores, mejoras al flujo de la consola, entrenamiento de nuevos intérpretes— dímelo. Los intérpretes que quieren participar en producto reciben compensación adicional por ese tiempo. Varios verificadores que están en producción ahora fueron sugeridos por intérpretes como tú.

Gracias por estar acá. En serio.

Freddy
Fundador, ORQUOR
freddy@orquor.com · orquor.com
Lima, Perú

---

**Notas para Hermes Recruiter-Bot**

La secuencia se dispara automáticamente cuando el estado del intérprete cambia a "onboarding" en el CRM interno.

Condiciones previas (verificadas por Compliance-Watcher):
- Contrato firmado ✓
- BAA firmado ✓
- Background check aprobado ✓
- Documentación fiscal (W-9 / RUC / equivalente) en archivo ✓
- Datos bancarios (Wise / Payoneer / banco local) confirmados ✓
- Cuenta de correo ORQUOR creada ✓
- Mentor asignado ✓

Email 1 se envía inmediatamente al cumplirse todas las condiciones.
Email 2 se envía 3 días después de que Email 1 es abierto (o en día 4 si no hay confirmación de lectura).
Email 3 se envía en día 10.

Variables a completar por la bot:
- `[First Name]` — del perfil del intérprete
- `[Mentor Name]` — de la asignación de mentor
- `[X]` años de experiencia del mentor — del perfil del mentor
- `[Production Rate]` — del contrato firmado

Human review: opcional para Email 1 y 2 (la bot los envía directamente). Obligatoria para Email 3 (contiene la tarifa de producción, validar que coincida con el contrato).
