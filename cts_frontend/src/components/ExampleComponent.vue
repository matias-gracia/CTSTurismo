<template>
    <div>
        <h1>Datos del backend</h1>
        <ul>
            <li v-for="item in items" :key="item.id">{{ item.name }}</li>
        </ul>
    </div>
</template>

<script>
import axios from '../api/axios.js';

export default {
    data() {
        return {
            items: [], // Aquí se guardarán los datos de la API
        };
    },
    created() {
        // Consumir la API cuando el componente se monte
        axios.get('endpoint/') // Cambia 'endpoint/' según la ruta de tu API
            .then(response => {
                this.items = response.data;
            })
            .catch(error => {
                console.error('Error al obtener los datos:', error);
            });
    },
};
</script>
