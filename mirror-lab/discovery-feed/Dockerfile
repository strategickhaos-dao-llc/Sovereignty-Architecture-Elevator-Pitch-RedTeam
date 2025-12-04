# Discovery Feed - Real-time Log of Breakthroughs
FROM node:20-alpine

WORKDIR /app

COPY package.json ./
RUN npm install --production

COPY . .

EXPOSE 3006

CMD ["node", "server.js"]
