<template>
  <div class="chat-container">
    <div class="chat-content" ref="contentRef">
      <div
        v-for="(message, index) in messages"
        :key="index"
        class="chat-message"
      >
        <div v-if="message.sender === 'user'" class="user-message">
          {{ message.content }}
        </div>
        <div v-else class="bot-message">
          {{ message.content }}
        </div>
      </div>
    </div>
    <div class="chat-input">
      <input
        v-model="inputText"
        placeholder="请输入消息"
        @keyup.enter="sendMessage"
      />
      <button @click="sendMessage">发送</button>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from 'vue';

interface Message {
  content: string;
  sender: string;
}

export default defineComponent({
  name: 'message-chat',
  setup() {
    const messages = ref<Message[]>([]);
    const inputText = ref('');
    const contentRef = ref<HTMLDivElement | null>(null);

    const sendMessage = () => {
      if (inputText.value.trim() !== '') {
        messages.value.push({ content: inputText.value, sender: 'user' });
        // 调用GPT接口进行机器人回复
        // ...

        // 假设机器人回复内容为reply
        const reply = '这是机器人的回复';
        messages.value.push({ content: reply, sender: 'bot' });

        inputText.value = '';
      }
    };

    // 滚动到底部
    const scrollToBottom = () => {
      if (contentRef.value) {
        contentRef.value.scrollTop = contentRef.value.scrollHeight;
      }
    };

    onMounted(scrollToBottom);

    return {
      messages,
      inputText,
      sendMessage,
      contentRef,
    };
  },
});
</script>

<style scoped>
.chat-container {
  display: flex;
  flex-direction: column;
  height: 100%;
  background-color: #f5f5f5;
  padding: 15px;
}

.chat-content {
  flex-grow: 1;
  overflow-y: auto;
  max-height: calc(100vh - 180px); /* 调整此处的高度以适应实际布局 */
}

.chat-message {
  margin-bottom: 10px;
  display: flex;
  flex-direction: column;
}

.user-message,
.bot-message {
  max-width: 70%;
  padding: 10px;
  border-radius: 8px;
  word-wrap: break-word;
}

.user-message {
  background-color: #007bff;
  color: #000;
  align-self: flex-end;
  margin-left: auto;
}

.bot-message {
  background-color: #fff;
  color: #000;
  align-self: flex-start;
  margin-right: auto;
}

.chat-input {
  display: flex;
  align-items: center;
  padding: 10px;
  background-color: #fff;
  border-radius: 20px;
  margin-top: 20px;
  border: 1px solid #ccc;
}

.chat-input input {
  flex-grow: 1;
  padding: 10px;
  border: none;
  border-radius: 4px;
  outline: none;
}

.chat-input button {
  margin-left: 10px;
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  background-color: #007bff;
  color: #fff;
  cursor: pointer;
}

.chat-input button:hover {
  background-color: #0069d9;
}

.chat-input button:focus {
  outline: none;
}

::-webkit-scrollbar {
  width: 6px;
}

::-webkit-scrollbar-thumb {
  background-color: rgba(0, 0, 0, 0.2);
  border-radius: 3px;
}

::-webkit-scrollbar-thumb:hover {
  background-color: rgba(0, 0, 0, 0.3);
}
</style>
