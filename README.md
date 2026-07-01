# API VeriCheck 2FA - Módulo de Seguridad y Despliegue (Grupo 6)

> **Proyecto:** Tech Solutions  
> **Componente:** Simulador de Validación de Identidad con Doble Factor de Autenticación (2FA)  
> **Tecnologías:** Python 3.10+ | FastAPI | Uvicorn

---

# Descripción del Módulo

Este componente pertenece al **Grupo 6**.

Implementa un flujo estricto de **Autenticación de Dos Pasos (2FA)**. En el primer paso se validan las reglas de negocio perimetrales y de prevención de fraude. Si la validación es exitosa, el sistema genera un **token dinámico de 6 dígitos**, que debe ser verificado en un segundo paso para completar el proceso de autenticación y otorgar el acceso final.

---

# Endpoints (Flujo de Conexión 2FA)

La API expone los siguientes endpoints para que los demás grupos puedan integrarse.

## Paso 1: Solicitud de Validación de Identidad

**URL**

`POST /validar`

**Descripción**

Valida los datos del cliente y genera un token temporal de 6 dígitos, el cual puede visualizarse en la consola del servidor.

**Body (JSON)**

```json
{
  "dni_cuil": "42333444",
  "nombre_empresa": "Tech Solutions SRL"
}
```

---

## Paso 2: Verificación del Token de Seguridad

**URL**

`POST /verificar-token`

**Descripción**

Recibe el código dinámico generado previamente y completa el proceso de autenticación.

**Body (JSON)**

```json
{
  "dni_cuil": "42333444",
  "token": "AQUÍ_EL_CÓDIGO_DE_6_DÍGITOS"
}
```

---

# Escenarios de Prueba

| Escenario | Endpoint | Datos | Resultado Esperado |
|-----------|----------|-------|--------------------|
| Camino Feliz (Paso 1) | `/validar` | Cualquier DNI válido | `Paso1_Exitoso` (genera token en consola) |
| Camino Feliz (Paso 2) | `/verificar-token` | DNI válido + Token correcto | **200 OK** - `Validacion_Exitosa` |
| Control de Fraude | `/validar` | DNI `11111111` | **403 Forbidden** |
| Token Erróneo | `/verificar-token` | DNI válido + Token incorrecto | **401 Unauthorized** |

---

# Instalación y Ejecución Local

## 1. Clonar el repositorio

```bash
git clone https://github.com/tiagoonorato-dv/api-vericheck-grupo6.git
cd api-vericheck-grupo6
```

## 2. Instalar las dependencias

```bash
pip install -r requirements.txt
```

## 3. Ejecutar el servidor

```bash
uvicorn main:app --reload
```

---

# Documentación Interactiva (Swagger)

Una vez iniciado el servidor, acceder desde el navegador a:

```text
http://127.0.0.1:8000/docs
```

---

# Tecnologías Utilizadas

- Python 3.10+
- FastAPI
- Uvicorn

---

# Autor

**Grupo 6 - Seguridad y Despliegue**
