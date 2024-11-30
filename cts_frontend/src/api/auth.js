import axiosInstance from './axios'; // Asegúrate de usar la ruta correcta

export const registerUser = async (userData) => {
    try {
        const response = await axiosInstance.post('register/', userData);
        console.log('Registro exitoso:', response.data);
        return response.data;
    } catch (error) {
        console.error('Error en el registro:', error.response?.data || error.message);
        throw error;
    }
};

// Nueva función para enviar contraseña al backend
export const setPassword = async (passwordData) => {
    try {
        const response = await axiosInstance.post('set-password/', passwordData);
        console.log('Contraseña establecida exitosamente:', response.data);
        return response.data;
    } catch (error) {
        console.error('Error al establecer la contraseña:', error.response?.data || error.message);
        throw error;
    }
};

export const loginUser = async (userData) => {
    try {
      const response = await axiosInstance.post('login/', userData);
      console.log('Inicio de sesión exitoso:', response.data);
      return response.data;
    } catch (error) {
      console.error('Error al iniciar sesión:', error.response?.data || error.message);
      throw error;
    }
  };
  
