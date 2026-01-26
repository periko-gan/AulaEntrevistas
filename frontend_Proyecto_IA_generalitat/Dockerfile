# Usa una imagen oficial de Node.js.
FROM node:20

# Establece el directorio de trabajo en el contenedor
WORKDIR /usr/src/app

# Copia los archivos de definición de dependencias
COPY package.json ./
COPY pnpm-lock.yaml ./

# Instala pnpm
RUN npm install -g pnpm

# Instala las dependencias del proyecto
RUN pnpm install

# Copia el resto de los archivos de la aplicación
COPY . .

# Expone el puerto en el que se ejecuta la aplicación
EXPOSE 5173

# Comando para ejecutar la aplicación
CMD [ "pnpm", "run", "dev", "--host" ]
