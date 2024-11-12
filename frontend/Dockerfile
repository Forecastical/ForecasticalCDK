FROM node:22
# Configure working dir
WORKDIR /app

COPY ./forecastical/package.json ./forecastical/package-lock.json* ./
RUN npm ci &&  npm cache clean --force

COPY ./forecastical/ .

RUN npm install

EXPOSE 8080

CMD ["npm", "run", "serve"]
