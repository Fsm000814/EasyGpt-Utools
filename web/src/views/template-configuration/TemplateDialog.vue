<template>
  <div class="dialog-background" @click="closeDialog">
    <div class="dialog" @click.stop>
      <!-- 模板信息展示 -->
      <button @click="closeDialog">Close</button>
    </div>
  </div>
</template>

<script lang="ts">
export default {
  name: 'TemplateDialog',
  props: ['template'],
  emits: ['close'],
  methods: {
    closeDialog() {
      this.$emit('close');
    },
  },
};
</script>

<style>
.dialog-background {
  /* 全屏半透明背景 */
}
.dialog {
  /* 对话框样式 */
}
</style>
