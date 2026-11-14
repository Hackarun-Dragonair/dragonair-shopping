#!/usr/bin/env bash
# Gera o vídeo final com a voz gravada no celular, num comando só.
#
#   bash docs/pitch/video/montar_com_voz.sh voz.m4a
#
# Aceita qualquer formato que o ffmpeg abra (m4a, mp3, ogg, opus, wav, aac...).
# Faz: limpa o ruído (afftdn), tira graves e chiado, equilibra o volume (loudnorm -16 LUFS),
# encaixa a voz no vídeo (acelera no máximo 6% se passar de 90 s; se for curta, a cena final
# fica mais tempo), acerta as legendas pelas pausas da voz e gera pitch-90s-final.mp4
# com as mesmas imagens e legendas das outras versões.
#
# Precisa das telas, cartelas e fontes já preparadas (bash docs/pitch/video/fazer_video.sh).
# Pasta dos vídeos: $VIDEO_DIR (padrão: ~/Vídeos/ronda-viva-pitch).
set -euo pipefail

if [ $# -lt 1 ] || [ ! -f "$1" ]; then
  echo "Uso: bash docs/pitch/video/montar_com_voz.sh <arquivo-da-voz>"
  echo "Exemplo: bash docs/pitch/video/montar_com_voz.sh ~/Downloads/voz.m4a"
  exit 1
fi

AQUI="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VIDEO_DIR="${VIDEO_DIR:-$HOME/Vídeos/ronda-viva-pitch}"
TRAB="$VIDEO_DIR/trabalho"
VOZ_DIR="$TRAB/voz-humana"
mkdir -p "$VOZ_DIR"

for f in "$TRAB/telas/marcas.json" "$TRAB/cartelas/moldura.png" "$TRAB/voz/tempos.json" "$TRAB/fontes/Montserrat-600.ttf"; do
  if [ ! -f "$f" ]; then
    echo "Falta $f. Rode antes: bash $AQUI/fazer_video.sh"
    exit 1
  fi
done

echo "1/3 Limpando a voz (ruído, graves, chiado)…"
ffmpeg -y -loglevel error -i "$1" -vn -ac 1 -ar 48000 \
  -af "highpass=f=80,lowpass=f=12000,afftdn=nr=12:nf=-30:tn=1,acompressor=threshold=-22dB:ratio=2.5:attack=8:release=120:makeup=2" \
  "$VOZ_DIR/voz-limpa.wav"

echo "2/3 Encaixando a voz no tempo do vídeo…"
python3 "$AQUI/alinhar_voz.py" "$TRAB/voz/tempos.json" "$VOZ_DIR/voz-limpa.wav" "$VOZ_DIR"

echo "3/3 Montando o vídeo (leva uns 3 minutos)…"
python3 "$AQUI/montar.py" "$TRAB" "$VOZ_DIR/tempos-voz.json" "$VOZ_DIR/voz-ajustada.wav" "$VIDEO_DIR/pitch-90s-final.mp4"

DUR=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$VIDEO_DIR/pitch-90s-final.mp4")
TAM=$(du -h "$VIDEO_DIR/pitch-90s-final.mp4" | cut -f1)
echo
echo "Pronto: $VIDEO_DIR/pitch-90s-final.mp4 (${DUR%.*} s, $TAM)"
echo "Assista inteiro com som antes de enviar (o regulamento aceita de 1min15 a 2min)."
