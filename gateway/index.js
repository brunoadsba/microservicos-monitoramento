const logger = require('./logger');
const express = require('express');
const { createProxyMiddleware } = require('http-proxy-middleware');
const rateLimit = require('express-rate-limit');
const morgan = require('morgan');

const app = express();

logger.info('Iniciando o gateway');

// Logging
app.use(morgan('combined'));

// Rate limiting
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutos
  max: 100 // limite de 100 requisições por janela
});
app.use(limiter);

logger.info('Configurações de rate limiting aplicadas');

// Error handling middleware
app.use((err, req, res, next) => {
  logger.error('Erro no middleware:', err.stack);
  res.status(500).send('Algo deu errado!');
});

// Proxy para o backend Flask
app.use('/api', createProxyMiddleware({
    target: 'http://backend:5000',
    changeOrigin: true,
    logLevel: 'debug',
    onProxyReq: (proxyReq, req) => {
      logger.info(`Proxying request to backend: ${req.method} ${req.path}`);
    },
    onError: (err, req, res) => {
      logger.error('Proxy error to backend:', err);
    }
}));

logger.info('Proxy para o backend configurado');

// Proxy para o frontend React
app.use('/', createProxyMiddleware({
    target: 'http://frontend:3000',
    changeOrigin: true,
    logLevel: 'debug',
    onProxyReq: (proxyReq, req) => {
      logger.info(`Proxying request to frontend: ${req.method} ${req.path}`);
    },
    onError: (err, req, res) => {
      logger.error('Proxy error to frontend:', err);
    }
}));

logger.info('Proxy para o frontend configurado');

const PORT = 3000;
app.listen(PORT, () => {
    logger.info(`API Gateway rodando na porta ${PORT}`);
});