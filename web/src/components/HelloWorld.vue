<template>
  <a-layout>
    <a-layout-sider
      v-model:collapsed="collapsed"
      :trigger="null"
      collapsible
      class="left"
    >
      <div class="logo">
        <img src="./logo.jpg" alt="" style="height: 30px; margin-left: 40%" />
      </div>
      <!--引入logo -->
      <a-menu v-model:selectedKeys="selectedKeys" theme="dark" mode="inline">
        <a-menu-item key="1">
          <user-outlined />
          <span>nav 1</span>
        </a-menu-item>
        <a-menu-item key="2">
          <video-camera-outlined />
          <span>nav 2</span>
        </a-menu-item>
        <a-menu-item key="3">
          <upload-outlined />
          <span>nav 3</span>
        </a-menu-item>
      </a-menu>
    </a-layout-sider>
    <a-layout-content> Content </a-layout-content>
    <a-layout-footer class="footer">
      EasyGpt ©2023 Created by FaceMan
    </a-layout-footer>
  </a-layout>
</template>
<script lang="ts" setup>
import { ref } from "vue";
const selectedKeys = ref<string[]>(["1"]);
const collapsed = ref<boolean>(true);
</script>
<style>
#components-layout-demo-custom-trigger .trigger {
  font-size: 18px;
  line-height: 64px;
  padding: 0 24px;
  cursor: pointer;
  transition: color 0.3s;
}

#components-layout-demo-custom-trigger .trigger:hover {
  color: #1890ff;
}

#components-layout-demo-custom-trigger .logo {
  height: 32px;
  background: rgba(255, 255, 255, 0.3);
  margin: 16px;
}

.site-layout .site-layout-background {
  background: #fff;
}

.logo {
  height: 32px;
  margin: 16px;
}

.footer {
  position: absolute;
  width: 100%;
  bottom: 0;
  border-top: 1px solid #e8e8e8;
  text-align: center;
  background: #fff;
  padding: 0.5%;
}

.left {
  overflow: "auto";
  height: 100vh;
  position: "fixed";
  left: 0;
  top: 0;
  bottom: 0;
}
</style>
