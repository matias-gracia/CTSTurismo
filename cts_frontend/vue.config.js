const { defineConfig } = require('@vue/cli-service');
module.exports = defineConfig({
  transpileDependencies: true,
  devServer: {
    proxy: {
      '/api/endpoint': {
        target: 'http://127.0.0.1:8000', // Backend Django
        changeOrigin: true,
        pathRewrite: { '^/api/endpoint': '' }, // Elimina '/api/endpoint' del path antes de enviarlo al backend
      },
    },
  },
});
