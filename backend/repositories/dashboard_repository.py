from database import get_db_connection

class DashboardRepository:
    def get_metricas(self):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            # (Simplificado para brevedad, combina las queries de metricas)
            data = {}
            queries = {
                "servicios_hoy": "SELECT COUNT(*) as val FROM servicios WHERE DATE(fecha)=CURDATE() AND estado='completado'",
                "ingresos_hoy": "SELECT COALESCE(SUM(monto_total), 0) as val FROM servicios WHERE DATE(fecha)=CURDATE() AND estado='completado'",
                "clientes_activos": "SELECT COUNT(DISTINCT placa) as val FROM servicios WHERE MONTH(fecha)=MONTH(CURDATE()) AND YEAR(fecha)=YEAR(CURDATE()) AND estado='completado'",
                "insumos_bajos": "SELECT COUNT(*) as val FROM inventario WHERE stock <= stock_minimo",
                "servicios_mes": "SELECT COUNT(*) as val FROM servicios WHERE MONTH(fecha)=MONTH(CURDATE()) AND YEAR(fecha)=YEAR(CURDATE()) AND estado='completado'",
                "ingresos_mes": "SELECT COALESCE(SUM(monto_total), 0) as val FROM servicios WHERE MONTH(fecha)=MONTH(CURDATE()) AND YEAR(fecha)=YEAR(CURDATE()) AND estado='completado'",
                "empleados_activos": "SELECT COUNT(*) as val FROM empleados WHERE estado='activo'",
                "convenios_activos": "SELECT COUNT(*) as val FROM convenios WHERE estado='activo' AND (fecha_termino IS NULL OR fecha_termino >= CURDATE())"
            }
            for key, sql in queries.items():
                cursor.execute(sql)
                data[key] = cursor.fetchone()['val']
            return data
        finally:
            cursor.close()
            conn.close()

    def get_servicios_recientes(self, limit: int):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("""
                SELECT s.id, s.placa, s.tipo_vehiculo, s.tipo_servicio, s.monto_total, s.monto_comision,
                s.fecha, s.estado, s.es_convenio, e.nombre as nombre_empleado, c.nombre_empresa
                FROM servicios s
                LEFT JOIN empleados e ON s.id_empleado = e.id
                LEFT JOIN convenios c ON s.id_convenio = c.id
                ORDER BY s.fecha DESC LIMIT %s
            """, (limit,))
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    def get_alertas_inventario(self):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("""
                SELECT id, nombre, categoria, stock, stock_minimo, unidad,
                CASE WHEN stock <= stock_minimo THEN 'URGENTE' ELSE 'ADVERTENCIA' END as nivel_alerta
                FROM inventario WHERE stock <= stock_minimo * 1.5 ORDER BY stock ASC LIMIT 10
            """)
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    def get_empleados_top(self, limit: int):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("""
                SELECT e.id, e.nombre, e.porcentaje_comision, COUNT(s.id) as total_servicios,
                COALESCE(SUM(s.monto_total), 0) as total_vendido, COALESCE(SUM(s.monto_comision), 0) as total_comisiones
                FROM empleados e LEFT JOIN servicios s ON e.id = s.id_empleado
                AND MONTH(s.fecha)=MONTH(CURDATE()) AND YEAR(s.fecha)=YEAR(CURDATE()) AND s.estado='completado'
                WHERE e.estado='activo' GROUP BY e.id ORDER BY total_vendido DESC LIMIT %s
            """, (limit,))
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    def get_grafico_servicios(self, dias: int):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("""
                SELECT DATE(fecha) as fecha, COUNT(*) as cantidad, SUM(monto_total) as ingresos
                FROM servicios WHERE fecha >= DATE_SUB(CURDATE(), INTERVAL %s DAY) AND estado='completado'
                GROUP BY DATE(fecha) ORDER BY fecha ASC
            """, (dias,))
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    def get_servicios_por_tipo(self):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("""
                SELECT tipo_servicio, COUNT(*) as cantidad, SUM(monto_total) as ingresos
                FROM servicios WHERE MONTH(fecha)=MONTH(CURDATE()) AND YEAR(fecha)=YEAR(CURDATE()) AND estado='completado'
                GROUP BY tipo_servicio ORDER BY cantidad DESC
            """)
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    def get_liquidaciones_pendientes(self):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("""
                SELECT l.id, l.periodo_inicio, l.periodo_fin, l.total_comisiones, e.nombre as nombre_empleado
                FROM liquidaciones l JOIN empleados e ON l.id_empleado = e.id
                WHERE l.estado='pendiente' ORDER BY l.fecha_creacion DESC LIMIT 5
            """)
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()