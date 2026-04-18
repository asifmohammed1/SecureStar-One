import gradio as gr
from llm_engine import run_vulnerability_scan, call_llm

def build_ui():
    css = ".report-box { border: 1px solid #222; padding: 20px; border-radius: 12px; background: #07090e; color: #eee; height: 600px; overflow-y: auto; }"
    
    with gr.Blocks(css=css, theme=gr.themes.Soft(primary_hue="blue")) as demo:
        gr.Markdown("# 🛡️ SecureStar One: AI Security Auditor")
        
        with gr.Tabs():
            with gr.TabItem("🔎 AI SCANNER"):
                gr.Markdown("## Production API Security Audit")
                with gr.Row():
                    api_in = gr.Textbox(label="API URL", placeholder="Target endpoint (Internal or External)")
                    swag_in = gr.Textbox(label="Swagger URL", value="https://securestar-one-1034435897603.us-central1.run.app/openapi.json")
                scan_btn = gr.Button("RUN FULL AUDIT", variant="primary")
                report_out = gr.Markdown(elem_classes="report-box", value="System Idle. Ready for assessment.")
                
                scan_btn.click(fn=run_vulnerability_scan, inputs=[swag_in, api_in], outputs=report_out)

            with gr.TabItem("💬 EXPERT CHAT"):
                gr.Markdown("## Security Specialist Chat")
                chat_in = gr.Textbox(label="Message", placeholder="Consult the AI on remediation strategies...")
                chat_btn = gr.Button("SEND MESSAGE", variant="primary")
                chat_out = gr.Markdown(elem_classes="report-box", value="Awaiting input...")
                
                chat_btn.click(fn=lambda x: call_llm(x), inputs=chat_in, outputs=chat_out)
    
    return demo
