from core.extension.extensible import ModuleExtension, ExtensionModule
from core.external_data_tool.base import ExternalDataTool
from core.moderation.base import Moderation

class Extension:
    # 模块扩展字典，用于存储模块和模块扩展的对应关系
    __module_extensions: dict[str, dict[str, ModuleExtension]] = {}

    # 模块类字典，用于存储模块类的类型
    module_classes = {
        ExtensionModule.MODERATION: Moderation,  # 模块类型为MODERATION时，使用Moderation类
        ExtensionModule.EXTERNAL_DATA_TOOL: ExternalDataTool  # 模块类型为EXTERNAL_DATA_TOOL时，使用ExternalDataTool类
    }

    def init(self):
        # 初始化模块扩展字典
        for module, module_class in self.module_classes.items():
            self.__module_extensions[module.value] = module_class.scan_extensions()

    def module_extensions(self, module: str) -> list[ModuleExtension]:
        # 获取指定模块的所有模块扩展
        module_extensions = self.__module_extensions.get(module)

        if not module_extensions:
            raise ValueError(f"Extension Module {module} not found")

        return list(module_extensions.values())

    def module_extension(self, module: ExtensionModule, extension_name: str) -> ModuleExtension:
        # 根据模块和模块扩展名称获取对应的模块扩展
        module_extensions = self.__module_extensions.get(module.value)

        if not module_extensions:
            raise ValueError(f"Extension Module {module} not found")

        module_extension = module_extensions.get(extension_name)

        if not module_extension:
            raise ValueError(f"Extension {extension_name} not found")

        return module_extension

    def extension_class(self, module: ExtensionModule, extension_name: str) -> type:
        # 获取模块扩展的类
        module_extension = self.module_extension(module, extension_name)
        return module_extension.extension_class

    def validate_form_schema(self, module: ExtensionModule, extension_name: str, config: dict) -> None:
        # 验证表单模式
        module_extension = self.module_extension(module, extension_name)
        form_schema = module_extension.form_schema

        # TODO validate form_schema