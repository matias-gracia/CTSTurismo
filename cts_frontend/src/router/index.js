import { createRouter, createWebHistory } from 'vue-router';
import RegisterForm from '../components/RegisterForm.vue';
import CreatePasswordForm from '../components/CreatePasswordForm.vue';
import LoginForm from '../components/LoginForm.vue';
import GenerateWinner from '../components/GenerateWinner.vue'; // Importa el nuevo componente
import axios from 'axios';

const routes = [
  { path: '/', name: 'Register', component: RegisterForm },
  { path: '/create-password', name: 'CreatePassword', component: CreatePasswordForm },
  { path: '/login', name: 'Login', component: LoginForm },
  {
    path: '/generate-winner',
    name: 'GenerateWinner',
    component: GenerateWinner,
    meta: { requiresAuth: true, adminOnly: true }, // Meta para proteger la ruta
  },
  { path: '/:pathMatch(.*)*', redirect: '/' }, // Redirige rutas no encontradas
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// Middleware global para proteger rutas
router.beforeEach(async (to, from, next) => {
  const token = localStorage.getItem('token'); // Obtén el token del almacenamiento local

  // Verifica si la ruta requiere autenticación
  if (to.meta.requiresAuth) {
    if (!token) {
      console.log('No token found. Redirecting to login.');
      return next('/login'); // Redirige al login si no hay token
    }

    try {
      // Solicita la información del usuario al backend
      const response = await axios.get('http://127.0.0.1:8000/api/endpoint/user-profile/', {
        headers: { Authorization: `Token ${token}` },
      });

      const user = response.data;

      // Verifica si es necesario acceso de administrador
      if (to.meta.adminOnly && !user.is_staff) {
        console.log('User is not an admin. Redirecting to home.');
        return next('/'); // Redirige si no es administrador
      }

      next(); // Permite acceso si todo está en orden
    } catch (error) {
      console.error('Error al verificar permisos:', error);
      localStorage.removeItem('token'); // Elimina el token si es inválido
      next('/login'); // Redirige al login si hay un error
    }
  } else {
    next(); // Si no requiere autenticación, permite acceso
  }
});

export default router;
