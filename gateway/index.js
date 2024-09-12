const express = require('express');
const { createProxyMiddleware } = require('http-proxy-middleware');
const morgan = require('morgan');
const cors = require('cors');

const app = express();
const PORT = 3002; 

app.use(morgan('dev'));

// Configuração do CORS
app.use(cors({
  origin: 'http://localhost:3000', // Endereço do frontend
  methods: ['GET', 'POST', 'PUT', 'DELETE'],
  allowedHeaders: ['Content-Type', 'Authorization']
}));

// Adicione este middleware antes da configuração do proxy
app.use((req, res, next) => {
  console.log(`Requisição recebida no Gateway: ${req.method} ${req.path}`);
  next();
});

// Proxy para o backend
app.use('/api', createProxyMiddleware({
    target: 'http://backend:5000', // Use o nome do serviço Docker
    changeOrigin: true,
    pathRewrite: {
        '^/api': '/api', // Mantenha o prefixo /api
    },
    onProxyReq: (proxyReq, req, res) => {
      console.log(`Requisição proxy para o backend: ${proxyReq.method} ${proxyReq.path}`);
    },
    onProxyRes: (proxyRes, req, res) => {
      console.log(`Resposta do backend: ${proxyRes.statusCode}`);
    },
    onError: (err, req, res) => {
      console.error('Erro no proxy:', err);
      res.status(500).send('Erro no proxy');
    }
}));

// Adicione uma rota padrão
app.get('/', (req, res) => {
    res.send('API Gateway está funcionando');
});

// Adicione uma rota de teste direta
app.get('/test', (req, res) => {
    res.send('Teste do Gateway funcionando');
});

app.listen(PORT, () => {
    console.log(`API Gateway rodando na porta ${PORT}`);
});