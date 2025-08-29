from flask import Flask, request, Response
from datetime import datetime, timezone
import os

app = Flask(__name__)

LOG_FILE = "requests_log.txt"
SEPARATOR = "-" * 50

def format_timestamp() -> str:
    """Retorna o timestamp atual em UTC no formato Apache/Nginx."""
    return datetime.now(timezone.utc).strftime("%d/%b/%Y:%H:%M:%S %z")

def get_client_ip() -> str:
    """Retorna o IP do cliente considerando proxy reverso."""
    return request.headers.get("X-Forwarded-For", request.remote_addr)

def format_log_entry() -> str:
    """Gera uma string de log para a requisição atual."""
    timestamp = format_timestamp()
    method = request.method
    path = request.path
    args = request.args.to_dict()
    body = request.data.decode("utf-8").strip() or "---"
    client_ip = get_client_ip()

    return (
        f"[{timestamp}] {method} {path} | IP: {client_ip}\n"
        f"Query: {args}\n"
        f"Body: {body}\n"
        f"{SEPARATOR}\n"
    )

def log_request():
    """Escreve a requisição no arquivo de log."""
    log_entry = format_log_entry()
    with open(LOG_FILE, "a", encoding="utf-8") as file:
        file.write(log_entry)

@app.route("/", defaults={"path": ""}, methods=["GET", "POST", "PUT", "PATCH", "DELETE"])
@app.route("/<path:path>", methods=["GET", "POST", "PUT", "PATCH", "DELETE"])
def catch_all(path: str) -> Response:
    """Captura qualquer requisição HTTP e registra no log."""
    log_request()
    return Response(status=200)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
