FROM node:22
# Configure working dir
WORKDIR /app

COPY . .

# npm install -g @vue/cli
RUN npm install -g @vue/cli
# npm install
RUN npm install
# Expose port 8080
# npm run serve
CMD [ "ls" ]
#CMD ["npm", "run", "serve"]
