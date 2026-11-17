# Encicla Analytics

Proyecto de portafolio: dashboard de Power BI sobre disponibilidad de bicicletas
del sistema Encicla (Valle de Aburrá), con datos recolectados por mí.

## Objetivo
1. Recolectar snapshots de todas las estaciones cada ~5 minutos durante 7 a 14 días.
2. Construir un modelo en estrella y un dashboard en Power BI (Power Query + DAX).
3. Publicar todo en GitHub con un README claro.

## Fuente de datos
GET https://webapp.metropol.gov.co/wsencicla/api/Disponibilidad/GetDisponibilidadMapas
Devuelve una lista de estaciones con: idZona, nameZona, id, name, address, lat, lon,
type (manual/automatica), capacity, bikes, places, closed, entre otros.
No he verificado que el endpoint siga activo: probarlo antes de construir nada.

## Decisiones ya tomadas
- Identificar estaciones por `id`, nunca por posición en la lista.
- Guardar timestamp en UTC con zona; convertir a America/Bogota en Power Query.
- Guardar TODAS las estaciones en cada lectura (formato largo: una fila por estación y lectura).
- `places` viene siempre en '0', así que los puestos libres = capacity - bikes.
- Calidad de datos: en estaciones manuales aparecen bikes > capacity (ej.: 83 bicicletas
  con capacidad 20). Verificar con datos completos y documentar el tratamiento en
  docs/decisions.md (tope al 100% o separar manuales de automáticas).
- Con muestreo de 5 min solo se observa variación neta, no tomas y entregas reales.
- Las ejecuciones de GitHub Actions se retrasan y no son exactas: no asumir intervalos regulares.

## Recolección
- GitHub Actions con cron cada 5 min, evitando el minuto 0, más workflow_dispatch.
- Antes de programar nada, ejecutar manualmente para confirmar que la API responde
  desde los servidores de GitHub (puede haber bloqueo de IPs de centros de datos).
- Los datos se commitean a la rama `data`; `main` solo contiene código y docs.

## Reglas
- No subir secretos, IDs de hojas de cálculo ni salidas de notebooks con datos sensibles.
- No incluir código ni datos de empleadores anteriores.
- Código, commits y README en inglés; conversación conmigo en español.
- Texto sin emojis y sin guiones largos.
- Explicar brevemente cada cambio importante antes de hacerlo.

## Estado actual
Nada implementado. Siguiente paso: collect.py y prueba local.