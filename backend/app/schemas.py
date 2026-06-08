from pydantic import BaseModel


class ReportResponse(BaseModel):
    """日報生成APIのレスポンススキーマ。"""

    report: str
