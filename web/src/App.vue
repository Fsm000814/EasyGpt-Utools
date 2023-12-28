<template>
  <div id="app">
    <div class="container">
      <sidebar />
      <div class="main">
        <a-layout style="height: 100%;">
          <a-layout-header style="background: #fff; padding: 0" />
          <a-layout-content>
            <router-view v-slot="{ Component, route }">
              <transition name="animation" mode="out-in">
                <component :is="Component" :key="route.path" />
              </transition>
            </router-view>
          </a-layout-content>
        </a-layout>
      </div>
    </div>
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
<style lang="scss">
.container {
  position: absolute;
  inset: 0;
  display: flex;

  .main {
    flex-grow: 1;
    height: 100%;
    overflow-x: hidden;
    overflow-y: auto;
  }
} 

</style>
