"""Conta pessoas por zona num vídeo (ou webcam) e gera números. Nunca guarda imagem crua.

Como funciona, em 4 passos:
1. YOLOv8n (Ultralytics) acha as pessoas em cada quadro.
2. ByteTrack (supervision) dá um número para cada pessoa entre os quadros.
3. PolygonZone (supervision) conta quantas estão dentro de cada zona desenhada.
4. A cada N segundos salva {t, zona, pessoas} e, se pedido, manda para a Ronda Viva.

No vídeo de saída as pessoas aparecem PIXELADAS (privacidade/LGPD).

Exemplos:
  python camera/contador.py --fonte meu_video.mp4 --saida camera/contagens.json
  python camera/contador.py --fonte 0 --enviar http://localhost:5000   # webcam ao vivo
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

import cv2
import numpy as np
import supervision as sv
from ultralytics import YOLO

sys.path.insert(0, str(Path(__file__).resolve().parent))
from enviar import postar  # noqa: E402

PESSOA = 0  # classe "person" do dataset COCO


def carregar_zonas(caminho: Path, largura: int, altura: int) -> list[tuple[str, sv.PolygonZone]]:
    """Zonas em coordenadas de 0 a 1 (vale para qualquer resolução)."""
    zonas = []
    for item in json.loads(caminho.read_text(encoding="utf-8")):
        pontos = np.array([[x * largura, y * altura] for x, y in item["poligono"]], dtype=np.int32)
        zonas.append((item["zona"], sv.PolygonZone(polygon=pontos)))
    return zonas


def main() -> None:
    args = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    args.add_argument("--fonte", required=True, help="arquivo de vídeo ou 0 para webcam")
    args.add_argument("--zonas", default=str(Path(__file__).with_name("zonas.json")))
    args.add_argument("--saida", default=str(Path(__file__).with_name("contagens.json")))
    args.add_argument("--video-saida", default="", help="vídeo anotado e pixelado (opcional)")
    args.add_argument("--enviar", default="", help="URL da Ronda Viva, ex.: http://localhost:5000")
    args.add_argument("--intervalo", type=float, default=5.0, help="segundos entre contagens")
    args.add_argument("--confianca", type=float, default=0.35)
    args.add_argument("--mostrar", action="store_true", help="abre janela com o vídeo pixelado")
    a = args.parse_args()

    fonte = int(a.fonte) if a.fonte.isdigit() else a.fonte
    video = cv2.VideoCapture(fonte)
    if not video.isOpened():
        sys.exit(f"Não consegui abrir a fonte: {a.fonte}")
    fps = video.get(cv2.CAP_PROP_FPS) or 25
    largura = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    altura = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    zonas = carregar_zonas(Path(a.zonas), largura, altura)

    modelo = YOLO("yolov8n.pt")  # baixa ~6 MB na 1ª vez; depois roda offline
    rastreador = sv.ByteTrack()
    pixelar = sv.PixelateAnnotator(pixel_size=12)
    desenhos = [sv.PolygonZoneAnnotator(zone=z, color=sv.Color.YELLOW, thickness=2) for _n, z in zonas]

    gravador = None
    if a.video_saida:
        gravador = cv2.VideoWriter(a.video_saida, cv2.VideoWriter_fourcc(*"mp4v"), fps, (largura, altura))

    contagens: list[dict] = []
    quadro_n = 0
    proxima = 0.0
    ao_vivo = isinstance(fonte, int)
    inicio = time.time()
    while True:
        ok, quadro = video.read()
        if not ok:
            break
        t = (time.time() - inicio) if ao_vivo else quadro_n / fps
        quadro_n += 1

        resultado = modelo(quadro, classes=[PESSOA], conf=a.confianca, verbose=False)[0]
        deteccoes = rastreador.update_with_detections(sv.Detections.from_ultralytics(resultado))

        if t >= proxima:
            proxima = t + a.intervalo
            for nome, zona in zonas:
                pessoas = int(zona.trigger(detections=deteccoes).sum())
                contagens.append({"t": round(t, 1), "zona": nome, "pessoas": pessoas})
                print(f"[{t:6.1f}s] {nome}: {pessoas} pessoas")
                if a.enviar:
                    resposta = postar(a.enviar, "/eventos/camera", {"zona": nome, "pessoas": pessoas})
                    if resposta.get("novo"):
                        print(f"   -> ocorrência #{resposta['problema_id']} aberta na fila")
                    elif "erro" in resposta:
                        print(f"   -> erro: {resposta}")

        if gravador or a.mostrar:
            tela = pixelar.annotate(quadro.copy(), detections=deteccoes)  # ninguém identificável
            for desenho in desenhos:
                tela = desenho.annotate(tela)
            if gravador:
                gravador.write(tela)
            if a.mostrar:
                cv2.imshow("Ronda Viva - camera (pixelado)", tela)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break

    video.release()
    if gravador:
        gravador.release()
    cv2.destroyAllWindows()
    Path(a.saida).write_text(json.dumps(contagens, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{len(contagens)} contagens salvas em {a.saida} (só números, nenhuma imagem).")


if __name__ == "__main__":
    main()
