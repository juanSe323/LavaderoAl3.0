# Manual de Usuario - Lavadero AL

## Bienvenido a Lavadero AL

Este manual te guiará paso a paso en el uso del sistema de gestión de lavadero. Está diseñado para usuarios sin conocimientos técnicos.

## Tabla de Contenidos

- [Inicio de Sesión](#inicio-de-sesión)
- [Dashboard (Panel Principal)](#dashboard-panel-principal)
- [Gestión de Empleados](#gestión-de-empleados)
- [Registro de Servicios](#registro-de-servicios)
- [Control de Inventario](#control-de-inventario)
- [Convenios Empresariales](#convenios-empresariales)
- [Generación de Liquidaciones](#generación-de-liquidaciones)
- [Tarifas](#tarifas)
- [Reportes](#reportes)
- [Preguntas Frecuentes](#preguntas-frecuentes)


---

## Dashboard (Panel Principal)

El Dashboard es la primera pantalla que ves al iniciar sesión. Muestra información resumida de tu lavadero.

### Información Visible

#### Tarjetas de Resumen

**Servicios del Mes:**
- Total de servicios realizados
- Monto total generado
- Promedio por servicio

**Empleados:**
- Número de empleados activos
- Empleado más productivo del mes

**Inventario:**
- Productos con stock bajo
- Valor total del inventario

**Convenios:**
- Convenios activos
- Servicios realizados a empresas

#### Gráfico de Servicios

- Muestra la cantidad de servicios por día
- Útil para identificar días de mayor demanda

### Navegación

Usa el menú lateral izquierdo para acceder a las diferentes secciones:

- **Dashboard:** Resumen general
- **Servicios:** Registro y consulta de servicios
- **Empleados:** Gestión de personal
- **Inventario:** Control de productos
- **Convenios:** Empresas con acuerdo especial
- **Liquidaciones:** Pagos a empleados
- **Tarifas:** Precios por tipo de vehículo
- **Reportes:** Informes y estadísticas

---

## Gestión de Empleados

### Ver Lista de Empleados

1. Haz clic en "Empleados" en el menú lateral
2. Verás una tabla con todos los empleados
3. La tabla muestra:
   - Nombre
   - Cédula
   - Teléfono
   - Email
   - Porcentaje de comisión
   - Estado (Activo/Inactivo)

### Agregar un Nuevo Empleado

1. Haz clic en el botón "Nuevo Empleado"
2. Completa el formulario:
   - **Nombre completo:** Ej: "Juan Pérez García"
   - **Cédula:** Documento de identidad
   - **Teléfono:** Número de contacto
   - **Email:** Correo electrónico (opcional)
   - **Porcentaje de comisión:** Entre 0 y 100 (Ej: 15 significa 15%)
3. Haz clic en "Guardar"
4. Verás un mensaje de confirmación

### Editar un Empleado

1. En la lista de empleados, haz clic en el botón "Editar" (ícono de lápiz)
2. Se abrirá el formulario con los datos actuales
3. Modifica los campos que desees
4. Haz clic en "Actualizar"

### Desactivar un Empleado

1. Haz clic en el botón "Eliminar" (ícono de basura)
2. Confirma la acción
3. El empleado quedará marcado como "Inactivo"
4. No se elimina de la base de datos

### Reactivar un Empleado

1. Los empleados inactivos aparecen con una marca distintiva
2. Haz clic en "Reactivar"
3. El empleado volverá a estar activo

---

## Registro de Servicios

### Ver Servicios Realizados

1. Haz clic en "Servicios" en el menú
2. Verás una tabla con todos los servicios registrados
3. Puedes ver:
   - Fecha y hora
   - Placa del vehículo
   - Tipo de vehículo
   - Tipo de servicio
   - Empleado que lo realizó
   - Monto

### Registrar un Nuevo Servicio

1. Haz clic en "Nuevo Servicio"
2. Completa el formulario:

   **Datos del Vehículo:**
   - **Placa:** Ej: "ABC123"
   - **Tipo de vehículo:** Selecciona entre:
     - Auto
     - SUV
     - Camioneta
     - Camión

   **Datos del Servicio:**
   - **Tipo de servicio:** Ej: "Lavado completo", "Lavado express", etc.
   - **Monto total:** Precio del servicio
   - **Empleado:** Selecciona quién realizó el servicio

   **Opcional (si aplica convenio):**
   - **Convenio:** Selecciona la empresa si el vehículo tiene convenio
   - **Descuento:** Se calcula automáticamente según el convenio
   - **Observaciones:** Notas adicionales

3. Haz clic en "Guardar"

### Filtrar Servicios

Puedes filtrar los servicios por:
- Rango de fechas
- Tipo de vehículo
- Empleado

### Exportar a Excel

1. Haz clic en el botón "Exportar a Excel"
2. Se descargará un archivo con todos los servicios
3. Útil para llevar registros externos

---

## Control de Inventario

### Ver Inventario Actual

1. Haz clic en "Inventario" en el menú
2. Verás una tabla con todos los productos:
   - Nombre del producto
   - Categoría
   - Stock actual
   - Stock mínimo
   - Precio unitario
   - Unidad de medida
   - Estado (Normal/Bajo/Crítico)

### Alertas de Stock

- **Verde:** Stock normal
- **Amarillo:** Stock bajo (cerca del mínimo)
- **Rojo:** Stock crítico (por debajo del mínimo)

### Agregar Nuevo Producto

1. Haz clic en "Nuevo Producto"
2. Completa:
   - **Nombre:** Ej: "Champú Premium"
   - **Categoría:** Ej: "Limpieza", "Acabado", "Herramientas"
   - **Stock inicial:** Cantidad actual
   - **Stock mínimo:** Alerta cuando llegue a este nivel
   - **Precio unitario:** Costo del producto
   - **Unidad:** Litro, Kilo, Unidad, etc.
   - **Descripción:** Información adicional
3. Haz clic en "Guardar"

### Registrar Movimiento de Inventario

#### Entrada de Productos (Compra)

1. Haz clic en "Registrar Movimiento"
2. Selecciona el producto
3. Tipo de movimiento: "Entrada"
4. Cantidad: Cantidad que ingresa
5. Motivo: Ej: "Compra a proveedor"
6. Haz clic en "Registrar"
7. El stock se incrementará automáticamente

#### Salida de Productos (Uso)

1. Mismo proceso que entrada
2. Tipo de movimiento: "Salida"
3. Motivo: Ej: "Uso en servicios del día"
4. El stock se reducirá automáticamente

#### Ajuste de Inventario

1. Tipo de movimiento: "Ajuste"
2. Usar cuando hay diferencias por inventario físico
3. Motivo: Ej: "Ajuste por conteo físico"

### Ver Historial de Movimientos

1. Haz clic en un producto
2. Selecciona "Ver Movimientos"
3. Verás el historial completo:
   - Fecha
   - Tipo de movimiento
   - Cantidad
   - Stock anterior y nuevo
   - Motivo
   - Usuario que registró

---

## Convenios Empresariales

### ¿Qué es un Convenio?

Un convenio es un acuerdo especial con empresas que tienen flotas de vehículos. Permite aplicar descuentos automáticos.

### Ver Convenios Activos

1. Haz clic en "Convenios" en el menú
2. Verás:
   - Nombre de la empresa
   - NIT
   - Tipo de descuento
   - Valor del descuento
   - Estado
   - Cantidad de vehículos registrados

### Crear un Nuevo Convenio

1. Haz clic en "Nuevo Convenio"
2. Completa:

   **Datos de la Empresa:**
   - **Nombre:** Ej: "Transportes XYZ S.A."
   - **NIT:** Número de identificación
   - **Contacto:** Nombre del encargado
   - **Teléfono:** Número de contacto
   - **Email:** Correo electrónico
   - **Dirección:** Dirección de la empresa

   **Datos del Convenio:**
   - **Tipo de descuento:**
     - **Porcentaje:** Ej: 15% de descuento
     - **Monto fijo:** Ej: $5.000 de descuento
   - **Valor del descuento:** Según el tipo elegido
   - **Fecha de inicio:** Cuándo inicia el convenio
   - **Fecha de término:** Cuándo vence (opcional)
   - **Observaciones:** Notas adicionales

3. Haz clic en "Guardar"

### Agregar Vehículos a un Convenio

1. En la lista de convenios, haz clic en "Ver Vehículos"
2. Haz clic en "Agregar Vehículo"
3. Completa:
   - **Placa:** Ej: "XYZ789"
   - **Tipo de vehículo:** Auto, SUV, etc.
   - **Modelo:** Ej: "Toyota Hilux 2022"
   - **Color:** Ej: "Blanco"
4. Haz clic en "Guardar"

### Usar un Convenio al Registrar Servicio

1. Al registrar un servicio, selecciona el convenio en el formulario
2. El descuento se aplicará automáticamente
3. El monto final se ajustará según el convenio

---

## Generación de Liquidaciones

### ¿Qué es una Liquidación?

Una liquidación es el cálculo de pago a un empleado basado en:
- Servicios realizados en un período
- Porcentaje de comisión del empleado

### Ver Liquidaciones

1. Haz clic en "Liquidaciones" en el menú
2. Verás todas las liquidaciones:
   - Empleado
   - Período (fecha inicio - fecha fin)
   - Total de servicios
   - Monto total
   - Comisión calculada
   - Estado (Pendiente/Pagada)

### Crear una Nueva Liquidación

1. Haz clic en "Nueva Liquidación"
2. Selecciona:
   - **Empleado:** De la lista de empleados activos
   - **Fecha de inicio:** Inicio del período
   - **Fecha de fin:** Fin del período
3. Haz clic en "Generar Liquidación"
4. El sistema calculará automáticamente:
   - Todos los servicios del empleado en ese período
   - Comisión según su porcentaje

### Ver Detalle de Liquidación

1. Haz clic en "Ver Detalle" en una liquidación
2. Verás:
   - Lista de todos los servicios incluidos
   - Fecha de cada servicio
   - Placa del vehículo
   - Monto del servicio
   - Comisión calculada
   - Total a pagar

### Marcar Liquidación como Pagada

1. En una liquidación pendiente, haz clic en "Marcar como Pagada"
2. Confirma la acción
3. Se registrará la fecha de pago
4. El estado cambiará a "Pagada"

### Ejemplo de Cálculo

**Datos:**
- Empleado: Juan Pérez
- Porcentaje de comisión: 15%
- Período: 01/01/2024 al 15/01/2024
- Servicios realizados: 10 servicios
- Monto total de servicios: $250.000

**Cálculo:**
- Comisión = $250.000 × 15% = $37.500
- Juan Pérez recibirá $37.500

---

## Tarifas

### Ver Tarifas Actuales

1. Haz clic en "Tarifas" en el menú
2. Verás los precios por tipo de vehículo:
   - Auto
   - SUV
   - Camioneta
   - Camión

### Actualizar una Tarifa

1. Haz clic en "Editar" junto al tipo de vehículo
2. Ingresa el nuevo precio
3. Haz clic en "Actualizar"
4. El nuevo precio se aplicará a los siguientes servicios

**Nota:** Cambiar la tarifa no afecta servicios ya registrados.

---

## Reportes

### Reporte de Servicios

1. Haz clic en "Reportes" en el menú
2. Selecciona "Reporte de Servicios"
3. Define:
   - Fecha de inicio
   - Fecha de fin
   - Tipo de vehículo (opcional)
   - Empleado (opcional)
4. Haz clic en "Generar Reporte"
5. Verás:
   - Total de servicios
   - Monto total
   - Promedio por servicio
   - Desglose por tipo de vehículo
   - Desglose por empleado

### Reporte de Inventario

1. Selecciona "Reporte de Inventario"
2. Verás:
   - Valor total del inventario
   - Productos con stock bajo
   - Productos con stock crítico
   - Detalle de cada producto

### Reporte de Convenios

1. Selecciona "Reporte de Convenios"
2. Define el período
3. Verás:
   - Servicios realizados a cada convenio
   - Monto total por convenio
   - Descuentos aplicados
   - Facturación por empresa

### Exportar Reportes

Todos los reportes pueden exportarse a:
- **Excel:** Para análisis externo
- **PDF:** Para imprimir (próximamente)

---

## Preguntas Frecuentes

### ¿Puedo eliminar un servicio registrado por error?

Actualmente no se pueden eliminar servicios. Si registraste uno por error, contacta al administrador del sistema.

### ¿Qué pasa si desactivo un empleado?

- El empleado no aparecerá en la lista de empleados activos
- No podrás asignarle nuevos servicios
- Los servicios y liquidaciones anteriores se mantienen
- Puedes reactivarlo cuando lo necesites

### ¿Cómo sé si un producto está por agotarse?

El sistema muestra alertas de color:
- Verde: Stock normal
- Amarillo: Stock cerca del mínimo
- Rojo: Stock por debajo del mínimo

### ¿Puedo tener varios usuarios con el mismo nombre?

No, cada nombre de usuario debe ser único.

### ¿Cómo cambio mi contraseña?

Actualmente debes contactar al administrador para cambiar contraseñas.

### ¿Qué hago si olvidé mi contraseña?

Contacta al administrador del sistema para que la restablezca.

### ¿Puedo usar el sistema desde mi teléfono?

Sí, el sistema es responsive y se adapta a pantallas de celular y tablet.

### ¿Los reportes se guardan automáticamente?

No, debes exportarlos a Excel si quieres guardarlos.

### ¿Puedo modificar una liquidación ya pagada?

No, las liquidaciones pagadas no se pueden modificar. Esto asegura la integridad de los registros contables.

### ¿Cómo sé cuánto debe ganar cada empleado?

El sistema calcula automáticamente las comisiones basándose en:
- Los servicios realizados por el empleado
- El porcentaje de comisión configurado para ese empleado

---

## Consejos y Mejores Prácticas

### Para Registro de Servicios

1. **Registra los servicios inmediatamente** después de realizarlos
2. **Verifica la placa** antes de guardar
3. **Asigna el empleado correcto** para que la comisión se calcule bien
4. **Usa observaciones** para notas importantes del cliente

### Para Control de Inventario

1. **Actualiza el inventario regularmente**
2. **Define stock mínimos realistas** según tu consumo
3. **Revisa las alertas semanalmente**
4. **Haz conteos físicos mensuales** y ajusta si es necesario

### Para Liquidaciones

1. **Genera liquidaciones periódicamente** (quincenal o mensual)
2. **Revisa el detalle** antes de marcar como pagada
3. **Imprime o exporta** las liquidaciones para el archivo

### Para Convenios

1. **Actualiza los datos de contacto** si cambian
2. **Revisa las fechas de vencimiento** mensualmente
3. **Mantén actualizada la lista de vehículos** de cada empresa

---

## Atajos de Teclado

- **ESC:** Cerrar modales/ventanas emergentes
- **CTRL + S:** Guardar formulario activo (en algunos navegadores)
- **CTRL + F:** Buscar en la página actual

---

## Soporte Técnico

### ¿Necesitas Ayuda?

**Contacto:**
- Email: soporte@lavaderoal.com
- Teléfono: (601) 123-4567

**Horario de Soporte:**
- Lunes a Viernes: 8:00 AM - 6:00 PM
- Sábados: 8:00 AM - 12:00 PM

### Reportar un Problema

Cuando contactes soporte, proporciona:
1. Tu nombre de usuario
2. Descripción del problema
3. Qué estabas haciendo cuando ocurrió
4. Captura de pantalla (si es posible)

---

## Glosario

**Comisión:** Porcentaje del monto del servicio que recibe el empleado

**Convenio:** Acuerdo especial con empresas para descuentos

**Dashboard:** Panel principal con resumen de información

**Liquidación:** Cálculo de pago a empleado por período

**Stock:** Cantidad disponible de un producto

**Tarifa:** Precio establecido por tipo de vehículo

---

¡Gracias por usar Lavadero AL!

Si tienes sugerencias para mejorar este manual, por favor contáctanos.

**Versión del Manual:** 1.0.0
**Última actualización:** Enero 2025
