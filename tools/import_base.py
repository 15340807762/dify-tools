import psycopg2

class HuaweiCloudGaussDBBase:
    def __init__(self, host: str, port: int, user: str, password: str, database_name: str):
        self.conn_info = {
            "host": host,
            "port": port,
            "user": user,
            "password": password,
            "dbname": database_name,
        }

    def create_import_task(self, import_type: str, file_content: str, charset="UTF-8",
                           ignore_errors=False, remark="", schema="public"):
        if import_type.lower() != 'sql':
            raise NotImplementedError("当前只支持 SQL 类型导入")

        conn = psycopg2.connect(**self.conn_info)
        try:
            with conn:
                with conn.cursor() as cur:
                    # ✅ 设置 search_path，保证后续表名解析在指定 schema 中
                    cur.execute(f"SET search_path TO {schema}")

                    # ✅ 执行 SQL 内容（无需替换 schema 前缀）
                    cur.execute(file_content)

            return {"task_id": "local-exec-001", "remark": remark}
        except Exception as e:
            if ignore_errors:
                return {"task_id": "local-exec-001", "remark": remark, "error": str(e)}
            else:
                raise
        finally:
            conn.close()

    def execute_query(self, query: str, schema="public", limit=100):
        conn = psycopg2.connect(**self.conn_info)
        try:
            with conn:
                with conn.cursor() as cur:
                    cur.execute(f"SET search_path TO {schema}")
                    cur.execute(query)
                    result = cur.fetchall()
                    columns = [desc[0] for desc in cur.description]
                    return {"columns": columns, "rows": result}
        finally:
            conn.close()
