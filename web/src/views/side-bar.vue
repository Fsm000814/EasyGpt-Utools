<template>

  <div class="side-bar" :class="collapsed ? 'collapsed' : ''" >
    <div class="logo">
      <img src="../assets/logo.png" class="logo-img" />
    </div>
    <div class="menu">
      <a-menu v-model:selectedKeys="selectedKeys" theme="dark" mode="inline" @click="handleMenuChange">
        <a-menu-item v-for="menuItem in menuItems" :key="menuItem.menu">
          <component :is="menuItem.icon" />
          <span v-if="!collapsed">{{ menuItem.name }}</span>
        </a-menu-item>
      </a-menu>
    </div>
    <div
      class="bottom-bar"
      @click="collapsed = !collapsed"
    >
    <RightCircleOutlined v-if="collapsed"/>
    <LeftCircleOutlined v-else/>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import {
  UserOutlined,
  CommentOutlined,
  UploadOutlined,
  SettingFilled,
  BlockOutlined,
  RightCircleOutlined,
  LeftCircleOutlined
} from '@ant-design/icons-vue';

export default defineComponent({
  components: {
    RightCircleOutlined,
    LeftCircleOutlined
  },
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
        { key: '/message-setting', icon: SettingFilled, name: '设置', menu: 'message-setting' },
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
});
</script>

<style lang="scss">
.side-bar {
  display: flex;
  flex-direction: column;
  width: 240px;
  height: 100%;
  flex-shrink: 0;
  background-color: #001529;
  transition: width 0.3s ease;

  &.collapsed {
    width: 70px;
  }

  .logo {
    flex-shrink: 0;

    .logo-img {
      height: 24px;
      margin: 16px;
      margin-left: 36%;
    }
  }

  .menu {
    flex-grow: 1;
  }

  .bottom-bar {
    flex-shrink: 0;
    height: 40px;
    display: flex;
    justify-content: center;
    align-items: center;
    color: white;
    cursor: pointer;
    background-color: #03284a;
  }
}



.animation-enter-from,
.animation-leave-to {
  transform: translateX(20px);
  opacity: 0;
}
.animation-enter-to,
.animation-leave-from {
  opacity: 1;
}
.animation-enter-active {
  transition: all 0.7s ease;
}
.animation-leave-active {
  transition: all 0.3s cubic-bezier(1, 0.6, 0.6, 1);
}
</style>
