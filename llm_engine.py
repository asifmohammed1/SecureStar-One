import os
import json
import requests

# NVIDIA NIM CONFIG
# We prioritize the Environment Variable 'API_KEY' for security
NVIDIA_API_KEY = os.getenv("API_KEY", "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")
INVOKE_URL = "https://integrate.api.nvidia.com/v1/chat/completions"
MODEL_NAME = "nvidia/nemotron-mini-4b-instruct"

def call_llm(content: str, is_audit: bool = False):
    """Core interaction with Nvidia NIM API (build.nvidia.com)."""
    
    # Define the security researcher persona
    system_instr = (
        "You are an expert API Security Auditor. Analyze the provided endpoint logic for potential "
        "vulnerabilities (OWASP Top 10). Always start your response with 'STATUS: VULNERABLE' or 'STATUS: SECURE'."
        if is_audit else "You are SecureStar AI, a professional security consultant."
    )
    
    headers = {
        "Authorization": f"Bearer {NVIDIA_API_KEY}",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": system_instr},
            {"role": "user", "content": content}
        ],
        "temperature": 0.2,
        "top_p": 0.7,
        "max_tokens": 1024
    }
    
    try:
        response = requests.post(INVOKE_URL, headers=headers, json=payload, timeout=45)
        if response.status_code != 200:
            return f"Nvidia NIM Error {response.status_code}: {response.text}"
        
        data = response.json()
        return data['choices'][0]['message']['content']
    except Exception as e:
        return f"NIM Connection Failed: {str(e)}"

def run_vulnerability_scan(swagger_json_url: str = None, direct_url: str = None):
    """Parses API documentation and runs the security analysis using Nemotron-Mini."""
    endpoints = []
    
    # Handle Swagger/OpenAPI Specs
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
        except Exception as e:
            print(f"Swagger Parse Error: {e}")
    
    # Handle direct endpoint scan
    if not endpoints and direct_url:
        endpoints.append({"path": direct_url, "method": "GET", "summary": "Manual Scan"})

    report = "# 🛡️ Autonomous Security Audit Report\n\n"
    report += f"**Engine**: Nvidia NIM ({MODEL_NAME})\n\n---\n\n"
    
    if not endpoints:
        return "No valid endpoints found for analysis."

    # Scan top 10 endpoints
    for idx, ep in enumerate(endpoints[:10]):
        analysis = call_llm(json.dumps(ep), is_audit=True)
        status_icon = "❌" if "VULNERABLE" in analysis.upper() else "✅"
        report += f"### {status_icon} {idx+1}. `{ep['method']}` {ep['path']}\n{analysis}\n\n---\n"
    
    return report
