<template>
  <div class="register-container">
    <div class="form-container">
      <h2>Regístrate para el sorteo</h2>
      <form @submit.prevent="handleRegister">
        <input v-model="username" type="text" placeholder="Nombre completo" required />
        <input v-model="email" type="email" placeholder="Correo electrónico" required />
        <button type="submit">Registrarse</button>
      </form>
      <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
      <p v-if="successMessage" class="success">{{ successMessage }}</p>
    </div>
  </div>
</template>

<script>
import axios from '../api/axios';

export default {
  data() {
    return {
      username: '',
      email: '',
      errorMessage: '',
      successMessage: '',
    };
  },
  methods: {
    async handleRegister() {
      try {
        const response = await axios.post('/register/', {
          username: this.username,
          email: this.email,
        });
        this.successMessage = response.data.message;
        this.errorMessage = '';
        this.username = '';
        this.email = '';
      } catch (error) {
        this.errorMessage =
          error.response?.data?.error || 'Error al registrarse. Por favor, inténtalo de nuevo.';
        this.successMessage = '';
      }
    },
  },
};
</script>

<style scoped>
.register-container {
  background: url('../assets/pareja.jpg') no-repeat center center fixed; 
  background-size: cover; /* Asegura que la imagen cubra toda la pantalla */
  height: 100vh; /* Altura completa de la pantalla */
  display: flex;
  justify-content: center;
  align-items: center;
}

.form-container {
  background-color: rgba(255, 255, 255, 0.8); /* Fondo blanco translúcido */
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
  text-align: center;
}

input {
  width: 100%;
  margin: 10px 0;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

button {
  padding: 10px 20px;
  background-color: #4caf50;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

button:hover {
  background-color: #45a049;
}

.error {
  color: red;
  margin-top: 10px;
}

.success {
  color: green;
  margin-top: 10px;
}
</style>
