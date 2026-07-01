# API VeriCheck - Módulo de Seguridad y Despliegue (Grupo 6)

> **Proyecto:** Tech Solutions  
> **Componente:** Simulador de Servicio Externo de Validación de Identidad (VeriCheck)  
> **Tecnologías:** Python 3.10+ | FastAPI | Uvicorn  

---

## Descripción del Módulo

Este componente de software pertenece al **Grupo 6**. Cumple la función de simular la API externa **VeriCheck**, requerida en el flujo de negocio para validar la autenticidad de los clientes y mitigar riesgos de fraude antes de procesar operaciones sensibles en la plataforma de la consultora.

Cuenta con políticas de seguridad perimetral (**CORS** habilitado) y un **mecanismo automático de Logs de Auditoría** que registra en la consola del servidor cada petición con su respectiva estampa de tiempo e IP de origen.

---

## Endpoints (Puntos de Conexión)

La API expone los siguientes extremos para que los demás grupos puedan integrarse:

### Control de Estado (Health Check)
* **URL:** `GET /health`
* **Descripción:** Permite verificar si el servicio de VeriCheck está online en el servidor.
* **Respuesta exitosa (HTTP 200):**
```json
{
  "status": "online",
  "grupo": "Grupo 6 - Seguridad y Despliegue"
}

### Validación de Identidad
* **URL:** POST /validar
* **Descripción:** Recibe los datos del cliente y ejecuta las reglas de negocio de seguridad.

**Estructura requerida del Cuerpo (JSON Body):**
```json
{
  "dni_cuil": "42333444",
  "nombre_empresa": "Tech Solutions SRL"
}

### Escenarios de Prueba e Integración (Casos de Uso)
* Para facilitar el testeo a los otros equipos del curso, la API tiene programadas las siguientes respuestas basadas en los códigos de estado HTTP estándar:

```json
Escenario de NegocioEntrada de Prueba (dni_cuil)Código HTTPEstado en JSONCamino Feliz (Éxito)Cualquier DNI válido (ej: 35123456)200 OKValidacion_ExitosaControl de Fraude11111111403 ForbiddenValidacion_FallidaError de FormatoMenos de 7 dígitos o letras (ej: abc)422 UnprocessableDatos_InvalidosCampos Vacíos"" (Vacío)400 Bad RequestError detallado

### Instalación y Ejecución Local
**Si querés correr este módulo en tu máquina para hacer pruebas locales, seguí estos pasos:**

* **Clonar el repositorio:**
```json
git clone [https://github.com/tiagoonorato-dv/api-vericheck-grupo6.git](https://github.com/tiagoonorato-dv/api-vericheck-grupo6.git)
cd api-vericheck-grupo6]

* **Instalar las dependencias obligatorias:**
```json
pip install -r requirements.txt

* **Iniciar el servidor de desarrollo:**
```json
uvicorn main:app --reload

* **Interfaz de Pruebas Interactiva (Swagger):**
Una vez encendido, ingresá desde tu navegador a: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
