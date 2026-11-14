#!/usr/bin/env bash
# Refaz tudo do zero: grava as telas do app, renderiza as cartelas, gera a voz guia
# e monta as duas versões do vídeo (sem voz e com voz guia sintética).
#
#   bash docs/pitch/video/fazer_video.sh            # tudo
#   bash docs/pitch/video/fazer_video.sh --sem-gravar   # reaproveita a gravação de tela que já existe
#
# Variáveis (com padrão):
#   VIDEO_DIR    pasta dos vídeos (~/Vídeos/ronda-viva-pitch); nada de vídeo vai para o git
#   PY_APP       Python do projeto, com Flask e segno (.venv/bin/python)
#   PY_PLAYWRIGHT Python com Playwright + Chrome (para gravar a tela e renderizar as cartelas)
#   PY_PIPER     Python com piper-tts (voz guia offline)
#   VOZ_PIPER    modelo de voz pt_BR do Piper (.onnx)
set -euo pipefail

AQUI="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RAIZ="$(cd "$AQUI/../../.." && pwd)"
VIDEO_DIR="${VIDEO_DIR:-$HOME/Vídeos/ronda-viva-pitch}"
TRAB="$VIDEO_DIR/trabalho"
PY_APP="${PY_APP:-$RAIZ/.venv/bin/python}"
PY_PLAYWRIGHT="${PY_PLAYWRIGHT:?defina PY_PLAYWRIGHT com o python que tem playwright}"
PY_PIPER="${PY_PIPER:?defina PY_PIPER com o python que tem piper-tts}"
VOZ_PIPER="${VOZ_PIPER:?defina VOZ_PIPER com o caminho do pt_BR-faber-medium.onnx}"
PORTA=8778
mkdir -p "$TRAB/fontes" "$TRAB/voz"

echo "== fontes Montserrat (licença OFL, Google Fonts)"
if [ ! -f "$TRAB/fontes/Montserrat-800.ttf" ]; then
  i=0
  for url in $(curl -s -A "Mozilla/4.0" "https://fonts.googleapis.com/css2?family=Montserrat:wght@500;600;700;800" | grep -o "https://[^)]*"); do
    i=$((i + 1)); peso=$(echo "500 600 700 800" | cut -d" " -f$i)
    curl -sfL -o "$TRAB/fontes/Montserrat-$peso.ttf" "$url"
  done
fi

echo "== QR da etiqueta (zona de demonstração) e da demo online (cartela final)"
"$PY_APP" -c "
import segno
segno.make('https://ronda-viva-0ek7.onrender.com/z/sanitario-piso1', error='m').save('$TRAB/qr-zona.svg', scale=10, border=0, dark='#2c241b', xmldecl=False)
segno.make('https://ronda-viva-0ek7.onrender.com', error='m').save('$TRAB/qr-demo.svg', scale=10, border=0, dark='#2c241b', xmldecl=False)
"

echo "== cartelas"
"$PY_PLAYWRIGHT" "$AQUI/render_cartelas.py" "$TRAB" "$TRAB/qr-zona.svg" "$TRAB/qr-demo.svg"

if [ "${1:-}" != "--sem-gravar" ]; then
  echo "== gravação das telas (app real, banco novo com dados fictícios, porta $PORTA)"
  "$PY_APP" "$AQUI/servidor_gravacao.py" $PORTA "$TRAB/banco" > "$TRAB/servidor.log" 2>&1 &
  SERVIDOR=$!
  trap 'kill $SERVIDOR 2>/dev/null || true' EXIT
  until curl -s -o /dev/null "http://127.0.0.1:$PORTA/entrar"; do sleep 1; done
  "$PY_PLAYWRIGHT" "$AQUI/gravar_telas.py" "$TRAB/telas" "http://127.0.0.1:$PORTA"
  kill $SERVIDOR
fi

echo "== voz guia (Piper, offline)"
"$PY_PIPER" "$AQUI/voz_guia.py" "$VOZ_PIPER" "$TRAB/voz" 0.9
ffmpeg -y -loglevel error -i "$TRAB/voz/voz-guia.wav" -af "highpass=f=70,loudnorm=I=-16:TP=-1.5:LRA=11,aresample=48000" \
  -ar 48000 "$TRAB/voz/voz-guia-tratada.wav"

echo "== montagem"
python3 "$AQUI/montar.py" "$TRAB" "$TRAB/voz/tempos.json" "$TRAB/voz/voz-guia-tratada.wav" "$VIDEO_DIR/pitch-90s-voz-guia.mp4"
python3 "$AQUI/montar.py" "$TRAB" "$TRAB/voz/tempos.json" silencio "$VIDEO_DIR/pitch-90s-sem-voz.mp4"

echo "== quadros para revisão (um por segundo, em 640x360)"
rm -rf "$TRAB/revisao" && mkdir -p "$TRAB/revisao"
ffmpeg -loglevel error -i "$VIDEO_DIR/pitch-90s-voz-guia.mp4" -vf "fps=1,scale=640:360" "$TRAB/revisao/q_%03d.png"
for v in "$VIDEO_DIR"/pitch-90s-*.mp4; do
  echo "$(basename "$v"): $(ffprobe -v error -show_entries format=duration -of csv=p=0 "$v") s, $(du -h "$v" | cut -f1)"
done
