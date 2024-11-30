<template>
  <div id="app">
    <router-view /> <!-- Aquí se renderizarán los componentes según la ruta -->
  </div>
</template>

<script>
export default {
  name: "App",
};
</script>

<style>
/* Si necesitas estilos globales, puedes colocarlos aquí */
body {
  margin: 0;
  font-family: Arial, sans-serif;
}
</style>
