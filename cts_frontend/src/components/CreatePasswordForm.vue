<template>
  <div class="create-password-container">
    <div class="form-container">
      <h2>Crear Nueva Contraseña</h2>
      <form @submit.prevent="handleSubmit">
        <input
          type="password"
          v-model="password"
          placeholder="Nueva contraseña"
          required
        />
        <input
          type="password"
          v-model="confirmPassword"
          placeholder="Confirmar contraseña"
          required
        />
        <button type="submit">Guardar Contraseña</button>
      </form>
      <div v-if="errorMessage" class="error">{{ errorMessage }}</div>
      <div v-if="successMessage" class="success">
        {{ successMessage }}
        <p>Serás redirigido al inicio de sesión en {{ countdown }} segundos...</p>
      </div>
    </div>
  </div>
</template>

<script>
import { setPassword } from '../api/auth'; // Importa la función para enviar la contraseña al backend

export default {
  data() {
    return {
      password: '',
      confirmPassword: '',
      errorMessage: '',
      successMessage: '',
      countdown: 5, // Inicializa el contador en 5 segundos
      uidb64: null, // Para almacenar uidb64 de la URL
      token: null, // Para almacenar token de la URL
    };
  },
  created() {
    // Captura los parámetros desde la URL
    this.uidb64 = this.$route.query.uidb64;
    this.token = this.$route.query.token;

    if (!this.uidb64 || !this.token) {
      this.errorMessage = 'Parámetros inválidos en el enlace.';
    }
  },
  methods: {
    async handleSubmit() {
      if (this.password !== this.confirmPassword) {
        this.errorMessage = 'Las contraseñas no coinciden.';
        return;
      }

      try {
        const response = await setPassword({
          uidb64: this.uidb64,
          token: this.token,
          password: this.password,
        });

        this.successMessage = response.message;
        this.errorMessage = '';

        // Inicia el contador regresivo
        const interval = setInterval(() => {
          if (this.countdown > 0) {
            this.countdown -= 1;
          } else {
            clearInterval(interval); // Detiene el contador
            this.$router.push('/login'); // Redirige al login
          }
        }, 1000); // Disminuye el contador cada segundo
      } catch (error) {
        this.successMessage = '';
        this.errorMessage =
          error.response?.data?.error || 'Error al establecer la contraseña.';
      }
    },
  },
};
</script>

<style scoped>
.create-password-container {
  background: url('../assets/pareja.jpg') no-repeat center center fixed; /* Ruta de tu imagen */
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
  width: 90%;
  margin: 10px 0;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

button {
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  background-color: #4caf50;
  color: white;
  cursor: pointer;
}

button:hover {
  background-color: #45a049;
}

.error {
  color: red;
  font-weight: bold;
  margin-top: 10px;
}

.success {
  color: green;
  font-weight: bold;
  margin-top: 10px;
}
</style>
