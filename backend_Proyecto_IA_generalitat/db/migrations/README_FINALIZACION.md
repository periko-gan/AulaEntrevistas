# Sistema de Finalización de Chats

## Objetivo
Marcar las entrevistas como finalizadas una vez generado el informe PDF, evitando que se puedan enviar más mensajes.

## Cambios realizados

### 1. Modelo Chat ([app/models/chat.py](../app/models/chat.py))
**Nuevos campos:**
- `status`: String(20), default='active'
  - Valores: `'active'` | `'completed'`
- `completed_at`: DateTime, nullable
  - Timestamp de cuándo se finalizó

### 2. Schema ChatResponse ([app/schemas/chat.py](../app/schemas/chat.py))
**Campos añadidos:**
- `status`: str
- `completed_at`: datetime | None

### 3. Repositorio ([app/repositories/chat_repo.py](../app/repositories/chat_repo.py))
**Nuevo método:**
```python
def mark_as_completed(db: Session, chat_id: int) -> Chat | None
```

### 4. Endpoint /reply ([app/api/v1/ai.py](../app/api/v1/ai.py))
**Validación añadida:**
- Rechaza mensajes si `chat.status == 'completed'`
- Error 400: "Esta entrevista ha finalizado..."

### 5. Endpoint /generate-report ([app/api/v1/ai.py](../app/api/v1/ai.py))
**Acción automática:**
- Marca el chat como completado después de generar el PDF
- Establece `completed_at` con timestamp actual

## Migración de Base de Datos

**Archivo:** `db/migrations/001_add_chat_status.sql`

**Ejecutar:**
```bash
# Opción 1: Dentro del contenedor MySQL
docker exec -it <mysql-container> mysql -u root -p aulavirtualbd < db/migrations/001_add_chat_status.sql

# Opción 2: Desde docker-compose
docker-compose exec db mysql -u root -p aulavirtualbd < db/migrations/001_add_chat_status.sql
```

**Cambios en BD:**
- Añade columna `status` VARCHAR(20) DEFAULT 'active'
- Añade columna `completed_at` DATETIME NULL
- Crea índice `idx_chats_status`

## Flujo de Usuario

### Chat Activo (status='active')
1. Usuario crea chat → status='active'
2. Usuario envía mensajes → ✅ Permitido
3. IA responde → ✅ Permitido
4. Repite 2-3 N veces

### Finalización
5. Usuario solicita generar PDF → `POST /ai/generate-report`
6. Backend:
   - Genera informe con IA
   - Crea PDF
   - **Marca chat como completado** (status='completed', completed_at=now)
   - Devuelve PDF

### Chat Completado (status='completed')
7. Usuario intenta enviar mensaje → ❌ Error 400
   ```json
   {
     "detail": "Esta entrevista ha finalizado. No se pueden enviar más mensajes. Crea una nueva entrevista para continuar."
   }
   ```

## Frontend - Cambios necesarios

### 1. Detectar estado del chat
```javascript
const chat = await fetch('/api/v1/chats/123');
const data = await chat.json();

if (data.status === 'completed') {
  // Deshabilitar input de mensajes
  inputElement.disabled = true;
  
  // Mostrar badge "Finalizada"
  showCompletedBadge();
  
  // Mostrar fecha de finalización
  if (data.completed_at) {
    showCompletionDate(data.completed_at);
  }
}
```

### 2. Manejo de errores al enviar
```javascript
try {
  await fetch('/api/v1/ai/reply', {
    method: 'POST',
    body: JSON.stringify({ chat_id: 123, contenido: 'mensaje' })
  });
} catch (error) {
  if (error.status === 400) {
    // Mostrar mensaje: "Esta entrevista ha finalizado"
    showAlert('Esta entrevista ya ha sido evaluada y no admite más mensajes.');
  }
}
```

### 3. UI Sugerencias

**Badge en lista de chats:**
```html
<div class="chat-item">
  <span class="chat-title">Mi entrevista de IA</span>
  <span v-if="chat.status === 'completed'" class="badge badge-success">
    ✓ Finalizada
  </span>
</div>
```

**Formulario deshabilitado:**
```html
<div v-if="chat.status === 'completed'" class="chat-completed-notice">
  <p>📋 Esta entrevista fue finalizada el {{ formatDate(chat.completed_at) }}</p>
  <p>Ya no es posible enviar más mensajes.</p>
  <button @click="createNewChat">Iniciar nueva entrevista</button>
</div>

<form v-else @submit="sendMessage">
  <input type="text" v-model="message" />
  <button type="submit">Enviar</button>
</form>
```

## Ventajas del Sistema

✅ **Integridad del informe**: El PDF refleja exactamente la conversación evaluada  
✅ **Simula realismo**: Como una entrevista real que no se puede repetir  
✅ **Fomenta progreso**: Cada nueva entrevista es una oportunidad de mejorar  
✅ **Evita confusión**: Clara separación entre entrevistas activas y completadas  
✅ **Auditoría**: Registro de cuándo se finalizó cada entrevista  

## Testing

**Test 1: Enviar mensaje a chat activo**
```bash
curl -X POST /api/v1/ai/reply \
  -H "Authorization: Bearer <token>" \
  -d '{"chat_id": 1, "contenido": "Hola"}'
# Esperado: 200 OK + respuesta IA
```

**Test 2: Generar PDF**
```bash
curl -X POST /api/v1/ai/generate-report \
  -H "Authorization: Bearer <token>" \
  -d '{"chat_id": 1}'
# Esperado: PDF descargado + chat.status='completed'
```

**Test 3: Enviar mensaje a chat completado**
```bash
curl -X POST /api/v1/ai/reply \
  -H "Authorization: Bearer <token>" \
  -d '{"chat_id": 1, "contenido": "Otro mensaje"}'
# Esperado: 400 Bad Request + mensaje de error
```

## Notas

- Los chats existentes tendrán `status='active'` por defecto (migración)
- Solo se puede finalizar un chat una vez
- No hay opción de "reabrir" un chat completado (by design)
- Si un usuario necesita continuar, debe crear un nuevo chat
