<template>
  <div id="app">
    <!-- 侧边栏组件 -->
    <sidebar />
  </div>
</template>
<script lang="ts">
import { defineComponent, ref } from 'vue';
import sidebar from './views/side-bar.vue';
export default defineComponent({
  name: 'App',
  components: {
    sidebar,
  },
});
</script>
<style lang="scss"></style>
