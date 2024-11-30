<template>
  <div class="login-container">
    <form @submit.prevent="loginUserHandler">
      <h2>Iniciar Sesión</h2>
      <input v-model="email" type="email" placeholder="Correo electrónico" required />
      <input v-model="password" type="password" placeholder="Contraseña" required />
      <button type="submit">Iniciar Sesión</button>
      <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
    </form>
    <!-- Mueve el contenedor del mensaje de éxito fuera del formulario -->
    <div v-if="successMessage" class="success-container">
      <p>{{ successMessage }}</p>
      <div class="animation">
        <div class="sunglasses-emoji">😎</div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from '../api/axios';

export default {
  data() {
    return {
      email: '',
      password: '',
      errorMessage: '',
      successMessage: '', // Mensaje de éxito para usuarios no admin
    };
  },
  methods: {
    async loginUserHandler() {
      try {
        const response = await axios.post('/login/', {
          email: this.email,
          password: this.password,
        });

        // Almacenar el token en el localStorage
        localStorage.setItem('token', response.data.token);

        if (response.data.is_staff) {
          // Si es administrador, redirige a la página de generación de ganador
          this.$router.push('/generate-winner');
        } else {
          // Si no es administrador, muestra el mensaje de éxito
          this.successMessage =
            '¡Usted se ha inscrito al sorteo que consiste en una promoción de un Hotel que regala una estadía de 2 noches con todo pagado para una pareja en el día de San Valentín! ¡Éxito y buena suerte!';
          this.errorMessage = ''; // Limpia cualquier mensaje de error
        }

        this.email = '';
        this.password = '';
      } catch (error) {
        this.errorMessage = error.response?.data?.error || 'Credenciales inválidas.';
        this.successMessage = ''; // Limpia cualquier mensaje de éxito
        console.error('Error en el inicio de sesión:', error);
      }
    },
  },
};
</script>

<style scoped>
.login-container {
  background: url('../assets/pareja.jpg') no-repeat center center fixed; /* Imagen de fondo */
  background-size: cover; /* Ajusta la imagen al tamaño de la pantalla */
  height: 100vh; /* Altura completa de la pantalla */
  display: flex;
  flex-direction: column; /* Para organizar el formulario y el mensaje de éxito en columna */
  justify-content: center;
  align-items: center;
  padding: 20px; /* Espaciado interno */
}

form {
  background-color: rgba(255, 255, 255, 0.9); /* Fondo blanco translúcido */
  padding: 30px;
  border-radius: 10px;
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
  width: 90%;
  max-width: 400px; /* Ancho máximo del formulario */
  text-align: center; /* Alineación central */
}

h2 {
  margin-bottom: 20px; /* Espaciado inferior */
  font-size: 1.5em;
  color: #333;
}

input {
  width: 100%;
  margin: 10px 0;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  font-size: 1em;
}

button {
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  background-color: #4caf50;
  color: white;
  cursor: pointer;
  font-size: 1em;
}

button:hover {
  background-color: #45a049;
}

.success-container {
  margin-top: 20px; /* Añade un espacio entre el formulario y el mensaje */
  padding: 20px;
  background-color: #e6ffe6;
  border: 2px solid #4caf50;
  border-radius: 5px;
  text-align: center;
  max-width: 400px; /* Mantén el ancho del mensaje consistente */
}

.success-container p {
  font-size: 1.2em;
  font-weight: bold;
  color: #4caf50;
}

.animation {
  margin-top: 20px;
}

.sunglasses-emoji {
  font-size: 3em;
  animation: emoji-move 3s ease-in-out infinite;
}

@keyframes emoji-move {
  0% {
    transform: translateX(0);
  }
  50% {
    transform: translateX(15px);
  }
  100% {
    transform: translateX(0);
  }
}

.error {
  color: red;
  margin-top: 10px;
  font-weight: bold;
}
</style>
