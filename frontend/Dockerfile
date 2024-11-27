FROM node:22
# Configure working dir
WORKDIR /app

COPY ./package.json ./package-lock.json* ./
RUN npm ci &&  npm cache clean --force

COPY . .

RUN npm install

CMD ["npm", "run", "serve"]
