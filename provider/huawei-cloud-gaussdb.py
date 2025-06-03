from typing import Any
import logging
from dify_plugin import ToolProvider
from dify_plugin.errors.tool import ToolProviderCredentialValidationError
from huaweicloudsdkcore.auth.credentials import BasicCredentials
from huaweicloudsdkcore.http.http_config import HttpConfig
from huaweicloudsdkrds.v3 import RdsClient, ListInstancesRequest

logger = logging.getLogger(__name__)

class HuaweiCloudGaussDBProvider(ToolProvider):
    def _validate_credentials(self, credentials: dict[str, Any]) -> None:
        try:
            # 获取认证信息
            ak = credentials.get("access_key_id")
            sk = credentials.get("secret_access_key")
            project_id = credentials.get("project_id")
            server_url = credentials.get("server_url", "https://rds.cn-north-4.myhuaweicloud.com")
            dify_endpoint = credentials.get("dify_endpoint", "")
            logger.info(f"Dify endpoint provided: {dify_endpoint}")

            # 验证必填参数
            if not ak:
                raise ToolProviderCredentialValidationError("AccessKeyID is required.")
            if not sk:
                raise ToolProviderCredentialValidationError("SecretAccessKey is required.")
            if not project_id:
                raise ToolProviderCredentialValidationError("Project ID is required.")

            # 初始化认证
            credentials = BasicCredentials(ak, sk, project_id)
            config = HttpConfig.get_default_config()
            config.ignore_ssl_verification = True

            # 初始化 RDS 客户端
            client = RdsClient.new_builder()\
                .with_http_config(config)\
                .with_credentials(credentials)\
                .with_endpoint(server_url)\
                .build()

            # 测试连接
            request = ListInstancesRequest()
            response = client.list_instances(request)

            # 如果能获取到实例列表，说明认证成功
            logger.info(f"Connection successful. Found {len(response.instances)} instances.")
        except Exception as e:
            raise ToolProviderCredentialValidationError(f"Credential validation failed: {str(e)}")


