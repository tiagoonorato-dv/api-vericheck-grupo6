from fastapi import FastAPI, Request, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime

app = FastAPI(
    title="API VeriCheck Premium - Grupo 6",
    description="Servicio de validación de identidad con códigos de estado HTTP y auditoría integrada",
    version="1.3.0"
)

# Habilitar CORS para evitar bloqueos entre grupos
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class DatosCliente(BaseModel):
    dni_cuil: str
    nombre_empresa: str

# MEJORA: Endpoint de Health Check (para ver si la API está viva en Render sin mandar datos)
@app.get("/health", status_code=status.HTTP_200_OK)
def health_check():
    return {
        "status": "online",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "grupo": "Grupo 6 - Seguridad y Despliegue"
    }

@app.post("/validar", status_code=status.HTTP_200_OK)
def punto_conexion_validacion(info: DatosCliente, request: Request):
    dni_recibido = info.dni_cuil.strip()
    empresa_recibida = info.nombre_empresa.strip()
    timestamp_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ip_cliente = request.client.host
    
    # 1. Validar campos vacíos
    if not dni_recibido or not empresa_recibida:
        print(f"[{timestamp_actual}] [AUDITORIA LOG] IP: {ip_cliente} | Acción: Intento_Validacion | Resultado: Datos_Incompletos ⚠️")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El DNI/CUIL y el Nombre de Empresa son campos obligatorios y no pueden estar vacíos."
        )

    # 2. Control de Fraude (Lista negra) -> Devuelve un 403 Forbidden (Acceso denegado/prohibido)
    if dni_recibido == "11111111":
        print(f"[{timestamp_actual}] [AUDITORIA LOG] IP: {ip_cliente} | DNI: {dni_recibido} | Acción: Validar | Resultado: Alerta_Fraude 🚨")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Validacion_Fallida: El documento ingresado posee alertas activas por intento de fraude en VeriCheck."
        )
        
    # 3. Validación de formato técnico -> Devuelve un 422 Unprocessable Entity
    if not dni_recibido.isdigit() or len(dni_recibido) < 7:
        print(f"[{timestamp_actual}] [AUDITORIA LOG] IP: {ip_cliente} | Entrada: {dni_recibido} | Acción: Validar | Resultado: Formato_Invalido")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Datos_Invalidos: El formato del documento debe contener únicamente números (mínimo 7 dígitos)."
        )
    
    # 4. Flujo Principal Exitoso
    print(f"[{timestamp_actual}] [AUDITORIA LOG] IP: {ip_cliente} | DNI: {dni_recibido} | Empresa: {empresa_recibida} | Resultado: Exitoso ✅")
    return {
        "status": "Validacion_Exitosa",
        "mensaje": f"Identidad confirmada para '{empresa_recibida}'. Documento válido.",
        "proveedor": "VeriCheck"
    }