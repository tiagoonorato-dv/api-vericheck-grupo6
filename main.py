from fastapi import FastAPI, Request, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
import random

app = FastAPI(
    title="API VeriCheck 2FA - Grupo 6",
    description="Servicio de Autenticación de Dos Pasos (2FA) con Tokens Temporales",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


base_tokens = {}

class DatosPaso1(BaseModel):
    dni_cuil: str
    nombre_empresa: str

class DatosPaso2(BaseModel):
    dni_cuil: str
    token: str

@app.get("/health", status_code=status.HTTP_200_OK)
def health_check():
    return {
        "status": "online",
        "grupo": "Grupo 6 - Seguridad y Despliegue (2FA Activo)"
    }


@app.post("/validar", status_code=status.HTTP_200_OK)
def paso_1_solicitar_token(info: DatosPaso1, request: Request):
    dni_recibido = info.dni_cuil.strip()
    empresa_recibida = info.nombre_empresa.strip()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ip_cliente = request.client.host
    
    
    if not dni_recibido or not empresa_recibida:
        raise HTTPException(status_code=400, detail="Campos obligatorios vacíos.")

    
    if dni_recibido == "11111111":
        print(f"[{timestamp}] [AUDITORIA 🚨] IP: {ip_cliente} | DNI: {dni_recibido} | Bloqueado por Fraude")
        raise HTTPException(status_code=403, detail="Validacion_Fallida: Alertas activas por intento de fraude.")
        
    if not dni_recibido.isdigit() or len(dni_recibido) < 7:
        raise HTTPException(status_code=422, detail="Formato de documento inválido.")
    
    
    token_generado = str(random.randint(100000, 999999))
    
    
    base_tokens[dni_recibido] = token_generado
    
    
    print("\n" + "="*50)
    print(f"[{timestamp}] [✉️ SMS/MAIL SIMULATOR] Enviando a {empresa_recibida}")
    print(f"👉 TOKEN SEGURO (2FA) PARA DNI {dni_recibido}: [ {token_generado} ]")
    print("="*50 + "\n")
    
    print(f"[{timestamp}] [AUDITORIA ✅] IP: {ip_cliente} | DNI: {dni_recibido} | Paso 1 Exitoso. Esperando verificación de token.")
    
    return {
        "status": "Paso1_Exitoso",
        "mensaje": "Datos correctos. Segundo factor requerido. Ingrese el token enviado para finalizar.",
        "proveedor": "VeriCheck 2FA"
    }


@app.post("/verificar-token", status_code=status.HTTP_200_OK)
def paso_2_verificar_token(info: DatosPaso2, request: Request):
    dni_recibido = info.dni_cuil.strip()
    token_ingresado = info.token.strip()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ip_cliente = request.client.host
    
    
    if dni_recibido not in base_tokens:
        print(f"[{timestamp}] [AUDITORIA ⚠️] IP: {ip_cliente} | DNI: {dni_recibido} | Intentó validar token sin Paso 1")
        raise HTTPException(status_code=400, detail="Error: No se ha solicitado un token previo para este documento.")
        
    
    token_correcto = base_tokens[dni_recibido]
    
    if token_ingresado != token_correcto:
        print(f"[{timestamp}] [AUDITORIA ❌] IP: {ip_cliente} | DNI: {dni_recibido} | Token Incorrecto: {token_ingresado}")
        raise HTTPException(status_code=401, detail="Token inválido o expirado. Acceso denegado.")
        
    
    del base_tokens[dni_recibido]
    
    print(f"[{timestamp}] [AUDITORIA 🔑] IP: {ip_cliente} | DNI: {dni_recibido} | Autenticación 2FA COMPLETADA CON ÉXITO")
    
    return {
        "status": "Validacion_Exitosa",
        "mensaje": f"Identidad confirmada mediante segundo factor de autenticación (2FA).",
        "proveedor": "VeriCheck 2FA"
    }