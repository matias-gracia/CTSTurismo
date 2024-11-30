<template>
    <div>
        <h1>Datos del Backend</h1>
        <ul>
            <li v-for="item in items" :key="item.id">{{ item.name }}</li>
        </ul>
    </div>
</template>

<script>
import axios from '../api/axios.js'; // Importa tu configuración global de Axios

export default {
    data() {
        return {
            items: [], // Aquí se guardarán los datos de la API
        };
    },
    created() {
        // Llamada a la API al montar el componente
        axios.get('/') // Cambia 'endpoint/' por '/' para evitar duplicaciones
            .then(response => {
                this.items = response.data; // Guarda los datos en la variable items
            })
            .catch(error => {
                console.error('Error al consumir la API:', error);
            });
    },
};
</script>

