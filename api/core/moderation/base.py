from abc import ABC, abstractmethod
from typing import Optional
from pydantic import BaseModel
from enum import Enum

from core.extension.extensible import Extensible, ExtensionModule

class ModerationAction(Enum):
    DIRECT_OUTPUT = 'direct_output'
    OVERRIDED = 'overrided'

class ModerationInputsResult(BaseModel):
    """
    用于存储输入结果的模型类。
    """
    flagged: bool = False
    action: ModerationAction
    preset_response: str = ""
    inputs: dict = {}
    query: str = ""

class ModerationOutputsResult(BaseModel):
    """
    用于存储输出结果的模型类。
    """
    flagged: bool = False
    action: ModerationAction
    preset_response: str = ""
    text: str = ""

class Moderation(Extensible, ABC):
    """
    审核类的基类。
    """
    module: ExtensionModule = ExtensionModule.MODERATION

    def __init__(self, app_id: str, tenant_id: str, config: Optional[dict] = None) -> None:
        super().__init__(tenant_id, config)
        self.app_id = app_id

    @classmethod
    @abstractmethod
    def validate_config(cls, tenant_id: str, config: dict) -> None:
        """
        验证传入的表单配置数据。

        :param tenant_id: 工作空间的id
        :param config: 表单配置数据
        :return:
        """
        raise NotImplementedError

    @abstractmethod
    def moderation_for_inputs(self, inputs: dict, query: str = "") -> ModerationInputsResult:
        """
        对输入内容进行审核。
        在用户输入后，调用此方法对用户输入进行敏感内容审核，并返回处理后的结果。

        :param inputs: 用户输入
        :param query: 查询字符串（在聊天应用中必需）
        :return:
        """
        raise NotImplementedError

    @abstractmethod
    def moderation_for_outputs(self, text: str) -> ModerationOutputsResult:
        """
        对输出内容进行审核。
        当LLM输出内容时，前端会将输出内容（可能进行分段）传递给此方法进行敏感内容审核，
        如果审核失败，则输出内容将被屏蔽。

        :param text: LLM的输出内容
        :return:
        """
        raise NotImplementedError

    @classmethod
    def _validate_inputs_and_outputs_config(self, config: dict, is_preset_response_required: bool) -> None:
        # inputs_config
        inputs_config = config.get("inputs_config")
        if not isinstance(inputs_config, dict):
            raise ValueError("inputs_config必须是一个字典")

        # outputs_config
        outputs_config = config.get("outputs_config")
        if not isinstance(outputs_config, dict):
            raise ValueError("outputs_config必须是一个字典")

        inputs_config_enabled = inputs_config.get("enabled")
        outputs_config_enabled = outputs_config.get("enabled")
        if not inputs_config_enabled and not outputs_config_enabled:
            raise ValueError("至少需要启用inputs_config或outputs_config中的一个")

        # preset_response
        if not is_preset_response_required:
            return

        if inputs_config_enabled:
            if not inputs_config.get("preset_response"):
                raise ValueError("inputs_config.preset_response是必需的")

            if len(inputs_config.get("preset_response")) > 100:
                raise ValueError("inputs_config.preset_response不得超过100个字符")

        if outputs_config_enabled:
            if not outputs_config.get("preset_response"):
                raise ValueError("outputs_config.preset_response是必需的")

            if len(outputs_config.get("preset_response")) > 100:
                raise ValueError("outputs_config.preset_response不得超过100个字符")


class ModerationException(Exception):
    pass