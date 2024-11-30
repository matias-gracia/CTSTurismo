<template>
  <div class="admin-container">
    <div class="form-container">
      <h2>Lista de Usuarios Registrados</h2>
      <table class="user-table" v-if="users.length">
        <thead>
          <tr>
            <th>Nombre</th>
            <th>Correo</th>
            <th>Estado</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="user in users"
            :key="user.email"
            :class="{ winner: user.is_winner }"
          >
            <td>{{ user.username }}</td>
            <td>{{ user.email }}</td>
            <td>{{ user.is_winner ? 'Ganador' : user.is_active ? 'Activo' : 'Inactivo' }}</td>
          </tr>
        </tbody>
      </table>
      <p v-if="!users.length">No hay usuarios registrados.</p>
    </div>
    <div class="form-container">
      <h2>Generar Ganador</h2>
      <form @submit.prevent="generateWinner">
        <button type="submit" class="generate-button">Seleccionar Ganador</button>
        <p v-if="winnerMessage" class="winner-message">{{ winnerMessage }}</p>
        <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
      </form>
    </div>
  </div>
</template>


<script>
import axios from '../api/axios';

export default {
  data() {
    return {
      users: [], // Lista de usuarios
      winnerMessage: '',
      errorMessage: '',
    };
  },
  methods: {
    async fetchUsers() {
      const token = localStorage.getItem('token');
      if (!token) {
        this.$router.push('/login');
        return;
      }
      try {
        const response = await axios.get('/user-list/', {
          headers: { Authorization: `Token ${token}` },
        });
        this.users = response.data;
      } catch (error) {
        console.error('Error al obtener la lista de usuarios:', error);
        this.$router.push('/login');
      }
    },
    async generateWinner() {
      const token = localStorage.getItem('token');
      if (!token) {
        this.errorMessage = 'No estás autenticado.';
        return;
      }
      try {
        const response = await axios.post('/generate-winner/', {}, {
          headers: { Authorization: `Token ${token}` },
        });

        // Obtén el correo del ganador
        const winnerEmail = response.data.winner_email;

        // Actualiza los datos de los usuarios para reflejar al ganador
        this.users = this.users.map((user) => ({
          ...user,
          is_winner: user.email === winnerEmail,
          is_active: user.email === winnerEmail ? false : user.is_active,
        }));

        this.winnerMessage = `¡Ganador seleccionado! Felicidades a ${response.data.winner}`;
        this.errorMessage = '';
      } catch (error) {
        this.errorMessage = error.response?.data?.error || 'Error al generar el ganador.';
        this.winnerMessage = '';
      }
    },
  },
  created() {
    this.fetchUsers(); // Cargar usuarios al iniciar
  },
};
</script>


<style scoped>
.admin-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
  background: url('../assets/pareja.jpg') no-repeat center center fixed;
  background-size: cover;
  min-height: 100vh;
}

.form-container {
  background-color: rgba(255, 255, 255, 0.9);
  padding: 20px;
  margin-bottom: 20px;
  border-radius: 10px;
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
  width: 90%;
  max-width: 800px;
  text-align: center;
}

.user-table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 20px;
}

.user-table th, .user-table td {
  border: 1px solid #ccc;
  padding: 10px;
  text-align: left;
}

.user-table th {
  background-color: #f4f4f4;
}

.user-table tr.winner {
  background-color: yellow; /* Resalta al ganador */
}

.generate-button {
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  background-color: #4caf50;
  color: white;
  cursor: pointer;
}

.generate-button:hover {
  background-color: #45a049;
}

.winner-message {
  color: green;
  font-weight: bold;
  margin-top: 20px;
}

.error {
  color: red;
  font-weight: bold;
  margin-top: 20px;
}
</style>
