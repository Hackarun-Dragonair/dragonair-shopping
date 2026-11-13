import os
import threading
import webbrowser

from app import create_app

app = create_app()


if __name__ == "__main__":
    porta = int(os.environ.get("PORT", "8000"))

    def abrir_navegador() -> None:
        webbrowser.open(f"http://127.0.0.1:{porta}/")

    threading.Timer(1.0, abrir_navegador).start()
    app.run(host="0.0.0.0", port=porta)
