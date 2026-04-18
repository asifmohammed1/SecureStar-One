import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import gradio as gr
import os
import logging
import sys

# Setup Logging for Cloud Run debugging
logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger("securestar")

try:
    from api_routes import router as api_router
    from ui_layout import build_ui
except ImportError as e:
    logger.error(f"STARTUP ERROR: Missing modules. {e}")
    sys.exit(1)

app = FastAPI(title="SecureStar One")
app.include_router(api_router)

# Mount Gradio
try:
    ui_app = build_ui()
    app = gr.mount_gradio_app(app, ui_app, path="/ui")
except Exception as e:
    logger.error(f"STARTUP ERROR: Failed to mount Gradio. {e}")

@app.get("/", response_class=HTMLResponse)
async def read_index():
    path = os.path.join(os.path.dirname(__file__), "templates", "index.html")
    if not os.path.exists(path):
        logger.error(f"CRITICAL: templates/index.html not found at {path}")
        return "System Calibration Error: UI File Not Found"
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

if __name__ == "__main__":
    # Cloud Run assigns a PORT env var
    port = int(os.environ.get("PORT", 8080))
    logger.info(f"Starting SecureStar One on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)
