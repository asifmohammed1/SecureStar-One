import os
import json
import requests
import uvicorn
from fastapi import FastAPI, HTTPException
import gradio as gr
from typing import List, Dict, Optional

# --- CONFIGURATION ---
OPENROUTER_API_KEY = "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"
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL_NAME = "google/gemini-2.0-flash-lite-preview-02-05:free"

app = FastAPI(title="SecureStar One API Scanner")

def call_llm_analysis(endpoint_data: str):
    """Calls OpenRouter LLM to analyze endpoint security."""
    prompt = f"""
    You are an expert API Security Researcher. Analyze the following API endpoint details and identify potential vulnerabilities based on OWASP API Top 10 (e.g., BOLA, Broken Authentication, Mass Assignment, Injection, etc.).
    
    API Endpoint Details:
    {endpoint_data}
    
    Provide a concise report for this endpoint:
    1. Potential Vulnerabilities
    2. Severity (High/Medium/Low)
    3. Recommended Fix
    """
    
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": "You are a professional security auditor."},
            {"role": "user", "content": prompt}
        ]
    }
    
    try:
        response = requests.post(OPENROUTER_URL, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']
    except Exception as e:
        return f"Error analyzing endpoint: {str(e)}"

def scan_api(target_url: str, swagger_url: str):
    """Main scanning logic."""
    report = []
    
    if not target_url and not swagger_url:
        return "Please provide at least an API URL or a Swagger Doc URL."

    # Try to fetch Swagger documentation if provided
    endpoints = []
    if swagger_url:
        try:
            res = requests.get(swagger_url, timeout=10)
            res.raise_for_status()
            swagger_data = res.json()
            
            # Simple parsing for OpenAPI/Swagger
            paths = swagger_data.get("paths", {})
            for path, methods in paths.items():
                for method, details in methods.items():
                    endpoints.append({
                        "path": path,
                        "method": method.upper(),
                        "summary": details.get("summary", "No summary"),
                        "parameters": details.get("parameters", [])
                    })
        except Exception as e:
            return f"Failed to fetch or parse Swagger Doc: {str(e)}"
    
    # If no swagger but we have a URL, we treat it as a single endpoint test
    if not endpoints and target_url:
        endpoints.append({
            "path": target_url,
            "method": "UNKNOWN (Direct URL Test)",
            "summary": "Manual Scan",
            "parameters": []
        })

    if not endpoints:
        return "No endpoints found to scan."

    # Analyze each endpoint
    full_report = "# 🛡️ SecureStar One: API Vulnerability Report\n\n"
    for ep in endpoints:
        ep_info = json.dumps(ep, indent=2)
        analysis = call_llm_analysis(ep_info)
        full_report += f"## Endpoint: `{ep['method']}` {ep['path']}\n"
        full_report += f"**Summary**: {ep['summary']}\n\n"
        full_report += f"{analysis}\n"
        full_report += "---\n\n"
    
    return full_report

# --- GRADIO UI ---
with gr.Blocks(theme=gr.themes.Soft(primary_hue="blue", secondary_hue="slate")) as ui:
    gr.Markdown(
        """
        # 🛡️ SecureStar One API Security Scanner
        ### Secure your Large-Scale Event Infrastructure
        Enter your API endpoint or Swagger documentation URL to perform a vulnerability audit using AI.
        """
    )
    
    with gr.Row():
        api_url = gr.Textbox(label="Base API URL (Optional)", placeholder="https://api.example.com")
        swagger_url = gr.Textbox(label="Swagger/OpenAPI JSON URL", placeholder="https://api.example.com/swagger.json")
    
    scan_btn = gr.Button("🚀 Start Security Scan", variant="primary")
    
    output = gr.Markdown(label="Security Audit Report")
    
    scan_btn.click(
        fn=scan_api,
        inputs=[api_url, swagger_url],
        outputs=output
    )

# Mount Gradio app into FastAPI
app = gr.mount_gradio_app(app, ui, path="/")

if __name__ == "__main__":
    # Running in a single file suitable for Cloud Run / App Engine
    uvicorn.run(app, host="0.0.0.0", port=8000)
