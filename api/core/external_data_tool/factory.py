from typing import Optional

from core.extension.extensible import ExtensionModule
from extensions.ext_code_based_extension import code_based_extension


class ExternalDataToolFactory:
    """
    外部数据工具工厂类
    """

    def __init__(self, name: str, tenant_id: str, app_id: str, variable: str, config: dict) -> None:
        """
        初始化方法
        :param name: 外部数据工具的名称
        :param tenant_id: 工作区的ID
        :param app_id: 应用的ID
        :param variable: 变量
        :param config: 配置数据
        """
        extension_class = code_based_extension.extension_class(ExtensionModule.EXTERNAL_DATA_TOOL, name)
        self.__extension_instance = extension_class(
            tenant_id=tenant_id,
            app_id=app_id,
            variable=variable,
            config=config
        )

    @classmethod
    def validate_config(cls, name: str, tenant_id: str, config: dict) -> None:
        """
        验证表单配置数据
        :param name: 外部数据工具的名称
        :param tenant_id: 工作区的ID
        :param config: 表单配置数据
        """
        code_based_extension.validate_form_schema(ExtensionModule.EXTERNAL_DATA_TOOL, name, config)
        extension_class = code_based_extension.extension_class(ExtensionModule.EXTERNAL_DATA_TOOL, name)
        extension_class.validate_config(tenant_id, config)

    def query(self, inputs: dict, query: Optional[str] = None) -> str:
        """
        查询外部数据工具
        :param inputs: 用户输入
        :param query: 聊天应用的查询
        :return: 工具的查询结果
        """
        return self.__extension_instance.query(inputs, query)