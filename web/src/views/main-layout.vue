<template>
  <a-layout>
    <a-layout-sider
      v-model:collapsed="collapsed"
      :trigger="null"
      collapsible
      class="left"
    >
      <div class="logo">
        <MenuUnfoldOutlined
          v-if="collapsed"
          class="trigger"
          @click="() => (collapsed = !collapsed)"
        />
        <MenuFoldOutlined
          v-else
          class="trigger"
          @click="() => (collapsed = !collapsed)"
        />
      </div>
      <a-menu v-model:selectedKeys="selectedKeys" theme="dark" mode="inline">
        <a-menu-item v-for="menuItem in menuItems" :key="menuItem.key">
          <component :is="menuItem.icon" />
          <span>{{ menuItem.name }}</span>
        </a-menu-item>
      </a-menu>
    </a-layout-sider>
    <a-layout-header style="background: #fff; padding: 0"> </a-layout-header>
    <a-layout-content class="content"> Content </a-layout-content>
    <a-layout-footer class="footer">
      EasyGpt ©2023 Created by FaceMan
    </a-layout-footer>
  </a-layout>
</template>
<script lang="ts" setup>
import { ref } from 'vue';
import {
  UserOutlined,
  VideoCameraOutlined,
  UploadOutlined,
  MenuUnfoldOutlined,
  MenuFoldOutlined,
} from '@ant-design/icons-vue';
const selectedKeys = ref<string[]>(['1']);
const collapsed = ref<boolean>(false);
const menuItems = [
  { key: '1', icon: UserOutlined, name: 'nav 1' },
  { key: '2', icon: VideoCameraOutlined, name: 'nav 2' },
  { key: '3', icon: UploadOutlined, name: 'nav 3' },
];
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
  background: hwb(337 11% 35% / 0.3);
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
  overflow: 'auto';
  height: 100vh;
  position: 'fixed';
  left: 0;
  top: 0;
  bottom: 0;
  color: rgb(255, 0, 55);
  background: #1890ff;
}
</style>
