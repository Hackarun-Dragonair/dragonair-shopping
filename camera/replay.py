"""Manda para a Ronda Viva as contagens já geradas pelo contador.py.

Para a demo não depender de webcam, luz ou CPU na hora: o YOLO roda antes,
e o replay só reenvia os números no mesmo ritmo (ou mais rápido).

  python camera/replay.py --enviar http://localhost:5000
  python camera/replay.py --enviar http://localhost:5000 --velocidade 5
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from enviar import postar  # noqa: E402


def main() -> None:
    args = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    args.add_argument("--contagens", default=str(Path(__file__).with_name("contagens.json")))
    args.add_argument("--enviar", default="http://localhost:5000")
    args.add_argument("--velocidade", type=float, default=1.0, help="2 = duas vezes mais rápido")
    a = args.parse_args()

    contagens = json.loads(Path(a.contagens).read_text(encoding="utf-8"))
    anterior = None
    for item in contagens:
        if anterior is not None and item["t"] > anterior:
            time.sleep((item["t"] - anterior) / a.velocidade)
        anterior = item["t"]
        resposta = postar(a.enviar, "/eventos/camera", {"zona": item["zona"], "pessoas": item["pessoas"]})
        marca = f" -> ocorrência #{resposta['problema_id']} aberta" if resposta.get("novo") else ""
        if "erro" in resposta:
            marca = f" -> erro: {resposta}"
        print(f"[{item['t']:6.1f}s] {item['zona']}: {item['pessoas']} pessoas{marca}")


if __name__ == "__main__":
    main()
