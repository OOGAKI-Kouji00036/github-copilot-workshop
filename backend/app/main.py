import logging

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from openai import BadRequestError

from app.schemas import ReportResponse
from app.services.azure_openai_service import AzureOpenAIReportService

logger = logging.getLogger(__name__)

load_dotenv()

app = FastAPI(title="Daily Report Generator API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health_check() -> dict[str, str]:
    """ヘルスチェック用エンドポイント。"""
    return {"status": "ok"}


@app.post("/api/reports/generate", response_model=ReportResponse)
async def generate_daily_report(image: UploadFile = File(...)) -> ReportResponse:
    """アップロード画像から日報を生成して返す。"""
    try:
        data = await image.read()

        service = AzureOpenAIReportService()
        report_text = service.generate_report(data)

        return ReportResponse(report=report_text)
    except ValueError as exc:
        message = str(exc)
        if "上限" in message:
            raise HTTPException(status_code=413, detail=message) from exc
        raise HTTPException(status_code=400, detail=message) from exc
    except RuntimeError as exc:
        logger.exception("モデル応答処理でエラーが発生しました。")
        raise HTTPException(status_code=502, detail="AI応答の解析に失敗しました。") from exc
    except BadRequestError as exc:
        logger.warning("Azure OpenAIへの入力が不正です: %s", exc)
        raise HTTPException(
            status_code=400,
            detail="画像を解析できませんでした。別の画像でお試しください。",
        ) from exc
    except Exception as exc:  # noqa: BLE001
        logger.exception("日報生成APIで予期せぬエラーが発生しました。")
        raise HTTPException(status_code=502, detail="日報生成に失敗しました。") from exc
