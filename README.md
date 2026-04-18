# 🛡️ SecureStar One: API Security Scanner

This application is designed to secure large-scale sporting venue infrastructures by auditing their APIs for vulnerabilities. It uses **FastAPI** for the backend, **Gradio** for a premium UI, and **OpenRouter (Gemini 2.0 Flash Lite)** for AI-driven security analysis.

## 🚀 Features
- **Swagger/OpenAPI Support**: Automatically parses API documentation URLs.
- **AI Vulnerability Analysis**: Detects OWASP Top 10 flaws like BOLA, Broken Auth, and Injection.
- **Single-File Architecture**: Ready for easy deployment.
- **Gradio UI**: Modern, responsive interface.

## 🛠️ Local Setup
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the application:
   ```bash
   python app.py
   ```
3. Access the UI at `http://localhost:8000`.

## ☁️ Google Cloud Deployment (Cloud Run)
1. **Build the Container**:
   Create a `Dockerfile`:
   ```dockerfile
   FROM python:3.9-slim
   WORKDIR /app
   COPY . .
   RUN pip install -r requirements.txt
   EXPOSE 8080
   CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]
   ```
2. **Deploy**:
   ```bash
   gcloud run deploy securestar-scanner --source . --region us-central1 --allow-unauthenticated
   ```

## 🏟️ Physical Event Experience Context
SecureStar One addresses:
- **Crowd Movement**: Ensuring API endpoints for IoT sensors are secure.
- **Waiting Times**: Protects the "Dynamic Queueing" API from abuse.
- **Real-time Coordination**: Secures the data exchange between staff and security systems.
