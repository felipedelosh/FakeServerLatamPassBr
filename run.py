"""
FelipedelosH
    2026

API - FAKE - LATAM_PASS_BR

BASE: .../sandbox/API/...
"""

from threading import Thread
from werkzeug.serving import make_server
from app.router import create_app

class ServerThread(Thread):
    def __init__(self, app, host: str, port: int) -> None:
        super().__init__(daemon=True)
        self.server = make_server(host, port, app)
        self.ctx = app.app_context()
        self.ctx.push()
        self.host = host
        self.port = port

    def run(self) -> None:
        print(f"[LATAM PASS BR FAKE SERVER] running on http://{self.host}:{self.port}")
        self.server.serve_forever()

    def shutdown(self) -> None:
        self.server.shutdown()


if __name__ == "__main__":
    app = create_app()

    ports = [9001, 9002, 9003]
    servers = [ServerThread(app, "0.0.0.0", port) for port in ports]

    try:
        for server in servers:
            server.start()

        print("[LATAM PASS BR FAKE SERVER] all ports are up")
        for server in servers:
            server.join()

    except KeyboardInterrupt:
        print("\n[LATAM PASS BR FAKE SERVER] shutting down...")
        for server in servers:
            server.shutdown()