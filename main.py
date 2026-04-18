import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import gradio as gr
import os

from api_routes import router as api_router
from ui_layout import build_ui

# Initialize FastAPI
app = FastAPI(title="SecureStar One - Enterprise Edition")

# Include the API routes
app.include_router(api_router)

# Build and mount Gradio UI
ui_app = build_ui()
app = gr.mount_gradio_app(app, ui_app, path="/ui")

# Serve the premium index.html
@app.get("/", response_class=HTMLResponse)
async def read_index():
    path = os.path.join(os.path.dirname(__file__), "templates", "index.html")
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

if __name__ == "__main__":
    # Ensure port consistency for deployment
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
