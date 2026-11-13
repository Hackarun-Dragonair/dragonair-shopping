"""Sensor de fumaça SIMULADO (não existe sensor físico na demo).

  python camera/simular_sensor.py --zona doca-1

No roadmap: ESP32 + sensor MQ-2 mandando este mesmo JSON.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from enviar import postar  # noqa: E402

if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--zona", default="doca-1")
    args.add_argument("--enviar", default="http://localhost:5000")
    a = args.parse_args()
    print(postar(a.enviar, "/eventos/sensor", {"zona": a.zona, "tipo": "fumaca", "simulado": True}))
