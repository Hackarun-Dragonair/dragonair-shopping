# Vídeo do pitch (90 s): como foi feito e como refazer

Vídeo de 88,6 s para a banca do HackaRun 2026 (regulamento: 1min15 a 2min), seguindo
[`../roteiro-90s.md`](../roteiro-90s.md) e [`../demo-cliques.md`](../demo-cliques.md).
Mostra, nesta ordem e com um rótulo no canto da tela: **1 · O problema**, **2 · A solução**,
**3 · Funcionalidades** (IA + regra de risco, gestor e linha do tempo, mapa, painel, acerto real da IA)
e **4 · Diferencial**, e fecha com o nome do produto, a equipe e "HackaRun 2026".

## Onde estão os arquivos
Os vídeos **não vão para o git** (são grandes). Ficam em `~/Vídeos/ronda-viva-pitch/`:

| Arquivo | O que é |
|---|---|
| `pitch-90s-sem-voz.mp4` | imagens + legendas, trilha de áudio em silêncio |
| `pitch-90s-voz-guia.mp4` | o mesmo, com voz sintética offline (guia de ritmo e plano B) |
| `pitch-90s-final.mp4` | gerado por `montar_com_voz.sh` com a voz gravada pela equipe |
| `trabalho/` | gravações de tela, cartelas, voz guia, cenas e quadros de revisão (pode apagar; o `fazer_video.sh` refaz) |

Formato: 1920x1080, 30 fps, H.264 + AAC 48 kHz, cerca de 23 MB (limite: 50 MB).

## Gravar a voz humana (versão final)
1. Siga [`GRAVAR-VOZ.md`](GRAVAR-VOZ.md) (5 minutos, no celular) lendo [`texto-locucao.md`](texto-locucao.md).
2. Rode **um comando**:
   ```bash
   bash docs/pitch/video/montar_com_voz.sh ~/Downloads/voz.m4a
   ```
   Limpa o ruído (afftdn), corta graves e chiado, equilibra o volume (loudnorm, -16 LUFS),
   encaixa a voz e gera `pitch-90s-final.mp4` com as mesmas imagens e legendas.
   - Fala longa: acelera no máximo 6% (atempo), sem cortar nada. Se ainda passar, o vídeo fica um pouco mais longo (até 2 min é aceito).
   - Fala curta: a cartela final fica mais tempo; o vídeo nunca fica abaixo de 88,6 s.
   - As legendas e as trocas de cena seguem a voz: o script acha as pausas `//` entre as partes
     e, dentro de cada parte, as pausas entre as frases. Testado com três gravações simuladas
     (lenta, normal e curta, com ruído): legenda a menos de 0,1 s do começo de cada frase.

## Como foi feito
Tudo por script, sem editor de vídeo:

| Script | Faz |
|---|---|
| `roteiro_video.py` | **texto único** das 24 falas (legenda, voz guia e `texto-locucao.md`), tempo de início de cada parte e duração do vídeo |
| `servidor_gravacao.py` | liga o app de verdade com banco novo, só dados fictícios do seed, sem planta enviada |
| `gravar_telas.py` | Chrome sem janela (Playwright) faz a demo: celular 390x844 com zoom 2x e computador 1536x864 com zoom 2x. Grava quadro a quadro pelo screencast do Chrome, com o mouse andando devagar e com curva. Guarda marcas de tempo e a posição dos elementos para o zoom |
| `cartelas.html` + `render_cartelas.py` | cartelas na paleta do app (bronze, bege, café, off-white), fonte Montserrat (licença OFL), moldura do celular desenhada em SVG e etiqueta com QR de verdade (segno). Saem em PNG 3840x2160 |
| `voz_guia.py` | voz sintética **Piper** (offline), modelo `pt_BR-faber-medium` do repositório oficial rhasspy/piper-voices, uma fala por vez; calcula o tempo de cada legenda |
| `montar.py` | ffmpeg: cada cena é encaixada no tempo das falas; zoom suave (zoompan) no aviso da brigada, na pergunta "Limpeza ou Elétrica?", em "Prioridade mantida em P1", na linha do tempo, nos números da IA e nas zonas cinza; fusões de 0,4 s; legendas ASS queimadas; reaproveita as imagens se só o áudio mudou |
| `alinhar_voz.py` | encaixa a voz humana: corta silêncio das pontas, acelera até 6% se preciso, acha as pausas e calcula o tempo de cada fala |
| `fazer_video.sh` | refaz tudo do zero (fontes, QR, cartelas, gravação, voz guia, as duas versões e os quadros de revisão) |
| `montar_com_voz.sh` | um comando para a versão com voz humana |

Legendas: Montserrat 52 px com caixa café semitransparente, embaixo e centralizadas; nas cenas do
celular vão para a coluna da direita, para não cobrir a tela do app.

### Refazer tudo
```bash
PY_PLAYWRIGHT=/caminho/do/venv-com-playwright/bin/python \
PY_PIPER=/caminho/do/venv-com-piper/bin/python \
VOZ_PIPER=/caminho/pt_BR-faber-medium.onnx \
bash docs/pitch/video/fazer_video.sh            # --sem-gravar reaproveita a gravação de tela
```
Precisa de: ffmpeg/ffprobe com libx264, libass e zoompan; Chrome + Playwright
(`pip install playwright`); Piper (`pip install piper-tts`) e o modelo de voz:
`https://huggingface.co/rhasspy/piper-voices/resolve/main/pt/pt_BR/faber/medium/pt_BR-faber-medium.onnx` (e o `.onnx.json`).
Leva cerca de 8 minutos num notebook com 8 núcleos.

## Revisão feita (quadros a cada 3 s)
- Texto do app e das cartelas legível em 1080p; o zoom aproxima o que a fala cita.
- Legenda não cobre a ação: nas cenas do celular fica ao lado do aparelho; no computador, embaixo.
- Nada cortado nas bordas das cartelas; rótulo de seção no canto, longe do conteúdo.
- **Nenhum dado pessoal**: crachás e nomes são os fictícios do seed (Otto Lima, "Campo, sem crachá").
- **Nenhuma planta real**: o mapa é o desenho esquemático da equipe; o servidor de gravação usa uma pasta de plantas vazia.
- **Nenhuma marca real além do contexto do desafio**: só o nome "Capim Dourado Shopping", como o próprio app faz; sem logotipo oficial.
- Duração conferida com ffprobe: 88,6 s nas duas versões; volume da voz guia em -16 LUFS.

## Declaração de uso de IA
- **Telas:** gravação **automatizada** do app real funcionando (Playwright dirigindo o Chrome), com banco
  de demonstração fictício. Nada foi montado sobre dados falsos além do seed. A seta do mouse e o círculo
  de toque foram desenhados em CSS **só durante a gravação**, porque o Chrome sem janela não mostra o cursor.
- **Voz guia:** **sintética**, gerada offline pelo Piper (modelo aberto pt_BR-faber-medium). Serve de guia de
  ritmo e de plano B. A versão final usa a voz de uma pessoa da equipe.
- **Roteiro, cartelas, scripts e montagem:** preparados com ajuda do Claude (Anthropic), a partir do roteiro
  escrito pela equipe; a equipe revisa o texto antes de gravar a voz.
- Sem música (nenhum direito autoral envolvido). Fonte Montserrat sob licença SIL OFL.
