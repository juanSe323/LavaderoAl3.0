# Guía de Contribución - Lavadero AL

¡Gracias por tu interés en contribuir a Lavadero AL! Este documento proporciona las pautas y procesos para contribuir al proyecto.

## Tabla de Contenidos

- [Código de Conducta](#código-de-conducta)
- [Cómo Contribuir](#cómo-contribuir)
- [Proceso de Desarrollo](#proceso-de-desarrollo)
- [Estándares de Código](#estándares-de-código)
- [Commits y Mensajes](#commits-y-mensajes)
- [Pull Requests](#pull-requests)
- [Reportar Bugs](#reportar-bugs)
- [Solicitar Características](#solicitar-características)
- [Preguntas Frecuentes](#preguntas-frecuentes)

---

## Código de Conducta

### Nuestro Compromiso

Este proyecto y todos sus participantes están comprometidos a proporcionar un ambiente de colaboración libre de acoso para todos, independientemente de:

- Edad
- Tamaño corporal
- Discapacidad
- Etnia
- Identidad y expresión de género
- Nivel de experiencia
- Nacionalidad
- Apariencia personal
- Raza
- Religión
- Orientación sexual

### Comportamiento Esperado

- Usar lenguaje acogedor e inclusivo
- Ser respetuoso con diferentes puntos de vista
- Aceptar críticas constructivas
- Enfocarse en lo que es mejor para la comunidad
- Mostrar empatía hacia otros miembros

### Comportamiento Inaceptable

- Uso de lenguaje o imágenes sexualizadas
- Comentarios insultantes o despectivos (trolling)
- Acoso público o privado
- Publicar información privada de otros
- Otras conductas no éticas o no profesionales

---

## Cómo Contribuir

Hay muchas formas de contribuir al proyecto:

### 1. Reportar Bugs

Si encuentras un error, por favor:

1. Verifica que no esté ya reportado en [Issues](https://github.com/tuusuario/LavaderoAl3.0/issues)
2. Crea un nuevo issue usando la plantilla de bug report
3. Incluye toda la información necesaria (ver sección [Reportar Bugs](#reportar-bugs))

### 2. Solicitar Características

Para solicitar nuevas funcionalidades:

1. Verifica que no exista una solicitud similar
2. Crea un issue con la etiqueta "enhancement"
3. Describe claramente el caso de uso y beneficios

### 3. Escribir Código

1. Fork el repositorio
2. Crea una rama para tu característica
3. Implementa tus cambios
4. Envía un Pull Request

### 4. Mejorar Documentación

- Corregir typos
- Mejorar explicaciones
- Agregar ejemplos
- Traducir documentación

### 5. Ayudar a Otros

- Responder preguntas en issues
- Revisar Pull Requests
- Compartir el proyecto

---

## Proceso de Desarrollo

### 1. Configurar el Entorno

```bash
# Fork y clonar el repositorio
git clone https://github.com/TU_USUARIO/LavaderoAl3.0.git
cd LavaderoAl3.0

# Agregar el repositorio original como upstream
git remote add upstream https://github.com/USUARIO_ORIGINAL/LavaderoAl3.0.git

# Instalar dependencias
npm install
cd backend
pip install -r requirements.txt
```

### 2. Crear una Rama

Usa nombres descriptivos para tus ramas:

```bash
# Características nuevas
git checkout -b feature/nombre-caracteristica

# Correcciones de bugs
git checkout -b fix/nombre-bug

# Mejoras de documentación
git checkout -b docs/descripcion

# Refactorización
git checkout -b refactor/componente
```

### 3. Realizar Cambios

- Mantén los cambios enfocados y atómicos
- Sigue los estándares de código
- Agrega tests si es aplicable
- Actualiza la documentación relevante

### 4. Probar tus Cambios

```bash
# Frontend
npm run dev

# Backend
cd backend
uvicorn main:app --reload

# Tests (cuando estén implementados)
npm run test
pytest
```

### 5. Mantener tu Rama Actualizada

```bash
# Obtener cambios del repositorio original
git fetch upstream
git rebase upstream/main
```

### 6. Enviar Pull Request

- Push a tu fork
- Crea el Pull Request desde GitHub
- Completa la plantilla de PR
- Espera revisión y comentarios

---

## Estándares de Código

### Python (Backend)

#### Estilo

- Seguir [PEP 8](https://pep8.org/)
- Usar 4 espacios para indentación
- Máximo 100 caracteres por línea
- Nombres descriptivos en español para variables de negocio

#### Ejemplo

```python
# ✅ Bueno
def calcular_comision_empleado(monto_servicio: float, porcentaje: int) -> float:
    """
    Calcula la comisión de un empleado basado en el monto del servicio.

    Args:
        monto_servicio: Monto total del servicio
        porcentaje: Porcentaje de comisión (0-100)

    Returns:
        Monto de la comisión calculada
    """
    return (monto_servicio * porcentaje) / 100

# ❌ Malo
def calc(m, p):
    return m*p/100
```

#### Type Hints

Usar type hints en todas las funciones:

```python
from typing import Optional, List, Dict

def obtener_empleado(id_empleado: int) -> Optional[Dict]:
    pass

def listar_servicios(limite: int = 50) -> List[Dict]:
    pass
```

#### Docstrings

Usar docstrings estilo Google:

```python
def crear_liquidacion(id_empleado: int, fecha_inicio: date, fecha_fin: date) -> int:
    """
    Crea una liquidación para un empleado en un período específico.

    Args:
        id_empleado: ID del empleado
        fecha_inicio: Fecha de inicio del período
        fecha_fin: Fecha de fin del período

    Returns:
        ID de la liquidación creada

    Raises:
        ValueError: Si las fechas son inválidas
        HTTPException: Si el empleado no existe
    """
    pass
```

### JavaScript/Vue (Frontend)

#### Estilo

- Usar 2 espacios para indentación
- Punto y coma al final de las líneas
- Single quotes para strings
- camelCase para variables y funciones
- PascalCase para componentes

#### Ejemplo Vue Component

```vue
<template>
  <div class="empleado-card">
    <h3>{{ empleado.nombre }}</h3>
    <p>Comisión: {{ empleado.porcentaje_comision }}%</p>
    <button @click="handleEdit">Editar</button>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';

const props = defineProps({
  empleado: {
    type: Object,
    required: true
  }
});

const emit = defineEmits(['edit']);

const handleEdit = () => {
  emit('edit', props.empleado.id);
};
</script>

<style scoped>
.empleado-card {
  padding: 1rem;
  border: 1px solid #ddd;
  border-radius: 8px;
}
</style>
```

#### Composables

```javascript
// useEmpleados.js
import { ref } from 'vue';
import { empleadosAPI } from '@/services/api';

export function useEmpleados() {
  const empleados = ref([]);
  const loading = ref(false);
  const error = ref(null);

  const cargarEmpleados = async () => {
    loading.value = true;
    error.value = null;

    try {
      const data = await empleadosAPI.getAll();
      empleados.value = data;
    } catch (err) {
      error.value = err.message;
    } finally {
      loading.value = false;
    }
  };

  return {
    empleados,
    loading,
    error,
    cargarEmpleados
  };
}
```

### SQL

- Palabras clave en MAYÚSCULAS
- Nombres de tablas y columnas en snake_case
- Usar indentación para queries complejas

```sql
-- ✅ Bueno
SELECT
    e.id,
    e.nombre,
    COUNT(s.id) AS total_servicios,
    SUM(s.monto_total) AS monto_total
FROM empleados e
LEFT JOIN servicios s ON e.id = s.id_empleado
WHERE e.activo = TRUE
    AND s.fecha >= '2024-01-01'
GROUP BY e.id, e.nombre
ORDER BY monto_total DESC;

-- ❌ Malo
select e.id,e.nombre,count(s.id),sum(s.monto_total) from empleados e left join servicios s on e.id=s.id_empleado where e.activo=1 group by e.id;
```

---

## Commits y Mensajes

### Formato de Commits

Usamos [Conventional Commits](https://www.conventionalcommits.org/):

```
<tipo>[scope opcional]: <descripción>

[cuerpo opcional]

[footer opcional]
```

### Tipos de Commit

- `feat`: Nueva característica
- `fix`: Corrección de bug
- `docs`: Cambios en documentación
- `style`: Cambios de formato (no afectan el código)
- `refactor`: Refactorización de código
- `perf`: Mejoras de rendimiento
- `test`: Agregar o modificar tests
- `chore`: Tareas de mantenimiento

### Ejemplos

```bash
# Característica nueva
git commit -m "feat(empleados): agregar filtro por estado activo"

# Corrección de bug
git commit -m "fix(inventario): corregir cálculo de stock negativo"

# Documentación
git commit -m "docs(api): actualizar ejemplos de endpoints"

# Refactorización
git commit -m "refactor(servicios): extraer lógica de comisiones a utilidad"
```

### Mensajes Descriptivos

```bash
# ✅ Bueno
git commit -m "feat(liquidaciones): implementar generación automática de PDF"

# ❌ Malo
git commit -m "update"
git commit -m "fix bug"
git commit -m "changes"
```

---

## Pull Requests

### Antes de Enviar

- [ ] Código sigue los estándares establecidos
- [ ] Tests pasan (cuando estén implementados)
- [ ] Documentación actualizada
- [ ] Sin conflictos con la rama main
- [ ] Commits siguen el formato convencional

### Título del PR

Usar el mismo formato que los commits:

```
feat(empleados): Agregar exportación de datos a Excel
fix(dashboard): Corregir gráfico de servicios mensuales
docs: Actualizar guía de instalación
```

### Descripción del PR

Usar la siguiente plantilla:

```markdown
## Descripción
Breve descripción de los cambios realizados.

## Tipo de cambio
- [ ] Bug fix (cambio que corrige un issue)
- [ ] Nueva característica (cambio que agrega funcionalidad)
- [ ] Breaking change (cambio que puede romper funcionalidad existente)
- [ ] Documentación

## ¿Cómo se ha probado?
Describe las pruebas realizadas.

## Checklist
- [ ] Mi código sigue los estándares del proyecto
- [ ] He realizado una auto-revisión de mi código
- [ ] He comentado mi código en áreas difíciles de entender
- [ ] He actualizado la documentación correspondiente
- [ ] Mis cambios no generan nuevos warnings
- [ ] He agregado tests que prueban mi funcionalidad
```

### Proceso de Revisión

1. Espera al menos una aprobación
2. Responde a comentarios constructivamente
3. Realiza cambios solicitados
4. El mantenedor hará merge cuando esté aprobado

---

## Reportar Bugs

### Antes de Reportar

- Verifica que no esté ya reportado
- Intenta reproducir el bug
- Recopila información relevante

### Información a Incluir

```markdown
**Descripción del bug**
Una descripción clara y concisa del bug.

**Pasos para reproducir**
1. Ir a '...'
2. Hacer click en '....'
3. Hacer scroll hasta '....'
4. Ver error

**Comportamiento esperado**
Qué esperabas que sucediera.

**Comportamiento actual**
Qué sucedió realmente.

**Screenshots**
Si aplica, agrega screenshots.

**Ambiente:**
 - OS: [e.g. Windows 10, Ubuntu 20.04]
 - Navegador: [e.g. Chrome 96, Firefox 95]
 - Versión Node: [e.g. 20.19.0]
 - Versión Python: [e.g. 3.11.0]

**Información adicional**
Cualquier otro contexto sobre el problema.
```

---

## Solicitar Características

### Propuesta de Característica

```markdown
**¿Tu solicitud está relacionada con un problema?**
Una descripción clara del problema. Ej: Siempre es frustrante cuando [...]

**Describe la solución que te gustaría**
Una descripción clara de lo que quieres que suceda.

**Describe alternativas que has considerado**
Otras soluciones o características que has considerado.

**¿Beneficios de implementar esta característica?**
- Beneficio 1
- Beneficio 2

**¿Esta característica requiere cambios en la API?**
Sí/No - Detalles si aplica

**Contexto adicional**
Agrega cualquier otro contexto o screenshots.
```

---

## Preguntas Frecuentes

### ¿Necesito permiso para trabajar en un issue?

No necesitas permiso, pero es buena práctica comentar en el issue que planeas trabajar en él para evitar duplicación de esfuerzos.

### ¿Puedo trabajar en múltiples issues a la vez?

Sí, pero recomendamos enfocarte en uno o dos a la vez para mantener la calidad.

### ¿Qué hago si mi PR no recibe revisión?

Espera al menos 3-5 días. Si no hay respuesta, puedes hacer un comentario solicitando revisión.

### ¿Puedo enviar un PR sin issue relacionado?

Para cambios pequeños (typos, documentación), sí. Para características nuevas, primero crea un issue para discutir.

### ¿Cómo puedo convertirme en mantenedor?

Contribuye consistentemente con PRs de calidad. Los mantenedores actuales te contactarán.

### ¿Hay algún canal de comunicación?

Por ahora, usa GitHub Issues y Discussions. En el futuro podríamos agregar Discord o Slack.

---

## Buenas Prácticas

### Para Contribuidores

1. **Lee la documentación existente** antes de empezar
2. **Pregunta si tienes dudas** - no hay preguntas tontas
3. **Mantén los PRs pequeños** - más fácil de revisar
4. **Escribe tests** para tu código (cuando estén disponibles)
5. **Sé paciente** - los mantenedores son voluntarios

### Para Revisores

1. **Sé constructivo** en tus comentarios
2. **Explica el "por qué"** de tus sugerencias
3. **Aprecia el esfuerzo** de los contribuidores
4. **Revisa en tiempo razonable**
5. **Aprueba cuando esté listo** - no busques perfección absoluta

---

## Recursos Útiles

- [Guía de Markdown](https://www.markdownguide.org/)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [PEP 8 - Python Style Guide](https://pep8.org/)
- [Vue.js Style Guide](https://vuejs.org/style-guide/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Git Workflow](https://www.atlassian.com/git/tutorials/comparing-workflows)

---

## Agradecimientos

Gracias a todos los que contribuyen al proyecto. Cada contribución, sin importar el tamaño, es valiosa.

### Contribuidores Destacados

<!-- Se llenará automáticamente con contribuidores del proyecto -->

---

**¡Gracias por contribuir a Lavadero AL!** 🚗✨
