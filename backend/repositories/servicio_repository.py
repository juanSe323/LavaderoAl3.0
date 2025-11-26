from database import get_db_connection
from schemas import ServicioCreate

class ServicioRepository:
    def get_all(self, limit=100):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            # Unimos con empleados y convenios para mostrar nombres en lugar de solo IDs
            query = """
                SELECT s.*, e.nombre as nombre_empleado, c.nombre_empresa
                FROM servicios s
                LEFT JOIN empleados e ON s.id_empleado = e.id
                LEFT JOIN convenios c ON s.id_convenio = c.id
                ORDER BY s.fecha DESC
                LIMIT %s
            """
            cursor.execute(query, (limit,))
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    def get_by_id(self, id_servicio: int):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM servicios WHERE id = %s", (id_servicio,))
            return cursor.fetchone()
        finally:
            cursor.close()
            conn.close()

    def create(self, data: ServicioCreate, monto_comision: int, es_convenio: int, descuento: float):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            query = """
                INSERT INTO servicios 
                (placa, tipo_vehiculo, tipo_servicio, monto_total, monto_comision, 
                 id_empleado, id_convenio, es_convenio, descuento, observaciones, fecha, estado)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW(), 'completado')
            """
            # Mapeo exacto de tu esquema
            values = (
                data.placa.upper(), 
                data.tipo_vehiculo, 
                data.tipo_servicio, 
                data.monto_total, 
                monto_comision, 
                data.id_empleado,
                data.id_convenio,
                es_convenio,
                descuento,
                data.observaciones
            )
            cursor.execute(query, values)
            conn.commit()
            return cursor.lastrowid
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()

    def update_dynamic(self, id_servicio: int, campos: list, vals: list):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            # AÃ±adimos el ID al final de la lista de valores para la clÃ¡usula WHERE
            vals.append(id_servicio)
            sql = f"UPDATE servicios SET {', '.join(campos)} WHERE id = %s"
            
            cursor.execute(sql, vals)
            conn.commit()
            return cursor.rowcount
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()

    def cancel(self, id_servicio: int):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            # Soft delete: cambiamos estado a 'cancelado' y anulamos comisiÃ³n
            cursor.execute("""
                UPDATE servicios 
                SET estado = 'cancelado', monto_comision = 0 
                WHERE id = %s
            """, (id_servicio,))
            conn.commit()
            return cursor.rowcount
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()