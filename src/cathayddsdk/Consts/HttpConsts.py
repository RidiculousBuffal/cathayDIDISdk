class MimeTypes:
    """
    存放所有MIME类型的常量
    """
    # 表单
    APPLICATION_X_WWW_FORM_URLENCODED = "application/x-www-form-urlencoded"
    MULTIPART_FORM_DATA = "multipart/form-data"

    # JSON
    APPLICATION_JSON = "application/json"
    APPLICATION_JSON_UTF8 = "application/json; charset=utf-8"

    # XML
    APPLICATION_XML = "application/xml"
    TEXT_XML = "text/xml"

    # 文本和HTML
    TEXT_PLAIN = "text/plain"
    TEXT_HTML = "text/html"

    # 图片
    IMAGE_JPEG = "image/jpeg"
    IMAGE_PNG = "image/png"

class HeaderNames:
    """
    存放所有请求头名称的常量
    """
    CONTENT_TYPE = "Content-Type"
    ACCEPT = "Accept"
    AUTHORIZATION = "Authorization"

