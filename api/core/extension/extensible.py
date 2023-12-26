import enum
import importlib.util
import json
import logging
import os
from collections import OrderedDict
from typing import Any, Optional

from pydantic import BaseModel


class ExtensionModule(enum.Enum):
    """
    扩展模块枚举类

    用于表示不同的扩展模块类型

    Attributes:
        MODERATION (str): 指定模块为 MODERATION 
        EXTERNAL_DATA_TOOL (str): 指定模块为 EXTERNAL_DATA_TOOL 外部数据工具
    """
    MODERATION = 'moderation'
    EXTERNAL_DATA_TOOL = 'external_data_tool'


class ModuleExtension(BaseModel):
    extension_class: Any
    name: str
    label: Optional[dict] = None
    form_schema: Optional[list] = None
    builtin: bool = True
    position: Optional[int] = None


class Extensible:
    module: ExtensionModule

    name: str
    tenant_id: str
    config: Optional[dict] = None

    def __init__(self, tenant_id: str, config: Optional[dict] = None) -> None:
        self.tenant_id = tenant_id
        self.config = config

    @classmethod
    def scan_extensions(cls):
        """
        扫描扩展模块函数

        Args:
            cls: 扩展类

        Returns:
            OrderedDict: 排序后的扩展模块字典
        """

        extensions = {}

        # 获取当前类的路径
        current_path = os.path.abspath(cls.__module__.replace(".", os.path.sep) + '.py')
        current_dir_path = os.path.dirname(current_path)

        # 遍历子目录
        for subdir_name in os.listdir(current_dir_path):
            if subdir_name.startswith('__'):
                continue

            subdir_path = os.path.join(current_dir_path, subdir_name)
            extension_name = subdir_name
            if os.path.isdir(subdir_path):
                file_names = os.listdir(subdir_path)

                # 是否为内置扩展，前端页面和业务逻辑中会有特殊处理
                builtin = False
                position = None
                if '__builtin__' in file_names:
                    builtin = True

                    builtin_file_path = os.path.join(subdir_path, '__builtin__')
                    if os.path.exists(builtin_file_path):
                        with open(builtin_file_path, 'r') as f:
                            position = int(f.read().strip())

                # 如果缺少 {extension_name}.py 文件，则跳过
                if (extension_name + '.py') not in file_names:
                    logging.warning(f"在 {subdir_path} 中缺少 {extension_name}.py 文件，跳过。")
                    continue

                # 动态加载 {subdir_name}.py 文件并找到 Extensible 子类
                py_path = os.path.join(subdir_path, extension_name + '.py')
                spec = importlib.util.spec_from_file_location(extension_name, py_path)
                mod = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(mod)

                extension_class = None
                for name, obj in vars(mod).items():
                    # 如果 obj 是 cls 的子类且不等于 cls，则将其赋值给 extension_class
                    if isinstance(obj, type) and issubclass(obj, cls) and obj != cls:
                        extension_class = obj
                        break

                # 如果没有找到 cls 的子类，则跳过
                if not extension_class:
                    logging.warning(f"在 {py_path} 中缺少 {cls.__name__} 的子类，跳过。")
                    continue

                json_data = {}
                if not builtin:
                    # 如果缺少 schema.json 文件，则跳过
                    if 'schema.json' not in file_names:
                        logging.warning(f"在 {subdir_path} 中缺少 schema.json 文件，跳过。")
                        continue

                    json_path = os.path.join(subdir_path, 'schema.json')
                    json_data = {}
                    if os.path.exists(json_path):
                        with open(json_path, 'r') as f:
                            json_data = json.load(f)

                extensions[extension_name] = ModuleExtension(
                    extension_class=extension_class,
                    name=extension_name,
                    label=json_data.get('label'),
                    form_schema=json_data.get('form_schema'),
                    builtin=builtin,
                    position=position
                )

        # 按照 position 排序，如果没有 position，则排在前面
        sorted_items = sorted(extensions.items(), key=lambda x: (x[1].position is None, x[1].position))
        sorted_extensions = OrderedDict(sorted_items)

        return sorted_extensions
