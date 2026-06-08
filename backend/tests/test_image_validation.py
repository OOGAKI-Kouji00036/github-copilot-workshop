import base64

import pytest

from app.services.azure_openai_service import AzureOpenAIReportService


# 1x1 PNG画像のbase64（テスト用の固定データ）。
PNG_1X1_BASE64 = (
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGD4DwAB"
    "BAEAX+XDSQAAAABJRU5ErkJggg=="
)


def _service_without_init() -> AzureOpenAIReportService:
    """外部依存初期化を避けるために__new__でインスタンス化する。"""
    return AzureOpenAIReportService.__new__(AzureOpenAIReportService)


def test_validate_image_accepts_png() -> None:
    """PNG画像は許可されることを確認する。"""
    service = _service_without_init()
    image_data = base64.b64decode(PNG_1X1_BASE64)

    mime_type = service.validate_image(image_data)

    assert mime_type == "image/png"


def test_validate_image_rejects_non_image() -> None:
    """画像以外の入力は拒否されることを確認する。"""
    service = _service_without_init()

    with pytest.raises(ValueError, match="JPEG / PNG"):
        service.validate_image(b"plain-text")


def test_validate_image_rejects_too_large_file() -> None:
    """上限超過サイズは拒否されることを確認する。"""
    service = _service_without_init()
    oversized_data = b"\x89PNG\r\n\x1a\n" + b"0" * (6 * 1024 * 1024)

    with pytest.raises(ValueError, match="上限"):
        service.validate_image(oversized_data)
