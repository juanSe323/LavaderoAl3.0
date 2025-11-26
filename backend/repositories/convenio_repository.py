from database import get_db_connection
from schemas import ConvenioCreate, VehiculoConvenioCreate

class ConvenioRepository:
    def get_all(self):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("""
                SELECT c.*, (SELECT COUNT(*) FROM vehiculos_convenio v 
                 WHERE v.id_convenio = c.id AND v.estado = 'activo') as total_vehiculos
                FROM convenios c ORDER BY c.estado, c.nombre_empresa
            """)
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    # --- NUEVO MÃ‰TODO AGREGADO ---
    def get_by_id(self, id_convenio: int):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM convenios WHERE id = %s", (id_convenio,))
            return cursor.fetchone()
        finally:
            cursor.close()
            conn.close()
    # -----------------------------

    def create(self, c: ConvenioCreate):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            query = """
                INSERT INTO convenios
                (nombre_empresa, nit_empresa, contacto, telefono, email, direccion,
                 tipo_descuento, valor_descuento, fecha_inicio, fecha_termino, observaciones)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (
                c.nombre_empresa, c.nit_empresa, c.contacto, c.telefono, c.email, c.direccion,
                c.tipo_descuento, c.valor_descuento, c.fecha_inicio, c.fecha_termino, c.observaciones
            ))
            conn.commit()
            return cursor.lastrowid
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()

    def update_dynamic(self, id_convenio: int, campos: list, vals: list):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            vals.append(id_convenio)
            cursor.execute(f"UPDATE convenios SET {', '.join(campos)} WHERE id = %s", vals)
            conn.commit()
            return cursor.rowcount
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()

    def soft_delete(self, id_convenio: int):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("UPDATE convenios SET estado = 'inactivo' WHERE id = %s", (id_convenio,))
            conn.commit()
            return cursor.rowcount
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()

    def get_vehiculos(self, id_convenio: int):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM vehiculos_convenio WHERE id_convenio = %s AND estado='activo'", (id_convenio,))
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    def check_vehiculo_activo(self, placa: str):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT id FROM vehiculos_convenio WHERE placa = %s AND estado = 'activo'", (placa,))
            return cursor.fetchone()
        finally:
            cursor.close()
            conn.close()

    def add_vehiculo(self, id_convenio: int, v: VehiculoConvenioCreate):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO vehiculos_convenio (id_convenio, placa, tipo_vehiculo, modelo, color)
                VALUES (%s, %s, %s, %s, %s)
            """, (id_convenio, v.placa, v.tipo_vehiculo, v.modelo, v.color))
            conn.commit()
            return cursor.lastrowid
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()

    def remove_vehiculo(self, id_vehiculo: int):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("UPDATE vehiculos_convenio SET estado = 'inactivo' WHERE id = %s", (id_vehiculo,))
            conn.commit()
            return cursor.rowcount
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()

    def validar_placa(self, placa: str):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("""
                SELECT c.id as id_convenio, c.nombre_empresa, c.tipo_descuento, c.valor_descuento, v.tipo_vehiculo
                FROM vehiculos_convenio v
                JOIN convenios c ON v.id_convenio = c.id
                WHERE v.placa = %s AND v.estado = 'activo' AND c.estado = 'activo'
            """, (placa,))
            return cursor.fetchone()
        finally:
            cursor.close()
            conn.close()