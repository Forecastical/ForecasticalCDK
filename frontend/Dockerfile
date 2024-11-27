FROM node:22
# Configure working dir
WORKDIR /app

RUN npm install -g http-server

COPY ./package.json ./package-lock.json* ./
RUN npm ci &&  npm cache clean --force

COPY . .

RUN npm install

RUN npm run build

EXPOSE 3000
CMD ["http-server", "dist", "-p", "3000"]
