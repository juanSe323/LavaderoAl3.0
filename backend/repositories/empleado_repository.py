from database import get_db_connection
from schemas import EmpleadoCreate

class EmpleadoRepository:
    def get_all(self):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM empleados ORDER BY estado, nombre")
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    def get_by_id(self, id_empleado: int):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM empleados WHERE id = %s", (id_empleado,))
            return cursor.fetchone()
        finally:
            cursor.close()
            conn.close()

    def get_by_cedula(self, cedula: str):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT id FROM empleados WHERE cedula = %s", (cedula,))
            return cursor.fetchone()
        finally:
            cursor.close()
            conn.close()

    def create(self, empleado: EmpleadoCreate):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            query = """
                INSERT INTO empleados (nombre, cedula, telefono, email, porcentaje_comision, estado)
                VALUES (%s, %s, %s, %s, %s, 'activo')
            """
            values = (empleado.nombre, empleado.cedula, empleado.telefono, empleado.email, empleado.porcentaje_comision)
            cursor.execute(query, values)
            conn.commit()
            return cursor.lastrowid
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()

    def update(self, id_empleado: int, empleado: EmpleadoCreate):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            query = """
                UPDATE empleados 
                SET nombre = %s, cedula = %s, telefono = %s, email = %s, porcentaje_comision = %s
                WHERE id = %s
            """
            values = (empleado.nombre, empleado.cedula, empleado.telefono, empleado.email, empleado.porcentaje_comision, id_empleado)
            cursor.execute(query, values)
            conn.commit()
            return cursor.rowcount
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()

    def soft_delete(self, id_empleado: int):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("UPDATE empleados SET estado = 'inactivo' WHERE id = %s", (id_empleado,))
            conn.commit()
            return cursor.rowcount
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()

# ... (código existente)

    def activate(self, id_empleado: int):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("UPDATE empleados SET estado = 'activo' WHERE id = %s", (id_empleado,))
            conn.commit()
            return cursor.rowcount
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()