# Stage 1: Build the Vue application
# Usa una imagen ligera de Node.js para la fase de construcción
FROM node:20-alpine as build-stage

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia los archivos de definición de paquetes y el lockfile
COPY package*.json ./
COPY pnpm-lock.yaml ./

# Instala pnpm globalmente y luego las dependencias del proyecto
RUN npm install -g pnpm
RUN pnpm install

# Copia el resto de los archivos del proyecto
COPY . .

# Ejecuta el script de build para generar los archivos de producción
RUN pnpm build

# Stage 2: Serve the built files with Nginx
# Usa una imagen ligera de Nginx para servir los archivos estáticos
FROM nginx:stable-alpine as production-stage

# Copia los archivos construidos desde la etapa anterior a la carpeta pública de Nginx
COPY --from=build-stage /app/dist /usr/share/nginx/html

# Opcional: Si tienes una configuración personalizada de Nginx, puedes copiarla aquí
# COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expone el puerto 80 para acceder a la aplicación
EXPOSE 80

# Comando para iniciar el servidor Nginx cuando el contenedor se inicie
CMD ["nginx", "-g", "daemon off;"]
