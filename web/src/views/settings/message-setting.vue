<template>
  <div class="messageSetting">
    <a-spin :spinning="loading">
      <a-card>
        <h2>设置</h2>
        <h3>基本配置</h3>
        <a-divider />
        <a-form :model="basicConfiguration" layout="vertical" ref="ruleForm">
          <a-form-item label="API KEY" ref="userName" name="userName">
            <a-input-password v-model:value="basicConfiguration.apiKey" />
          </a-form-item>
          <a-form-item label="APL URL" :tooltip="apiUrlTips">
            <a-input v-model:value="basicConfiguration.apiUrl" />
          </a-form-item>
          <a-row>
            <a-col span="14">
              <a-form-item label="模型">
                <a-select v-model:value="basicConfiguration.models">
                  <a-select-option value="gpt-3.5-turbo"
                    >gpt-3.5-turbo</a-select-option
                  >
                  <a-select-option value="gpt-3.5-turbo-0301"
                    >gpt-3.5-turbo-0301</a-select-option
                  >
                  <a-select-option value="gpt-4">gpt-4</a-select-option>
                  <a-select-option value="gpt-4-0314"
                    >gpt-4-0314</a-select-option
                  >
                  <a-select-option value="gpt-4-32k">gpt-4-32k</a-select-option>
                  <a-select-option value="gpt-4-32k-0314"
                    >gpt-4-32k-0314</a-select-option
                  >
                </a-select>
              </a-form-item>
            </a-col>
            <a-col span="1"></a-col>
            <a-col span="5">
              <a-form-item label="Max Tokens">
                <a-input-number v-model:value="basicConfiguration.maxTokens" />
              </a-form-item>
            </a-col>
          </a-row>
          <a-form-item label="系统消息(System Message)" :tooltip="messageTips">
            <a-input v-model:value="basicConfiguration.systemMessage" />
          </a-form-item>
          <a-form-item>
            <a-button type="primary">保存</a-button>
          </a-form-item>
        </a-form>
        <h3>代理</h3>
        <a-divider />
        <a-form layout="vertical" :model="broker">
          <a-form-item label="状态">
            <a-radio-group v-model:value="broker.status">
              <a-radio :value="true">开启</a-radio>
              <a-radio :value="false">关闭</a-radio>
            </a-radio-group>
          </a-form-item>
          <a-row :gutter="24">
            <a-col span="6">
              <a-form-item label="代理IP地址">
                <a-input
                  disabled="broker.status"
                  v-model:value="broker.ipAddress"
                  placeholder="请输入代理IP地址"
                />
              </a-form-item>
            </a-col>
            <a-col span="6">
              <a-form-item label="端口">
                <a-input
                  v-model:value="broker.prot"
                  placeholder="请输入端口"
                  disabled="broker.status"
                />
              </a-form-item>
            </a-col>
            <a-col span="6">
              <a-form-item label="用户名">
                <a-input
                  v-model:value="broker.userName"
                  placeholder="请输入用户名"
                  disabled="broker.status"
                />
              </a-form-item>
            </a-col>
            <a-col span="6">
              <a-form-item label="密码">
                <a-input
                  v-model:value="broker.password"
                  placeholder="请输入密码"
                  disabled="broker.status"
                />
              </a-form-item>
            </a-col>
          </a-row>
          <a-form-item>
            <a-button type="primary">保存</a-button>
          </a-form-item></a-form
        >
        <h3>其他</h3>
        <a-divider />
        <a-form layout="vertical" :model="broker">
          <a-row :gutter="24">
            <a-col span="12">
              <a-form-item label="主题" ref="userName" name="userName">
                <a-tooltip title="跟随主题">
                  <a-button type="info"
                    ><FundProjectionScreenOutlined
                  /></a-button>
                </a-tooltip>
                <a-tooltip title="明亮模式">
                  <a-button type="info"><AlertOutlined /></a-button>
                </a-tooltip>
                <a-tooltip title="暗黑模式">
                  <a-button type="info"><AlertFilled /></a-button>
                </a-tooltip>
              </a-form-item>
            </a-col>
            <a-col span="12">
              <a-form-item label="缓存" ref="userName" name="userName">
                <span>67 个会话、2400 条消息</span><a-button type="link"
                  ><DeleteOutlined
                />清除缓存</a-button>
              </a-form-item>
            </a-col>
          </a-row>
          <a-row :gutter="24">
            <a-col span="12">
              <a-form-item label="自动起会话标题">
                <a-radio-group v-model:value="broker.status">
                  <a-radio :value="true">开启</a-radio>
                  <a-radio :value="false">关闭</a-radio>
                </a-radio-group>
              </a-form-item>
            </a-col>
            <a-col span="12">
              <a-form-item label="盘古之白(优化文本可读性)">
                <a-radio-group v-model:value="broker.status">
                  <a-radio :value="true">开启</a-radio>
                  <a-radio :value="false">关闭</a-radio>
                </a-radio-group>
              </a-form-item>
            </a-col>
          </a-row>
          <a-row :gutter="24">
            <a-col span="12">
              <p>当前插件版本：v0.0.1</p>
            </a-col>
          </a-row>
          <a-form-item>
            <a-button>检查更新</a-button>
          </a-form-item></a-form
        >
      </a-card>
    </a-spin>
  </div>
</template>
<script lang="ts">
import { defineComponent } from "vue";
import {
  AlertOutlined,
  FundProjectionScreenOutlined,
  AlertFilled,
  DeleteOutlined
} from "@ant-design/icons-vue";
export default defineComponent({
  components: {
    AlertOutlined,
    FundProjectionScreenOutlined,
    AlertFilled,
    DeleteOutlined
  },
  data() {
    return {
      messageTips:
        "通常用于给Ai预置身份或指定对话要开始的话题，上下文。注意：会话级的配置会覆盖默认值",
      apiUrlTips:
        "适用于使用自建的openai接口代理服务，示例：https://api.my-ipenai.com/v1",
      loading: false,
      basicConfiguration: {
        apiKey: null,
        apiUrl: null,
        models: null,
        maxTokens: null,
        systemMessage: null,
      },
      broker: {
        status: false,
        ipAddress: null,
        prot: null,
        userName: null,
        password: null,
      },
    };
  },
  methods: {},
});
</script>
<style lang="scss" scoped>
.message-setting {
  overflow-y: auto;
  height: calc(100vh - 20px);
  position: fixed;
  left: 0;
  top: 0;
  bottom: 0;
  width: 200px; /* 设置具体的宽度 */
  color: rgb(255, 255, 255);
  background: #1890ff;
}
</style>
