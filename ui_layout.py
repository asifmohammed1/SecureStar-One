import gradio as gr
from llm_engine import run_vulnerability_scan, call_llm

def build_ui():
    css = ".report-box { border: 1px solid #222; padding: 20px; border-radius: 12px; background: #07090e; color: #eee; height: 600px; overflow-y: auto; }"
    
    with gr.Blocks(css=css, theme=gr.themes.Soft(primary_hue="blue")) as demo:
        with gr.Tabs():
            with gr.TabItem("🔎 SCANNER"):
                gr.Markdown("## API Security Auditor")
                with gr.Row():
                    api_in = gr.Textbox(label="API URL", placeholder="Target endpoint")
                    swag_in = gr.Textbox(label="Swagger URL", value="http://localhost:8000/openapi.json")
                scan_btn = gr.Button("RUN FULL AUDIT", variant="primary")
                report_out = gr.Markdown(elem_classes="report-box", value="System Idle...")
                
                scan_btn.click(fn=run_vulnerability_scan, inputs=[swag_in, api_in], outputs=report_out)

            with gr.TabItem("💬 EXPERT CHAT"):
                gr.Markdown("## Security Specialist Chat")
                chat_in = gr.Textbox(label="Message", placeholder="Ask a security question...")
                chat_btn = gr.Button("SEND", variant="primary")
                chat_out = gr.Markdown(elem_classes="report-box", value="Awaiting input...")
                
                chat_btn.click(fn=lambda x: call_llm(x), inputs=chat_in, outputs=chat_out)
    
    return demo
