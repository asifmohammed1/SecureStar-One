import json
import requests

# CONFIG
OPENROUTER_API_KEY = "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"
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL_NAME = "nvidia/nemotron-3-super-120b-a12b:free"

def call_llm(content: str, is_audit: bool = False):
    """Core interaction with OpenRouter."""
    system_instr = "Audit this API endpoint and start with 'STATUS: VULNERABLE' or 'STATUS: SECURE'." if is_audit else ""
    
    payload = {
        "model": MODEL_NAME,
        "messages": [{"role": "user", "content": f"{system_instr} {content}"}]
    }
    
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://securestar.one",
        "X-Title": "SecureStar One"
    }
    
    try:
        response = requests.post(OPENROUTER_URL, json=payload, headers=headers, timeout=30)
        if response.status_code != 200:
            return f"API error {response.status_code}: {response.text}"
        return response.json()['choices'][0]['message']['content']
    except Exception as e:
        return f"Network failure: {str(e)}"

def run_vulnerability_scan(swagger_json_url: str = None, direct_url: str = None):
    """Parses endpoints and runs the security analysis."""
    endpoints = []
    
    if swagger_json_url:
        try:
            res = requests.get(swagger_json_url, timeout=10)
            data = res.json()
            paths = data.get("paths", {})
            for path, methods in paths.items():
                for method, details in methods.items():
                    endpoints.append({
                        "path": path, 
                        "method": method.upper(), 
                        "summary": details.get("summary", "N/A")
                    })
        except: pass
    
    if not endpoints and direct_url:
        endpoints.append({"path": direct_url, "method": "GET", "summary": "Manual Scan"})

    report = "# 🛡️ Security Audit Results\n\n"
    for idx, ep in enumerate(endpoints[:10]):
        analysis = call_llm(json.dumps(ep), is_audit=True)
        status_icon = "❌" if "VULNERABLE" in analysis.upper() else "✅"
        report += f"### {status_icon} {idx+1}. `{ep['method']}` {ep['path']}\n{analysis}\n\n---\n"
    
    return report or "No endpoints found."
