USE aulavirtualbd;
-- Asegura motor InnoDB (necesario para FK)
SET sql_mode = 'STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION';

-- =========================
-- TABLA: users
-- =========================
CREATE TABLE IF NOT EXISTS users (
  id_usuario INT UNSIGNED NOT NULL AUTO_INCREMENT,
  email VARCHAR(255) NOT NULL,
  password_hash TEXT NOT NULL,
  nombre VARCHAR(100) NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id_usuario),
  UNIQUE KEY uq_users_email (email)
) ENGINE=InnoDB;

-- =========================
-- TABLA: chats
-- =========================
CREATE TABLE IF NOT EXISTS chats (
  id_chat INT UNSIGNED NOT NULL AUTO_INCREMENT,
  id_usuario INT UNSIGNED NOT NULL,
  title VARCHAR(255) NOT NULL DEFAULT 'Nuevo Chat',
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  last_message_at TIMESTAMP NULL DEFAULT NULL,
  PRIMARY KEY (id_chat),
  KEY idx_chats_usuario (id_usuario),
  CONSTRAINT fk_chats_usuario
    FOREIGN KEY (id_usuario)
    REFERENCES users (id_usuario)
    ON DELETE CASCADE
) ENGINE=InnoDB;

-- =========================
-- TABLA: mensajes
-- =========================
CREATE TABLE IF NOT EXISTS mensajes (
  id_mensaje INT UNSIGNED NOT NULL AUTO_INCREMENT,
  id_chat INT UNSIGNED NOT NULL,
  emisor ENUM('USER','IA') NOT NULL,
  contenido TEXT NOT NULL,
  sent_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id_mensaje),
  KEY idx_mensajes_chat (id_chat),
  KEY idx_mensajes_fecha (sent_at),
  CONSTRAINT fk_mensajes_chat
    FOREIGN KEY (id_chat)
    REFERENCES chats (id_chat)
    ON DELETE CASCADE
) ENGINE=InnoDB;
