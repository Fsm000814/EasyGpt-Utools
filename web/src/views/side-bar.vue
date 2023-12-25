<template>
  <!-- <router-view /> -->
  <a-layout>
    <a-layout-sider
      v-model:collapsed="collapsed"
      collapsible
      class="left"
      style="overflow: auto"
    >
      <div>
        <img src="../assets/logo.png" class="logo" />
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
      <a-layout-content>
        <router-view />
      </a-layout-content>
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
  name: 'side-bar',
  data() {
    return {
      collapsed: false,
      selectedKeys: ['message-chat'],
      menuItems: [
        {
          key: '/message-chat',
          icon: CommentOutlined,
          name: '聊天',
          menu: 'message-chat',
        },
        {
          key: '/trans-late',
          icon: BlockOutlined,
          name: '翻译',
          menu: 'trans-late',
        },
        {
          key: '/template-configuration',
          icon: UploadOutlined,
          name: '模板配置',
          menu: 'template-configuration',
        },
        { key: '/setting', icon: SettingFilled, name: '设置', menu: 'setting' },
        { key: '/user', icon: UserOutlined, name: '用户', menu: 'user' },
      ],
    };
  },

  methods: {
    // 路由内容切换
    handleMenuChange(item: { key: string }) {
      // 为传递的参数指定类型
      // 切换到指定的路由
      debugger;
      this.$router.push({ path: item.key });
    },
  },
};
</script>

<style>
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
