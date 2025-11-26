from database import get_db_connection
from schemas import LiquidacionCreate

class LiquidacionRepository:
    def get_all(self):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("""
                SELECT l.*, e.nombre as nombre_empleado, e.cedula, e.porcentaje_comision
                FROM liquidaciones l
                JOIN empleados e ON l.id_empleado = e.id
                ORDER BY l.fecha_creacion DESC
            """)
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    def get_by_id(self, id_liquidacion: int):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("""
                SELECT l.*, e.nombre as nombre_empleado, e.cedula, e.email, e.telefono, e.porcentaje_comision
                FROM liquidaciones l
                JOIN empleados e ON l.id_empleado = e.id
                WHERE l.id = %s
            """, (id_liquidacion,))
            return cursor.fetchone()
        finally:
            cursor.close()
            conn.close()

    def get_detalles(self, id_empleado: int, inicio, fin):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("""
                SELECT s.id, s.placa, s.tipo_vehiculo, s.tipo_servicio, s.fecha, s.monto_total, s.monto_comision
                FROM servicios s
                WHERE s.id_empleado = %s AND s.fecha BETWEEN %s AND %s AND s.estado = 'completado'
                ORDER BY s.fecha DESC
            """, (id_empleado, inicio, fin))
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    def check_duplicates(self, id_empleado: int, inicio, fin):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT id FROM liquidaciones
                WHERE id_empleado = %s AND (
                    (periodo_inicio <= %s AND periodo_fin >= %s) OR (periodo_inicio <= %s AND periodo_fin >= %s)
                )
            """, (id_empleado, inicio, inicio, fin, fin))
            return cursor.fetchone()
        finally:
            cursor.close()
            conn.close()

    def calculate_totals(self, id_empleado: int, inicio, fin):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("""
                SELECT COUNT(*) as total_servicios, COALESCE(SUM(monto_total), 0) as monto_total_servicios,
                COALESCE(SUM(monto_comision), 0) as total_comisiones
                FROM servicios
                WHERE id_empleado = %s AND fecha BETWEEN %s AND %s AND estado = 'completado'
            """, (id_empleado, inicio, fin))
            return cursor.fetchone()
        finally:
            cursor.close()
            conn.close()

    def create(self, liq: LiquidacionCreate, totales: dict):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO liquidaciones (id_empleado, periodo_inicio, periodo_fin, total_servicios,
                 monto_total_servicios, total_comisiones, estado, fecha_creacion)
                VALUES (%s, %s, %s, %s, %s, %s, 'pendiente', NOW())
            """, (liq.id_empleado, liq.periodo_inicio, liq.periodo_fin, totales['total_servicios'],
                  totales['monto_total_servicios'], totales['total_comisiones']))
            
            id_liquidacion = cursor.lastrowid

            cursor.execute("""
                INSERT INTO detalle_liquidaciones (id_liquidacion, id_servicio, monto_servicio, monto_comision)
                SELECT %s, id, monto_total, monto_comision FROM servicios
                WHERE id_empleado = %s AND fecha BETWEEN %s AND %s AND estado = 'completado'
            """, (id_liquidacion, liq.id_empleado, liq.periodo_inicio, liq.periodo_fin))
            
            conn.commit()
            return id_liquidacion
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()

    def mark_paid(self, id_liquidacion: int):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("UPDATE liquidaciones SET estado='pagada', fecha_pago=CURDATE() WHERE id=%s AND estado='pendiente'", (id_liquidacion,))
            conn.commit()
            return cursor.rowcount
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()

    def delete(self, id_liquidacion: int):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM liquidaciones WHERE id = %s", (id_liquidacion,))
            conn.commit()
            return cursor.rowcount
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()