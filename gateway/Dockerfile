# Estágio de build
FROM node:14-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

# Estágio final
FROM node:14-alpine
WORKDIR /app
COPY --from=builder /app/node_modules ./node_modules
COPY . .

# Criar um usuário não-root
RUN addgroup -g 1001 -S nodejs
RUN adduser -S nodejs -u 1001
USER nodejs

# Definir variáveis de ambiente
ENV NODE_ENV production

# Expor a porta
EXPOSE 3000

CMD ["node", "index.js"]