import base64
import os
from typing import Final

from openai import AzureOpenAI


MAX_IMAGE_SIZE_BYTES: Final[int] = 5 * 1024 * 1024
ALLOWED_IMAGE_TYPES: Final[set[str]] = {"jpeg", "png"}


def _detect_image_type(data: bytes) -> str | None:
    """マジックナンバーから画像形式を判定する。"""
    if data.startswith(b"\x89PNG\r\n\x1a\n"):
        return "png"

    if data.startswith(b"\xFF\xD8\xFF"):
        return "jpeg"

    return None


class AzureOpenAIReportService:
    """Azure OpenAIを用いて画像から日報テキストを生成するサービス。"""

    def __init__(self) -> None:
        """環境変数からAzure OpenAIクライアント設定を読み込む。"""
        self._endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        self._api_key = os.getenv("AZURE_OPENAI_API_KEY")
        self._deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")
        self._api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2024-08-01-preview")

        if not self._endpoint or not self._api_key or not self._deployment:
            raise ValueError(
                "AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_API_KEY, "
                "AZURE_OPENAI_DEPLOYMENT を設定してください。"
            )

        # Azure OpenAI用のSDKクライアントを初期化する。
        self._client = AzureOpenAI(
            azure_endpoint=self._endpoint,
            api_key=self._api_key,
            api_version=self._api_version,
        )

    def validate_image(self, data: bytes) -> str:
        """入力画像の容量と形式を検証し、MIME typeを返す。"""
        if not data:
            raise ValueError("画像データが空です。")

        if len(data) > MAX_IMAGE_SIZE_BYTES:
            raise ValueError("画像サイズが上限(5MB)を超えています。")

        image_type = _detect_image_type(data)
        if image_type not in ALLOWED_IMAGE_TYPES:
            raise ValueError("対応形式は JPEG / PNG のみです。")

        if image_type == "jpeg":
            return "image/jpeg"

        return "image/png"

    def generate_report(self, image_data: bytes) -> str:
        """画像をAzure OpenAIへ送信し、日報Markdownを返す。"""
        mime_type = self.validate_image(image_data)
        b64 = base64.b64encode(image_data).decode("utf-8")

        system_prompt = (
            "あなたは業務日報作成アシスタントです。"
            "入力画像から読み取れる作業内容を要約し、"
            "必ず日本語でMarkdown形式の3セクションを出力してください。"
            "セクション見出しは必ず『作業内容』『進捗状況』『課題・問題点』にしてください。"
            "不明点は推測しすぎず、必要なら『確認が必要』と記載してください。"
        )

        user_prompt = "この画像から、日報を作成してください。"

        response = self._client.chat.completions.create(
            model=self._deployment,
            messages=[
                {"role": "system", "content": system_prompt},
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": user_prompt},
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:{mime_type};base64,{b64}"},
                        },
                    ],
                },
            ],
            temperature=0.2,
            max_tokens=900,
        )

        content = response.choices[0].message.content
        if not content:
            raise RuntimeError("モデル応答が空です。")

        return content.strip()
