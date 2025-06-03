# query.py
from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage
from typing import Any
from collections.abc import Generator
from tools.import_base import HuaweiCloudGaussDBBase

class GaussDBQueryTool(Tool):
    def __init__(self, runtime, session):
        super().__init__(runtime, session)
        self.client = None

    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        host = tool_parameters.get("host")
        port = tool_parameters.get("port")
        user = tool_parameters.get("user")
        password = tool_parameters.get("password")
        database_name = tool_parameters.get("database_name")
        sql_query = tool_parameters.get("sql_query")
        schema = tool_parameters.get("schema", "public")

        if not all([host, port, user, password, database_name, sql_query]):
            yield self.create_text_message("错误：缺少必要的数据库连接参数或 SQL 查询语句")
            return

        self.client = HuaweiCloudGaussDBBase(host, port, user, password, database_name)

        try:
            result = self.client.execute_query(query=sql_query, schema=schema)

            columns = result["columns"]
            rows = result["rows"]

            # 格式化结果
            formatted_result = " | ".join(columns) + "\n"
            formatted_result += "-" * 40 + "\n"
            for row in rows:
                formatted_result += " | ".join(map(str, row)) + "\n"

            yield self.create_text_message(f"✅ 查询成功：\n```\n{formatted_result}```")
        except Exception as e:
            yield self.create_text_message(f"❌ 查询失败，错误：{str(e)}")

