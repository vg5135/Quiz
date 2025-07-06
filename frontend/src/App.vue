<template>
  <router-view />
  <Chatbot />
</template>

<script setup>
import Chatbot from './components/Chatbot.vue';
// No logic needed here, router-view only
</script>

<style>
body {
  margin: 0;
  font-family: "Inter", "Segoe UI", Arial, sans-serif;
  background: #f7fafc;
}
#app{
  margin:0 !important;
  padding:0 !important;
}
</style>
