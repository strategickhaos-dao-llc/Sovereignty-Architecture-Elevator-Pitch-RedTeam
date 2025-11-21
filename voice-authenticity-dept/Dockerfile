FROM node:20-alpine

WORKDIR /app

# Copy package files
COPY package*.json ./
COPY tsconfig.json ./

# Install dependencies
RUN npm ci --only=production

# Copy source code
COPY src/ ./src/

# Build TypeScript
RUN npm install -g typescript && \
    tsc -p tsconfig.json && \
    npm uninstall -g typescript

# Remove source files after build
RUN rm -rf src/

# Expose port
EXPOSE 3030

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD node -e "require('http').get('http://localhost:3030/api/health', (r) => { process.exit(r.statusCode === 200 ? 0 : 1) })"

# Run the service
CMD ["node", "dist/server.js"]
