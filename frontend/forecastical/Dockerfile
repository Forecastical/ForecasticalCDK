FROM node:22

# Configure working dir
WORKDIR /app

# Install dependencies first for better caching
COPY package*.json ./
RUN npm install

# Copy source code
COPY . .

# Expose the Vue dev server port
EXPOSE 3000

# Run the development server
ENV HOST=0.0.0.0
CMD ["npm", "run", "serve:frontend", "--", "--port", "3000"]