# Agent Grid - 80 Agents Visible, Click to Watch Their Screens
FROM node:20-alpine

WORKDIR /app

# Install dependencies
COPY package.json ./
RUN npm install --production

# Copy application
COPY . .

EXPOSE 3000 8090

CMD ["node", "server.js"]
