import os

import requests

from models.api_based_extension import APIBasedExtensionPoint


class APIBasedExtensionRequestor:
    timeout: (int, int) = (5, 60)
    """请求超时时间"""

    def __init__(self, api_endpoint: str, api_key: str) -> None:
        """
        初始化APIBasedExtensionRequestor对象。

        参数：
        api_endpoint - API端点地址
        api_key - API密钥
        """
        self.api_endpoint = api_endpoint
        self.api_key = api_key

    def request(self, point: APIBasedExtensionPoint, params: dict) -> dict:
        """
        请求API接口。

        参数：
        point - API接口类型
        params - 请求参数

        返回：
        API接口响应的JSON数据
        """
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(self.api_key)
        }

        url = self.api_endpoint

        try:
            # 支持安全性较高的代理
            proxies = None
            if os.environ.get("API_BASED_EXTENSION_HTTP_PROXY") and os.environ.get("API_BASED_EXTENSION_HTTPS_PROXY"):
                proxies = {
                    'http': os.environ.get("API_BASED_EXTENSION_HTTP_PROXY"),
                    'https': os.environ.get("API_BASED_EXTENSION_HTTPS_PROXY"),
                }

            response = requests.request(
                method='POST',
                url=url,
                json={  # 构建请求JSON数据
                    'point': point.value,
                    'params': params
                },
                headers=headers,
                timeout=self.timeout,  # 设置超时时间
                proxies=proxies
            )
        except requests.exceptions.Timeout:
            raise ValueError("请求超时")
        except requests.exceptions.ConnectionError:
            raise ValueError("请求连接错误")

        if response.status_code != 200:
            raise ValueError("请求错误，状态码：{}，内容：{}".format(
                response.status_code,
                response.text[:100]
            ))

        return response.json()