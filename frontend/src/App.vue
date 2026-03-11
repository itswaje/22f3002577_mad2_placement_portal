<script setup>
import Navbar from '@/components/Navbar.vue'
import Footer from '@/components/Footer.vue'
</script>

<template>
  <Navbar />
  <main class="main-content">
    <RouterView />
  </main>
  <Footer />
</template>

<style scoped>
.main-content {
  min-height: calc(100vh - 120px);
  background: #f1f5f9;
}
</style>
