const logger = require('./logger');
const express = require('express');
const { createProxyMiddleware } = require('http-proxy-middleware');

const app = express();
const PORT = process.env.PORT || 3000;

// Configuração do middleware de proxy
app.use('/api', createProxyMiddleware({
    target: 'http://localhost:5000', // Altere para o endereço do seu serviço backend
    changeOrigin: true,
}));

app.listen(PORT, () => {
    logger.info(`API Gateway rodando na porta ${PORT}`);
});