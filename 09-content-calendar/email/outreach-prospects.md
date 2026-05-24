# Email — Outreach Frío a Hospitales Prospecto (CR y CO)

**Trigger**: Campaña de prospección outbound a directores médicos / jefes de calidad de hospitales en Costa Rica y Colombia.
**From**: `freddy@orquor.com`
**Subject**: ORQUOR Clinical — interpretación clínica con verificación automática para [Hospital Name]

---

Estimado/a Dr./Dra. [Last Name],

Le escribo porque [Hospital Name] aparece en los registros públicos de acreditación de [Joint Commission International / ICONTEC / Ministerio de Salud] como una institución que mide y audita sus procesos clínicos. Eso me dice que la precisión en la comunicación con pacientes que no dominan el español es un tema que su equipo ya toma en serio.

Mi nombre es Freddy, soy el fundador de ORQUOR. Hemos construido un sistema de traducción clínica que no depende de un solo modelo de inteligencia artificial. Usamos una arquitectura que llamamos ACTO (Auditable Clinical Translation Orchestration): un motor de traducción asistido por sesenta verificadores automáticos que actúan como una segunda opinión en tiempo real. Si algún verificador detecta riesgo —una dosis pediátrica mal convertida, una contraindicación omitida, un término anatómico ambiguo— la traducción no se entrega. Escala a un intérprete humano certificado.

El resultado es un sistema donde cada utterance traducida tiene un audit log criptográficamente verificable. No es una caja negra. Es trazabilidad clínica de extremo a extremo.

**Lo que propongo**

Una demo de 30 minutos de ORQUOR Clinical, enfocada en las especialidades que más volumen de interpretación generan en [Hospital Name]. No es un webinar genérico. Preparo la demo sobre escenarios clínicos reales de su institución —si usted me comparte las áreas de mayor fricción— o sobre casos representativos de su perfil: [emergencias / obstetricia / pediatría / consulta externa].

La demo cubre tres cosas:

1. Cómo el motor traduce una consulta en vivo y qué sucede cuando un verificador dispara una alerta.
2. Cómo se ve el audit log después de una sesión —qué datos quedan, cómo se firman, qué puede auditar el comité de calidad del hospital.
3. Cómo integramos con el EHR del hospital vía FHIR R4, sin reemplazar su flujo actual.

No pido una decisión. Pido treinta minutos para que usted juzgue si la arquitectura tiene sentido clínico para su institución.

El whitepaper completo de ACTO está disponible en orquor.com/whitepaper-acto.pdf. Si prefiere leer antes de hablar, por ahí puede empezar. Y si quiere que se lo envíe impreso, deme una dirección y se lo mando.

Quedo atento. Gracias por su tiempo.

Freddy
Fundador, ORQUOR
freddy@orquor.com · orquor.com
Signal: [número]
Lima, Perú

---

## Hospitales Prospecto — Costa Rica (5)

| # | Hospital | Ciudad | Perfil | Contacto sugerido |
|---|----------|--------|--------|-------------------|
| 1 | Hospital Clínica Bíblica | San José | JCI-acreditado, alta complejidad, atención a pacientes internacionales | Dirección Médica / Calidad |
| 2 | Hospital CIMA San José | Escazú | Grupo hospitalario privado, obstetricia y cirugía de alta complejidad | Dirección Médica |
| 3 | Hospital México | San José | Público, Caja Costarricense de Seguro Social, mayor volumen de atención del país | Jefatura de Calidad / Dirección |
| 4 | Hospital Nacional de Niños | San José | Pediátrico de referencia nacional, población migrante significativa | Dirección Médica |
| 5 | Hospital San Juan de Dios | San José | Público general, Caja Costarricense de Seguro Social, emergencias 24h | Jefatura de Emergencias / Calidad |

## Hospitales Prospecto — Colombia (5)

| # | Hospital | Ciudad | Perfil | Contacto sugerido |
|---|----------|--------|--------|-------------------|
| 6 | Fundación Santa Fe de Bogotá | Bogotá | JCI-acreditado, universitario, atención a pacientes internacionales | Dirección Médica / Innovación |
| 7 | Hospital Universitario San Ignacio | Bogotá | Universitario (Pontificia Universidad Javeriana), alta complejidad | Dirección Médica / Docencia |
| 8 | Hospital Pablo Tobón Uribe | Medellín | Acreditado ICONTEC, referente en calidad y seguridad del paciente | Dirección de Calidad |
| 9 | Fundación Valle del Lili | Cali | Alta complejidad, JCI-acreditado, centro de referencia del suroccidente colombiano | Dirección Médica |
| 10 | Clínica Universidad de La Sabana | Chía | Universitario, enfoque en innovación tecnológica en salud | Dirección Médica / Innovación |

---

**Notas para Hermes Sales-Bot**

Este template es para primer contacto frío (no hay relación previa, no hay referral, no hay interacción en redes sociales).

Reglas de envío:
- Investigar el nombre correcto del director médico o jefe de calidad antes de enviar. No enviar a info@ ni a buzones genéricos.
- Si el hospital tiene acreditación JCI o ICONTEC, mencionarlo en el primer párrafo como arriba. Si no, eliminar la referencia y empezar directamente con la propuesta.
- Usar el nombre real del hospital en el subject line, no la variable [Hospital Name].
- Adjuntar el whitepaper ACTO solo si el destinatario lo solicita. En el primer contacto, incluir el enlace. El PDF adjunto puede disparar filtros de spam corporativos.
- Personalizar la selección de especialidades en "La demo cubre tres cosas" según el perfil del hospital (tabla arriba).
- Human review obligatoria antes de envío. La bot redacta el 90%. Freddy revisa y personaliza los últimos detalles.
- Si no hay respuesta en 7 días, activar follow-up-prospects.md.
