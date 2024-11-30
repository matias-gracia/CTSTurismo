<template>
  <div class="confirmation-container">
    <h2>Confirmación de Correo Electrónico</h2>
    <p v-if="loading">Validando tu correo, por favor espera...</p>
    <p v-else-if="success" class="success">¡Tu correo ha sido validado exitosamente! Ahora puedes iniciar sesión.</p>
    <p v-else class="error">Lo sentimos, la validación de tu correo ha fallado. Intenta nuevamente.</p>
    <router-link v-if="success" to="/">Ir al inicio</router-link>
  </div>
</template>

<script>
import axiosInstance from "../api/axios"; // Usa tu configuración de Axios

export default {
  data() {
    return {
      loading: true,
      success: false,
    };
  },
  async created() {
    const uidb64 = this.$route.query.uidb64; // Captura uidb64 desde la URL
    const token = this.$route.query.token; // Captura token desde la URL

    if (!uidb64 || !token) {
      this.loading = false;
      this.success = false;
      return;
    }

    try {
      const response = await axiosInstance.get(`/verify-email/?uidb64=${uidb64}&token=${token}`);
      if (response.status === 200) {
        this.success = true;
      } else {
        throw new Error("Error en la validación.");
      }
    } catch (error) {
      console.error(error.message);
      this.success = false;
    } finally {
      this.loading = false;
    }
  },
};
</script>

<style scoped>
.confirmation-container {
  max-width: 400px;
  margin: 50px auto;
  text-align: center;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background-color: #fff;
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
}
h2 {
  color: #333;
}
.success {
  color: green;
  font-weight: bold;
}
.error {
  color: red;
  font-weight: bold;
}
</style>
