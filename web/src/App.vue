<template>
  <!-- <router-view /> -->
  <a-layout>
    <a-layout-sider v-model:collapsed="collapsed" collapsible class="left">
      <div>
        <img src="../src/assets/logo.png" class="logo" />
      </div>
      <a-menu
        v-model:selectedKeys="selectedKeys"
        theme="dark"
        mode="inline"
        @click="handleMenuChange"
      >
        <a-menu-item v-for="menuItem in menuItems" :key="menuItem.menu">
          <component :is="menuItem.icon" />
          <span>{{ menuItem.name }}</span>
        </a-menu-item>
      </a-menu>
    </a-layout-sider>
    <a-layout>
      <a-layout-header style="background: #fff; padding: 0" />
      <a-layout-content style="margin: 0 16px">
        <router-view />
      </a-layout-content>
      <a-layout-footer style="text-align: center">
        EasyGpt ©2023 Created by FaceMan
      </a-layout-footer>
    </a-layout>
  </a-layout>
</template>
<script lang="ts">
import {
  UserOutlined,
  CommentOutlined,
  UploadOutlined,
  SettingFilled,
  BlockOutlined,
} from '@ant-design/icons-vue';

export default {
  data() {
    return {
      collapsed: false,
      selectedKeys: ['message-chat'],
      menuItems: [
        { key: '1', icon: CommentOutlined, name: '聊天', menu: '/' },
        { key: '2', icon: BlockOutlined, name: '翻译', menu: '/translate' },
        {
          key: '3',
          icon: UploadOutlined,
          name: '模板配置',
          menu: '/template-configuration',
        },
        { key: '4', icon: SettingFilled, name: '设置', menu: '/setting' },
        { key: '5', icon: UserOutlined, name: '用户', menu: '/user' },
      ],
      context: '' as string,
    };
  },
  methods: {
    //路由内容切换
    handleMenuChange(this: any, item: any) {
      this.$router.push({ path: item.key });
    },
  },
};
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
  margin-left: 36%;
}

.left {
  overflow: 'auto';
  height: 100vh;
  position: 'fixed';
  left: 0;
  top: 0;
  bottom: 0;
  color: rgb(255, 255, 255);
  background: #1890ff;
}
</style>
