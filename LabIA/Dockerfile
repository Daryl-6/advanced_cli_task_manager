# Stage 1: Build
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm install --production

# Stage 2: Final (Correction 25% : Sécurité & Légèreté)
FROM node:18-alpine
WORKDIR /app
COPY --from=builder /app/node_modules ./node_modules
COPY . .

# Ne pas exécuter en root
USER node

EXPOSE 3000
CMD ["node", "app.js"]
