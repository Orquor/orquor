# Política de Privacidad — Orquor S.A.C.

**Versión 2026-05** · Última actualización: [fecha de publicación]

Esta Política de Privacidad describe cómo Orquor S.A.C. ("Orquor", "nosotros", "nuestro") recolecta, usa, almacena, transfiere y protege los datos personales tratados en el contexto de los servicios de orquestación de traducción clínica y demás productos de la familia Orquor.

Esta Política se rige por la **Ley N° 29733 — Ley de Protección de Datos Personales del Perú**, su reglamento aprobado por Decreto Supremo N° 003-2013-JUS, y normas conexas. Donde aplique, también atendemos el Reglamento General de Protección de Datos de la Unión Europea (GDPR), la Lei Geral de Proteção de Dados (LGPD) del Brasil, y el régimen HIPAA de los Estados Unidos cuando los servicios involucren a Covered Entities estadounidenses.

---

## 1. Identificación del titular de la base de datos

**Razón social**: Orquor S.A.C.
**RUC**: [completar]
**Domicilio**: [completar — Lima, Perú]
**Correo de privacidad**: privacy@orquor.com
**Responsable de protección de datos**: [nombre del DPO o, en su defecto, del fundador]

## 2. Datos personales que tratamos

### 2.1 Datos del personal clínico (usuarios de la plataforma)
- Nombre completo, correo electrónico institucional, número de matrícula profesional, institución a la que pertenece.

### 2.2 Datos del paciente (recolectados indirectamente vía la institución cliente)
- Identificador interno asignado por la institución (no DNI directo, salvo necesidad clínica documentada).
- Audio de la conversación clínica en idioma origen.
- Transcripción producida por el componente ASR.
- Traducción producida por el componente MT.
- Resultado del verificador outcome-based aplicado a cada utterance.
- Marca temporal criptográfica (RFC 3161 / OpenTimestamps).

**Nota crítica**: el audio crudo se procesa en modo "Confidential Computing" en GPU (NVIDIA H100 confidential mode), de modo que ni el sistema operativo del host ni el personal técnico de Orquor pueden leer el contenido en claro.

### 2.3 Datos de contacto comercial
- Para prospects y clientes corporativos: nombre, rol, organización, correo, teléfono, eventos de engagement.

## 3. Finalidades del tratamiento

Tratamos los datos personales para las siguientes finalidades:

1. **Prestación del servicio de traducción clínica** (Orquor Clinical) — finalidad principal.
2. **Generación de logs de auditoría inmutables** que el cliente puede invocar ante eventos adversos, auditorías regulatorias o procesos legales.
3. **Mejora de los modelos de ASR y traducción** mediante datasets agregados de-identificados con técnicas de privacidad diferencial. Esta finalidad requiere consentimiento expreso adicional del cliente institucional y de los titulares cuando aplique.
4. **Cumplimiento regulatorio**, incluyendo notificación de incidentes, auditorías SBS / SUSALUD / DGAJ-MINJUS / OCR-HHS / ANPD / ANVISA según corresponda.
5. **Contacto comercial** con prospects y clientes que hayan manifestado interés.

## 4. Base legal del tratamiento

- Para el servicio principal: el contrato comercial entre Orquor y la institución cliente (Art. 14, num. 1 de la Ley 29733: cumplimiento de obligaciones derivadas de relación jurídica).
- Para finalidades secundarias (mejora de modelos, contacto comercial directo): consentimiento previo, expreso, informado e inequívoco del titular, conforme al Art. 13 de la Ley 29733.

## 5. Transferencias internacionales

Algunos componentes de procesamiento ocurren en infraestructura ubicada en los Estados Unidos (Lambda Labs US-West, para failover N+1), Brasil (eventual segunda región LATAM) o la Unión Europea (proveedores de almacenamiento cifrado).

Estas transferencias se realizan bajo los siguientes resguardos:
- Cláusulas Contractuales Tipo de la Autoridad Nacional de Protección de Datos Personales (ANPDP) del Perú.
- Standard Contractual Clauses (SCCs) de la Comisión Europea cuando hay transferencias a/desde la UE.
- Encriptación at-rest y in-transit en todas las transferencias.
- Confidential Computing donde técnicamente disponible.

## 6. Conservación de los datos

| Tipo de dato | Plazo de conservación |
|---|---|
| Audio crudo de sesión clínica | 30 días (siempre cifrado y en enclave confidential computing) |
| Transcripción ASR | 7 años (alineado a plazos de conservación de historia clínica peruana) |
| Traducción MT | 7 años (idem) |
| Logs de auditoría con timestamp criptográfico | 10 años |
| Datos de contacto comercial | Hasta revocación del consentimiento |

## 7. Derechos del titular

Conforme al Capítulo III de la Ley 29733, el titular tiene derecho a:

- **Información** sobre el tratamiento de sus datos.
- **Acceso** a sus datos en posesión de Orquor.
- **Actualización, inclusión, rectificación y supresión**.
- **Oposición** al tratamiento cuando la base legal lo permita.
- **Cancelación** cuando no sean necesarios para la finalidad.
- **Portabilidad** de los datos en formato estructurado y de uso común.

Para ejercer estos derechos, escribir a **privacy@orquor.com** desde una dirección que permita razonablemente verificar la identidad. El tiempo máximo de respuesta es de **veinte (20) días hábiles**, conforme al Art. 19 de la Ley.

Adicionalmente, el titular tiene derecho a presentar reclamo ante la **Autoridad Nacional de Protección de Datos Personales (ANPDP-MINJUS)** del Perú.

## 8. Seguridad

Orquor implementa medidas de seguridad técnicas, administrativas y físicas conforme a la Directiva de Seguridad de la Información de la ANPDP. Las medidas incluyen, sin limitarse a:

- Cifrado de datos en reposo (AES-256) y en tránsito (TLS 1.2+).
- Confidential Computing en GPU para datos sensibles.
- Timestamping criptográfico de logs (RFC 3161).
- Controles de acceso con autenticación multifactor (MFA).
- Auditorías de seguridad periódicas con terceros independientes.
- Política de notificación de incidentes en máximo 48 horas hábiles desde detección.

## 9. Cookies y tecnologías similares

El sitio web orquor.com utiliza cookies estrictamente necesarias para el funcionamiento (autenticación, preferencias de sesión) y cookies analíticas anonimizadas (Plausible Analytics, sin tracking individual). No utilizamos cookies publicitarias de terceros.

## 10. Cambios en esta Política

Notificaremos cambios materiales a esta Política con al menos quince (15) días de anticipación en orquor.com/legal/privacy y, cuando aplique, por correo electrónico a usuarios con cuenta activa.

## 11. Contacto

Para preguntas sobre esta Política: **privacy@orquor.com**
Para reclamos ANPDP: https://www.minjus.gob.pe/proteccion-datos-personales/

---

**Inscripción en el Registro Nacional de Protección de Datos Personales (RNPDP) del MINJUS**: pendiente de número de registro al momento de publicación. Será actualizado en cuanto la inscripción esté completa.
