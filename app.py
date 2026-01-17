from flask import Flask
import os
import signal
import sys

app = Flask(__name__)
PID_FILE = "service.pid"

@app.route("/health")
def health():
    return {"status": "ok"}, 200


def shutdown_handler(signum, frame):
    if os.path.exists(PID_FILE):
        os.remove(PID_FILE)
    sys.exit(0)


if __name__ == "__main__":
    # Guardar PID
    with open(PID_FILE, "w") as f:
        f.write(str(os.getpid()))

    # Capturar señales de apagado
    signal.signal(signal.SIGTERM, shutdown_handler)
    signal.signal(signal.SIGINT, shutdown_handler)

    app.run(host="0.0.0.0", port=8080)
