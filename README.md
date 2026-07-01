# API VeriCheck - Grupo 6 (Seguridad y Despliegue)

Este componente simula el servicio externo **VeriCheck** para la validación de identidad de clientes y control de fraude en la plataforma de la consultora.

## Endpoints Disponibles
* **GET `/health`**: Verifica si el servidor está online.
* **POST `/validar`**: Procesa la validación de un cliente.

### Formato de Entrada (JSON)
```json
{
  "dni_cuil": "42333444",
  "nombre_empresa": "Tech Solutions SRL"
}