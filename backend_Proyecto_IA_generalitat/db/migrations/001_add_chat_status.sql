-- Migración: Añadir campos de estado y finalización a la tabla chats
-- Fecha: 2026-01-15
-- Descripción: Permite marcar chats como completados después de generar el informe PDF

-- Añadir columna de estado
ALTER TABLE chats 
ADD COLUMN status VARCHAR(20) NOT NULL DEFAULT 'active' 
COMMENT 'Estado del chat: active (activo) o completed (finalizado)';

-- Añadir columna de fecha de finalización
ALTER TABLE chats 
ADD COLUMN completed_at DATETIME NULL 
COMMENT 'Fecha y hora en que se finalizó la entrevista';

-- Crear índice para búsquedas por estado
CREATE INDEX idx_chats_status ON chats(status);

-- Verificar cambios
SELECT 
    COLUMN_NAME, 
    DATA_TYPE, 
    IS_NULLABLE, 
    COLUMN_DEFAULT, 
    COLUMN_COMMENT
FROM INFORMATION_SCHEMA.COLUMNS 
WHERE TABLE_NAME = 'chats' 
  AND TABLE_SCHEMA = DATABASE()
  AND COLUMN_NAME IN ('status', 'completed_at');
