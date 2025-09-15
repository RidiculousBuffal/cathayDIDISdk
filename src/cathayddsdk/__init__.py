import httpx

limits = httpx.Limits(max_connections=1000, max_keepalive_connections=200)
timeout = httpx.Timeout(None, connect=40.0)  # 设置时间限制