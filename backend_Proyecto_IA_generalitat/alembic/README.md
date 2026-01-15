# Alembic Migrations

Esta carpeta contiene las migraciones de base de datos gestionadas por Alembic.

## Uso básico

### Crear una nueva migración automática

```bash
# Desde el directorio backend_Proyecto_IA_generalitat/
alembic revision --autogenerate -m "descripcion del cambio"
```

Alembic detectará los cambios en tus modelos SQLAlchemy y generará automáticamente los scripts de migración.

### Crear una migración manual

```bash
alembic revision -m "descripcion del cambio"
```

Luego edita el archivo generado en `versions/` para definir manualmente las operaciones `upgrade()` y `downgrade()`.

### Aplicar migraciones

```bash
# Aplicar todas las migraciones pendientes
alembic upgrade head

# Aplicar migraciones hasta una revisión específica
alembic upgrade <revision_id>

# Aplicar solo la siguiente migración
alembic upgrade +1
```

### Revertir migraciones

```bash
# Revertir la última migración
alembic downgrade -1

# Revertir hasta una revisión específica
alembic downgrade <revision_id>

# Revertir todas las migraciones
alembic downgrade base
```

### Ver historial de migraciones

```bash
# Ver historial completo
alembic history

# Ver migración actual
alembic current

# Ver migraciones pendientes
alembic show head
```

## Buenas prácticas

1. **Siempre revisa las migraciones autogeneradas** antes de aplicarlas. Alembic puede no detectar algunos cambios o generar código no óptimo.

2. **Prueba las migraciones en desarrollo** antes de aplicarlas en producción:
   ```bash
   alembic upgrade head
   alembic downgrade -1
   alembic upgrade head
   ```

3. **Usa nombres descriptivos** para las migraciones:
   ```bash
   alembic revision --autogenerate -m "add_user_profile_fields"
   ```

4. **Implementa downgrade correctamente**. Siempre define cómo revertir los cambios.

5. **Evita modificar migraciones ya aplicadas**. Si encuentras un error, crea una nueva migración correctiva.

## Ejemplo: Migración del campo status en chats

```python
"""add_chat_status_field

Revision ID: 001
Revises: 
Create Date: 2024-01-15 10:30:00.000000

"""
from alembic import op
import sqlalchemy as sa

revision = '001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.add_column('chats', 
        sa.Column('status', sa.String(20), server_default='active', nullable=False)
    )
    op.add_column('chats', 
        sa.Column('completed_at', sa.DateTime, nullable=True)
    )

def downgrade() -> None:
    op.drop_column('chats', 'completed_at')
    op.drop_column('chats', 'status')
```

## Estructura de archivos

```
alembic/
├── versions/          # Migraciones generadas
│   ├── 20240115_1030-001_add_chat_status.py
│   └── 20240116_0945-002_add_user_email_verified.py
├── env.py            # Configuración del entorno de Alembic
└── script.py.mako    # Template para nuevas migraciones

alembic.ini           # Configuración principal de Alembic
```

## Troubleshooting

### Error: "Can't locate revision identified by 'xxxx'"

La base de datos y las migraciones están desincronizadas. Opciones:
1. Resetear la tabla `alembic_version` y ejecutar `alembic stamp head`
2. Crear una nueva migración desde el estado actual

### Error: "Target database is not up to date"

```bash
alembic upgrade head
```

### Quiero aplicar manualmente un cambio sin Alembic

No recomendado, pero si es necesario:
```bash
# Aplicar cambio manual a BD
# Luego marcar como aplicado en Alembic:
alembic stamp <revision_id>
```
