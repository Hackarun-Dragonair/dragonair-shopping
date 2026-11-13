# 📹 Câmera da Ronda Viva (proposta)

A câmera **só conta pessoas por zona** e manda **números** para a Ronda Viva.
Nenhuma imagem sai do notebook. No vídeo de saída, as pessoas aparecem pixeladas.

Quando o movimento fica alto em 3 leituras seguidas, o sistema **sugere** a tarefa
"Reforçar limpeza" (P3, equipe Limpeza) na fila. Quem confirma é uma pessoa.

## Arquivos
| Arquivo | O que faz |
|---|---|
| `contador.py` | Roda o YOLO num vídeo/webcam, conta por zona e salva `contagens.json` |
| `replay.py` | Reenvia as contagens salvas para a Ronda Viva (demo sem risco) |
| `simular_sensor.py` | Sensor de fumaça **SIMULADO** → P1 + aviso à brigada |
| `zonas.json` | Zonas desenhadas no vídeo (coordenadas de 0 a 1). Fictícias, **não é a planta** |
| `contagens-exemplo.json` | Números de exemplo para testar o replay sem vídeo |
| `enviar.py` | Faz o POST (só biblioteca padrão) |

## Rodar a demo SEM câmera (2 terminais)
```bash
# Terminal 1 — sistema (limite 3 pessoas só para a demo)
LIMITE_USO=3 python wsgi.py
# Terminal 2 — replay dos números
python camera/replay.py --contagens camera/contagens-exemplo.json --velocidade 5
```
Abra `http://localhost:5000`: a praça mostra "📹 N pessoas agora" e a ocorrência aparece em `/telas/fila`.

## Rodar o YOLO de verdade (uma vez, no notebook)
```bash
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
pip install -r camera/requirements-camera.txt
python camera/contador.py --fonte nosso_video.mp4 --video-saida saida_pixelada.mp4
```
Gera `camera/contagens.json` (só números). Depois é só usar o `replay.py`.

## Regras (LGPD e regulamento)
- Vídeo só **da equipe, com consentimento**. O vídeo cru **não vai para o repo** (o `.gitignore` bloqueia `.mp4`).
- Câmera **nunca dentro de banheiro**. Banheiro continua no QR.
- Sensor é **SIMULADO** e isso aparece escrito na ocorrência.
- Ultralytics é **AGPL-3.0** e supervision é **MIT**. Os dois estão declarados no README e em `docs/IA.md`.
