import hashlib
import logging  # 1. 导入 logging 模块
import os
import time
from typing import Dict, Any, Optional

import httpx

from . import limits, timeout


class DIDIBaseClient:
    """
    滴滴企业版 API 客户端基类 (异步版本)。

    该类封装了必要的认证信息、签名逻辑和 access_token 的获取与管理。
    所有网络请求均使用 httpx 进行异步操作。
    """
    BASE_URL = "https://api.es.xiaojukeji.com/"

    def __init__(self, client_id: Optional[str] = None, client_secret: Optional[str] = None,
                 sign_key: Optional[str] = None, phone_number: Optional[str] = None,
                 logger: Optional[logging.Logger] = None):  # 2. 新增 logger 参数
        """
        初始化客户端。

        初始化顺序：
        1. 检查是否通过方法参数传入。
        2. 如果参数未传入，则尝试从环境变量中获取 (例如: DIDI_CLIENT_ID)。
        3. 如果两种方式都无法获取到值，则会抛出 ValueError。

        Args:
            client_id (str, optional): 您的 Client ID. 默认为 None.
            client_secret (str, optional): 您的 Client Secret. 默认为 None.
            sign_key (str, optional): 您的 Sign Key. 默认为 None.
            phone_number (str, optional): 您的 Phone Number (如果业务需要). 默认为 None.
            logger (logging.Logger, optional): 自定义的日志记录器实例. 如果为 None, 则创建一个默认的 logger.

        Raises:
            ValueError: 当某个必要的配置项既没有通过参数传入，也未在环境变量中设置时抛出。
        """
        self.client_id = client_id or os.getenv('DIDI_CLIENT_ID')
        self.client_secret = client_secret or os.getenv('DIDI_CLIENT_SECRET')
        self.sign_key = sign_key or os.getenv('DIDI_SIGN_KEY')
        self.phone_number = phone_number or os.getenv('DIDI_PHONE_NUMBER')

        # 2. 初始化 logger
        if logger:
            self.logger = logger
        else:
            self.logger = logging.getLogger(__name__)
            if not self.logger.handlers:  # 防止重复添加 handler
                handler = logging.StreamHandler()
                formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
                handler.setFormatter(formatter)
                self.logger.addHandler(handler)
                self.logger.setLevel(logging.INFO)

        if not self.client_id:
            raise ValueError("配置错误: 'DIDI_CLIENT_ID' 必须通过参数或环境变量提供。")
        if not self.client_secret:
            raise ValueError("配置错误: 'DIDI_CLIENT_SECRET' 必须通过参数或环境变量提供。")
        if not self.sign_key:
            raise ValueError("配置错误: 'DIDI_SIGN_KEY' 必须通过参数或环境变量提供。")

        self._access_token: Optional[str] = None
        self._token_expires_at: int = 0

    def _generate_sign(self, params: Dict[str, Any], sign_method: str = 'md5') -> str:
        """
        根据滴滴的规则生成签名 (这是一个同步的 CPU 密集型操作，无需异步)。

        Args:
            params (Dict[str, Any]): 参与签名的参数字典。
            sign_method (str, optional): 加密方法，'md5' 或 'sha256'。默认为 'md5'。

        Returns:
            str: 计算出的签名字符串（小写）。
        """
        temp_params = params.copy()
        temp_params['sign_key'] = self.sign_key
        sorted_keys = sorted(temp_params.keys())

        str_to_sign_parts = [f"{key}={str(temp_params[key]).strip()}" for key in sorted_keys]
        str_to_sign = "&".join(str_to_sign_parts)

        if sign_method.lower() == 'sha256':
            return hashlib.sha256(str_to_sign.encode('utf-8')).hexdigest()
        else:
            return hashlib.md5(str_to_sign.encode('utf-8')).hexdigest()

    async def get_access_token(self, force_refresh: bool = False) -> Dict[str, Any]:
        """
        异步获取接口访问凭证 access_token。

        该方法会自动处理签名，并内置了简单的内存缓存机制。
        在 token 过期前，重复调用将直接返回缓存的结果，除非使用 force_refresh=True。

        Args:
            force_refresh (bool, optional): 是否强制刷新 token，忽略缓存。默认为 False。

        Returns:
            Dict[str, Any]: 包含 access_token 和 expires_in 等信息的字典。

        Raises:
            httpx.RequestError: 当网络请求失败时。
            ValueError: 当 API 返回业务错误信息时。
        """
        if not force_refresh and self._access_token and self._token_expires_at > time.time() + 60:
            self.logger.debug("从缓存中返回有效的 access_token。")
            return {
                "access_token": self._access_token,
                "expires_in": int(self._token_expires_at - time.time()),
                "from_cache": True
            }

        # 3. 将 print 替换为 logger.info
        self.logger.info("正在向滴滴服务器异步请求新的 access_token...")
        endpoint = "/river/Auth/authorize"
        url = self.BASE_URL.rstrip('/') + endpoint

        payload = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": "client_credentials",
            "timestamp": int(time.time())
        }

        sign = self._generate_sign(payload)
        payload['sign'] = sign

        headers = {"Content-Type": "application/json"}

        try:
            async with httpx.AsyncClient(limits=limits, timeout=timeout) as client:
                response = await client.post(url, json=payload, headers=headers)
                response.raise_for_status()
                data = response.json()

            if data.get("errno", 0) != 0:
                raise ValueError(f"获取 token 失败: {data.get('errmsg', '未知错误')}", data)

            self._access_token = data.get("access_token")
            expires_in = data.get("expires_in", 1800)
            self._token_expires_at = int(time.time()) + expires_in
            self.logger.info("成功获取并缓存了新的 access_token。")
            return data

        except httpx.RequestError as e:
            self.logger.error(f"网络请求错误: {e}", exc_info=True)
            raise
        except ValueError as e:
            self.logger.error(f"API 逻辑错误: {e}", exc_info=True)
            raise
