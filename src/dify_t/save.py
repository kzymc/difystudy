from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from datetime import datetime
from pathlib import Path
import json

app = FastAPI()

SAVE_DIR = Path("./saved")
SAVE_DIR.mkdir(exist_ok=True)


@app.post("/save")
async def save_data(request: Request):
    # 1. 拿到原始 body（不预设结构，Dify 发什么就收什么）
    raw_body = await request.body()

    # 2. 尝试解析成 JSON
    try:
        data = json.loads(raw_body)
    except json.JSONDecodeError:
        # 不是 JSON 也照样存下来，便于排查
        data = {"_raw": raw_body.decode("utf-8", errors="replace")}

    # 3. 用时间戳命名，避免覆盖
    ts = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    file_path = SAVE_DIR / f"payload_{ts}.json"

    # 4. 落盘（ensure_ascii=False 让中文可读，indent=2 方便人看）
    file_path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    # 5. 返回给 Dify，Dify 的 HTTP 节点会拿到这个响应
    return JSONResponse(
        status_code=200,
        content={"ok": True, "saved_to": str(file_path)},
    )


@app.get("/health")
async def health():
    return {"status": "up"}