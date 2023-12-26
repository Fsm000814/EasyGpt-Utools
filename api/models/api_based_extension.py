import enum

from sqlalchemy.dialects.postgresql import UUID

from extensions.ext_database import db


class APIBasedExtensionPoint(enum.Enum):
    """
    APIBasedExtensionPoint枚举类定义了可用的API扩展点类型。
    """
    APP_EXTERNAL_DATA_TOOL_QUERY = 'app.external_data_tool.query'  # 应用外部数据工具查询
    PING = 'ping'  # PING
    APP_MODERATION_INPUT = 'app.moderation.input'  # 应用审核输入
    APP_MODERATION_OUTPUT = 'app.moderation.output'  # 应用审核输出


class APIBasedExtension(db.Model):
    """
    APIBasedExtension类表示基于API的扩展，继承自db.Model。
    """

    __tablename__ = 'api_based_extensions'
    __table_args__ = (
        db.PrimaryKeyConstraint('id', name='api_based_extension_pkey'),
        db.Index('api_based_extension_tenant_idx', 'tenant_id'),
    )

    id = db.Column(UUID, server_default=db.text('uuid_generate_v4()'))  # 主键ID，生成方式为uuid_generate_v4()
    tenant_id = db.Column(UUID, nullable=False)  # 租户ID，不能为空
    name = db.Column(db.String(255), nullable=False)  # 名称，不能为空
    api_endpoint = db.Column(db.String(255), nullable=False)  # API端点，不能为空
    api_key = db.Column(db.Text, nullable=False)  # API密钥，不能为空
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.text('CURRENT_TIMESTAMP(0)'))  # 创建时间，不能为空，默认值为CURRENT_TIMESTAMP(0)