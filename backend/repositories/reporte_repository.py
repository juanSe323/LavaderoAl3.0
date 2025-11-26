from database import get_db_connection

class ReporteRepository:
    def get_general(self, where_clause, params):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(f"""
                SELECT COUNT(*) as total_servicios, COALESCE(SUM(monto_total), 0) as ingresos_totales,
                COALESCE(SUM(monto_comision), 0) as total_comisiones, COALESCE(AVG(monto_total), 0) as ticket_promedio
                FROM servicios s {where_clause}
            """, params)
            totales = cursor.fetchone()

            cursor.execute(f"SELECT tipo_servicio, COUNT(*) as cantidad, SUM(monto_total) as ingresos FROM servicios s {where_clause} GROUP BY tipo_servicio ORDER BY ingresos DESC", params)
            por_tipo = cursor.fetchall()

            cursor.execute(f"SELECT tipo_vehiculo, COUNT(*) as cantidad, SUM(monto_total) as ingresos FROM servicios s {where_clause} GROUP BY tipo_vehiculo ORDER BY ingresos DESC", params)
            por_vehiculo = cursor.fetchall()

            return {"totales": totales, "por_tipo_servicio": por_tipo, "por_tipo_vehiculo": por_vehiculo}
        finally:
            cursor.close()
            conn.close()

    def get_empleados(self, where_clause, params):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(f"""
                SELECT e.id, e.nombre, e.cedula, e.porcentaje_comision, COUNT(s.id) as total_servicios,
                COALESCE(SUM(s.monto_total), 0) as total_vendido, COALESCE(SUM(s.monto_comision), 0) as total_comisiones,
                COALESCE(AVG(s.monto_total), 0) as ticket_promedio
                FROM empleados e LEFT JOIN servicios s ON e.id = s.id_empleado AND s.estado='completado' {where_clause}
                WHERE e.estado='activo' GROUP BY e.id ORDER BY total_vendido DESC
            """, params)
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    def get_servicios_diarios(self, dias: int):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("""
                SELECT DATE(fecha) as fecha, COUNT(*) as total_servicios, SUM(monto_total) as ingresos, SUM(monto_comision) as comisiones
                FROM servicios WHERE fecha >= DATE_SUB(CURDATE(), INTERVAL %s DAY) AND estado='completado'
                GROUP BY DATE(fecha) ORDER BY fecha DESC
            """, (dias,))
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    def get_convenios(self, where_clause, params):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(f"""
                SELECT c.id, c.nombre_empresa, c.nit_empresa, COUNT(s.id) as total_servicios,
                COALESCE(SUM(s.monto_total), 0) as total_facturado, COALESCE(SUM(s.descuento), 0) as total_descuentos
                FROM convenios c LEFT JOIN servicios s ON c.id = s.id_convenio AND s.es_convenio=TRUE AND s.estado='completado' {where_clause}
                WHERE c.estado='activo' GROUP BY c.id ORDER BY total_facturado DESC
            """, params)
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    def get_inventario(self):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT COUNT(*) as total_insumos, SUM(stock * precio_unitario) as valor_total_inventario, SUM(CASE WHEN stock <= stock_minimo THEN 1 ELSE 0 END) as insumos_stock_critico FROM inventario")
            resumen = cursor.fetchone()
            
            cursor.execute("SELECT categoria, COUNT(*) as cantidad_insumos, SUM(stock) as stock_total, SUM(stock * precio_unitario) as valor_categoria FROM inventario GROUP BY categoria ORDER BY valor_categoria DESC")
            por_categoria = cursor.fetchall()
            
            cursor.execute("SELECT nombre, categoria, stock, stock_minimo, precio_unitario, CASE WHEN stock <= stock_minimo THEN 'CRITICO' ELSE 'BAJO' END as nivel_alerta FROM inventario WHERE stock <= stock_minimo * 1.5 ORDER BY stock ASC")
            stock_bajo = cursor.fetchall()
            
            return {"resumen": resumen, "por_categoria": por_categoria, "stock_bajo": stock_bajo}
        finally:
            cursor.close()
            conn.close()

    def get_financiero(self, anio: int):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("""
                SELECT MONTH(fecha) as mes, MONTHNAME(fecha) as nombre_mes, COUNT(*) as total_servicios,
                SUM(monto_total) as ingresos_brutos, SUM(monto_comision) as total_comisiones,
                SUM(monto_total - monto_comision) as ingresos_netos
                FROM servicios WHERE YEAR(fecha)=%s AND estado='completado'
                GROUP BY MONTH(fecha), MONTHNAME(fecha) ORDER BY mes
            """, (anio,))
            mensual = cursor.fetchall()
            
            cursor.execute("""
                SELECT COUNT(*) as total_servicios_anio, COALESCE(SUM(monto_total), 0) as ingresos_brutos_anio,
                COALESCE(SUM(monto_comision), 0) as comisiones_anio, COALESCE(SUM(monto_total - monto_comision), 0) as ingresos_netos_anio
                FROM servicios WHERE YEAR(fecha)=%s AND estado='completado'
            """, (anio,))
            totales = cursor.fetchone()
            
            return {"anio": anio, "mensual": mensual, "totales": totales}
        finally:
            cursor.close()
            conn.close()