const express = require('express');
const { createProxyMiddleware } = require('http-proxy-middleware');
const morgan = require('morgan');
const cors = require('cors');

const app = express();
const PORT = 3001;

app.use(morgan('dev'));

// Configuração do CORS
app.use(cors({
  origin: 'http://localhost:3000', // Endereço do frontend
  methods: ['GET', 'POST', 'PUT', 'DELETE'],
  allowedHeaders: ['Content-Type', 'Authorization']
}));

// Adicione este middleware antes da configuração do proxy
app.use((req, res, next) => {
  console.log(`Requisição recebida: ${req.method} ${req.path}`);
  next();
});

// Proxy para o backend
app.use('/api', createProxyMiddleware({
    target: 'http://localhost:5000',
    changeOrigin: true,
    pathRewrite: {
        '^/api': '', // Remove o prefixo /api ao encaminhar para o backend
    },
    onProxyReq: (proxyReq, req, res) => {
      console.log(`Requisição proxy para: ${proxyReq.method} ${proxyReq.path}`);
    },
    onError: (err, req, res) => {
      console.error('Erro no proxy:', err);
    }
}));

// Adicione uma rota padrão
app.get('/', (req, res) => {
    res.send('API Gateway está funcionando');
});

app.listen(PORT, () => {
    console.log(`API Gateway rodando na porta ${PORT}`);
});