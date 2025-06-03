from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage
from typing import Any
from collections.abc import Generator
from tools.import_base import HuaweiCloudGaussDBBase

class GaussDBImportTaskTool(Tool):
    def __init__(self, runtime, session):
        super().__init__(runtime, session)
        self.client = None

    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        host = tool_parameters.get("host")
        port = tool_parameters.get("port")
        user = tool_parameters.get("user")
        password = tool_parameters.get("password")
        database_name = tool_parameters.get("database_name")
        import_type = tool_parameters.get("import_type")
        file_content = tool_parameters.get("file_content")
        schema = tool_parameters.get("schema", "public")  # 默认使用 public

        # 参数校验
        if not all([host, port, user, password, database_name, import_type, file_content]):
            yield self.create_text_message("错误：缺少必要的数据库连接参数或导入参数")
            return

        self.client = HuaweiCloudGaussDBBase(host, port, user, password, database_name)

        try:
            result = self.client.create_import_task(
                import_type=import_type,
                file_content=file_content,
                charset=tool_parameters.get('charset', 'UTF-8'),
                ignore_errors=tool_parameters.get('ignore_errors', False),
                remark=tool_parameters.get('remark', ""),
                schema=schema  # ✅ 设置指定 schema
            )
            yield self.create_text_message(f"✅ 导入任务成功，任务ID：{result.get('task_id', '未知')}")
        except Exception as e:
            yield self.create_text_message(f"❌ 导入任务失败，错误：{str(e)}")

