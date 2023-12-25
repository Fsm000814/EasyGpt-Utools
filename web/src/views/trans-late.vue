<template>
  <div class="translator">
    <h1>多语言翻译器</h1>
    <div class="language-selector">
      <select v-model="sourceLanguage">
        <option value="auto">检测语言</option>
        <option v-for="lang in languages" :key="lang.code" :value="lang.code">
          {{ lang.name }}
        </option>
      </select>
      <span class="switch-arrow" @click="swapLanguages">&#8646;</span>
      <select v-model="targetLanguage">
        <option v-for="lang in languages" :key="lang.code" :value="lang.code">
          {{ lang.name }}
        </option>
      </select>
    </div>
    <textarea
      v-model="textToTranslate"
      placeholder="输入文本..."
      class="text-input"
    ></textarea>
    <button @click="translateText" class="translate-button">翻译</button>
    <div class="translation-result" v-if="translatedText">
      <p class="translated-text">{{ translatedText }}</p>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, reactive } from 'vue';

export default defineComponent({
  name: 'trans-late',
  setup() {
    const textToTranslate = ref('');
    const translatedText = ref('');
    const sourceLanguage = ref('auto');
    const targetLanguage = ref('en');
    const languages = reactive([
      // 下面添加了更多的语言选项
      { name: '英语', code: 'en' },
      { name: '中文', code: 'zh' },
      // 其他18种语言的代码和名称
      // ...
    ]);

    const swapLanguages = () => {
      // 交换源语言和目标语言
      [sourceLanguage.value, targetLanguage.value] = [
        targetLanguage.value,
        sourceLanguage.value,
      ];
    };

    const translateText = async () => {
      // 此处进行翻译调用
      // 注意：真正的翻译服务API调用应该在这里实现
      translatedText.value = `翻译成${targetLanguage.value}: ${textToTranslate.value}`;
    };

    return {
      textToTranslate,
      translatedText,
      sourceLanguage,
      targetLanguage,
      languages,
      swapLanguages,
      translateText,
    };
  },
});
</script>
<style scoped>
.translator {
  max-width: 600px;
  margin: 2rem auto;
  padding: 2rem;
  background-color: #f0f8ff;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  border-radius: 10px;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

h1 {
  color: #007bff;
  margin-bottom: 2rem;
}

.language-selector {
  display: flex;
  justify-content: space-between;
  margin-bottom: 1rem;
}

.language-selector select {
  flex: 1;
  padding: 0.75rem;
  border: 2px solid #007bff;
  border-radius: 0.375rem;
  background-color: #fff;
  font-size: 1rem;
  cursor: pointer;
  margin-right: 0.5rem;
}

.language-selector select:last-child {
  margin-right: 0;
}

.switch-arrow {
  font-size: 1.5rem;
  color: #007bff;
  cursor: pointer;
}

.input-area {
  margin-bottom: 1rem;
}

.text-input {
  width: 100%;
  padding: 1rem;
  font-size: 1rem;
  border: 2px solid #007bff;
  border-radius: 0.375rem;
  resize: none; /* Disable resize handle */
  overflow-y: auto;
  min-height: 150px; /* Set min-height for enough space */
}

.translate-button {
  width: 100%;
  padding: 1rem;
  border: none;
  background-color: #007bff;
  color: white;
  font-size: 1rem;
  border-radius: 0.375rem;
  cursor: pointer;
  transition: background-color 0.2s;
}

.translate-button:hover {
  background-color: #0056b3;
}

.translation-result {
  border: 2px solid #007bff;
  border-radius: 0.375rem;
  padding: 1rem;
  background-color: #fff;
  max-height: 200px;
  overflow-y: auto;
}

.translated-text {
  white-space: pre-wrap;
  word-break: break-word;
  color: #333;
}

@media (max-width: 768px) {
  .translator {
    margin: 1rem;
    padding: 1.5rem;
  }
  .language-selector select {
    margin-right: 0;
    margin-bottom: 0.5rem;
  }
  .language-selector .switch-arrow {
    align-self: center;
  }
}
</style>
