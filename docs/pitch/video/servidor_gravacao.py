"""Liga o Ronda Viva só para a gravação do vídeo, com banco novo e dados fictícios do seed.

Uso (na raiz do projeto):  .venv/bin/python docs/pitch/video/servidor_gravacao.py [porta] [pasta_temporaria]
O banco é apagado e semeado de novo a cada início, então toda gravação começa igual.
"""
import shutil
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(RAIZ))

from app import create_app  # noqa: E402

porta = int(sys.argv[1]) if len(sys.argv) > 1 else 8778
pasta = Path(sys.argv[2] if len(sys.argv) > 2 else "/tmp/ronda-viva-video")
shutil.rmtree(pasta, ignore_errors=True)
pasta.mkdir(parents=True)

app = create_app({
    "DATABASE": str(pasta / "ronda.sqlite3"),
    "PLANTAS_DIR": str(pasta / "plantas"),  # pasta vazia: nenhuma planta real é usada
    "SEXTA13": "0",  # sem o gato da sexta-feira 13 no vídeo
})
app.run(host="127.0.0.1", port=porta)
