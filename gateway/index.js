const express = require('express');
const { createProxyMiddleware } = require('http-proxy-middleware');
const cors = require('cors');

const app = express();

app.use(cors());

app.use('/api', createProxyMiddleware({ 
  target: 'http://backend:5000',
  changeOrigin: true,
}));

const PORT = 3002;
app.listen(PORT, () => {
  console.log(`Gateway running on port ${PORT}`);
});