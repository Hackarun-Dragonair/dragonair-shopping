# Vídeo do pitch (90 s): como foi feito e como refazer

Vídeo de **89,6 s** para a banca do HackaRun 2026 (regulamento: 1min15 a 2min), a partir de
[`../roteiro-90s.md`](../roteiro-90s.md) e [`../demo-cliques.md`](../demo-cliques.md), **versão 2**
(refeita depois da banca simulada 1). Mostra, com um rótulo grande no canto da tela:
**1 · O problema**, **2 · A solução no dia a dia**, **3 · Funcionalidades** (IA com senso crítico,
supervisor e linha do tempo, mapa, painel, o que medimos da IA), **4 · Diferencial** e **5 · Próximo passo**.

## O que mudou na versão 2 (notas da banca simulada 1)
| Antes | Agora |
|---|---|
| 7 s de cartela parada na abertura | o **mapa real** com zonas cinza se aproximando, e a pergunta entra por cima |
| problema sem consequência | "Se alguém escorrega ali, ninguém sabe quando foi conferido." |
| celular quase parado (19–28 s) | QR do Sanitário piso 1 → tela da zona → toque em **Tudo OK** → zona **verde** no mapa do celular; zoom de 1,7x |
| fala dizia "a IA sugere" enquanto a tela mostrava a IA em dúvida | a fala conta o que a tela mostra: **24%**, ela **perguntou**, ele escolheu Elétrica; "roda sem internet" saiu |
| "linha do tempo que não se apaga" | "a IA sugeriu Limpeza, o supervisor confirmou Elétrica, com hora e nome" + zoom em "Registro permanente" |
| cartões gigantes de 100% e "o acerto é real" | corte seco direto no zoom da **tabela de comparação** (os cartões de 100% não aparecem): palavras-chave 4 de 6 riscos, com a IA 6 de 6; em frases reais, **81%** |
| "prova que o shopping cuidou" e slogan 3 vezes | "Checklist cobra a tarefa. A Ronda Viva mostra o lugar…"; slogan só nas cartelas |
| final parado com 4 s mudos | **próximo passo** (piloto de 30 dias) + faixa "78 testes automáticos · teste cego n = 20 · demo online" + QR da demo; 1,5 s de folga |
| frases a 3–4,6 palavras/s, silêncios de até 4 s | cerca de **2,8 palavras/s** dentro das frases; pausas de 0,6–0,9 s entre as partes; 1,5 s no fim |
| rótulos pequenos | rótulos 50% maiores e zoom maior em todas as telas (legível em 640x360) |

Ajustes depois da banca simulada 2 (nota 8,1): abertura enquadra só o desenho do mapa (a coluna com
"100% Acerto da IA" fica fora), corte seco do painel direto para o zoom da tabela da IA, linha do tempo
enquadrada com o começo das linhas, cartela final com "78 testes automáticos" (número do main),
e guias de locução pedindo "sem pressa, pausas curtas" (cerca de 2,8 palavras/s).

Números falados, conferidos em `docs/evidencias/modelo/resumo.md`: teste cego n = 20, recall de P1
"só regras de palavras" 67% (4 de 6) e "modelo + regra dura" 100% (6 de 6); frases reais do campo
(rótulos ainda a revisar): categoria 81%. Os 24% são a confiança que a tela mostra na demo.

## Onde estão os arquivos
Os vídeos **não vão para o git** (são grandes). Ficam em `~/Vídeos/ronda-viva-pitch/`:

| Arquivo | O que é |
|---|---|
| `pitch-90s-sem-voz.mp4` | imagens + legendas, trilha de áudio em silêncio |
| `pitch-90s-voz-guia.mp4` | o mesmo, com voz sintética offline (guia de ritmo e plano B) |
| `pitch-90s-final.mp4` | gerado por `montar_com_voz.sh` com a voz gravada pela equipe |
| `trabalho/` | gravações de tela, cartelas, voz guia, cenas e quadros de revisão (pode apagar; o `fazer_video.sh` refaz) |

Formato: 1920x1080, 30 fps, H.264 + AAC 48 kHz, cerca de 25 MB (limite: 50 MB).

## Gravar a voz humana (versão final)
1. Siga [`GRAVAR-VOZ.md`](GRAVAR-VOZ.md) (5 minutos, no celular) lendo [`texto-locucao.md`](texto-locucao.md).
2. Rode **um comando**:
   ```bash
   bash docs/pitch/video/montar_com_voz.sh ~/Downloads/voz.m4a
   ```
   Limpa o ruído (afftdn), corta graves e chiado, equilibra o volume (loudnorm, -16 LUFS),
   encaixa a voz e gera `pitch-90s-final.mp4` com as mesmas imagens e legendas.
   - Fala longa: acelera no máximo 6% (atempo), sem cortar nada. Se ainda passar, o vídeo fica um pouco mais longo (até 2 min é aceito).
   - Fala curta: as cenas acompanham a fala e a cartela final segura até no mínimo 80 s (regulamento: 75 s).
   - As legendas e as trocas de cena seguem a voz: o script acha as pausas `//` entre as partes
     e, dentro de cada parte, as pausas entre as frases (a duração esperada de cada frase vem do
     tamanho do texto falado, então a pausa de uma vírgula não é confundida com o fim da frase).
     Testado com o texto da v2 e três gravações simuladas com ruído: fala de 91 s e de 102 s →
     legenda a menos de 0,1 s do começo de cada frase; fala exagerada de 115 s → uma frase 1,6 s fora.

## Como foi feito
Tudo por script, sem editor de vídeo:

| Script | Faz |
|---|---|
| `roteiro_video.py` | **texto único** das 25 falas, cada uma com um id (legenda, voz guia, montagem e `texto-locucao.md`), pausas e ritmo máximo |
| `servidor_gravacao.py` | liga o app de verdade com banco novo, só dados fictícios do seed, sem planta enviada |
| `gravar_telas.py` | Chrome sem janela (Playwright) faz a demo: mapa da abertura, celular 390x844 com zoom 2x (Tudo OK e Problema) e computador 1536x864 com zoom 2x. Grava quadro a quadro pelo screencast do Chrome, com o mouse andando devagar e com curva. Guarda marcas de tempo e a posição dos elementos para o zoom |
| `cartelas.html` + `render_cartelas.py` | cartelas na paleta do app (bronze, bege, café, off-white), fonte Montserrat (licença OFL), moldura do celular desenhada em SVG, camadas transparentes da abertura, etiqueta e QR da demo de verdade (segno). Saem em PNG 3840x2160 |
| `voz_guia.py` | voz sintética **Piper** (offline), modelo `pt_BR-faber-medium` do repositório oficial rhasspy/piper-voices, uma fala por vez; se uma frase sai rápida demais (mais de 2,6 palavras/s), sintetiza de novo mais devagar; calcula o tempo de cada legenda |
| `montar.py` | ffmpeg: cada cena e cada trecho de tela ficam presos a uma fala (ex.: o toque em Elétrica cai em "Ele escolheu Elétrica"); zoom suave (zoompan) no aviso da brigada, na pergunta "Limpeza ou Elétrica?", em "Prioridade mantida em P1", na linha do tempo, nos números da IA e nas zonas cinza; fusões de 0,35 s; legendas ASS queimadas; reaproveita as imagens se só o áudio mudou |
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

## Revisão feita (um quadro por segundo, olhado em 640x360)
- Texto do app e das cartelas legível em 1080p; o zoom aproxima o que a fala cita.
- Legenda não cobre a ação: nas cenas do celular fica ao lado do aparelho; no computador, embaixo.
- Nada cortado nas bordas das cartelas; rótulo de seção no canto, longe do conteúdo.
- **Nenhum dado pessoal**: crachás e nomes são os fictícios do seed (Otto Lima, "Campo, sem crachá").
- **Nenhuma planta real**: o mapa é o desenho esquemático da equipe; o servidor de gravação usa uma pasta de plantas vazia.
- **Nenhuma marca real além do contexto do desafio**: só o nome "Capim Dourado Shopping", como o próprio app faz; sem logotipo oficial.
- Sincronia: digitação durante "escreveu", pergunta da IA durante "perguntou", toque em Elétrica em "Ele escolheu Elétrica",
  "Prioridade mantida em P1" em "mantém P1", parágrafo das frases reais em "81%".
- Duração conferida com ffprobe: 89,6 s nas duas versões; volume da voz guia em -16 LUFS.

## Declaração de uso de IA
- **Telas:** gravação **automatizada** do app real funcionando (Playwright dirigindo o Chrome), com banco
  de demonstração fictício. Nada foi montado sobre dados falsos além do seed. A seta do mouse e o círculo
  de toque foram desenhados em CSS **só durante a gravação**, porque o Chrome sem janela não mostra o cursor.
- **Voz guia:** **sintética**, gerada offline pelo Piper (modelo aberto pt_BR-faber-medium). Serve de guia de
  ritmo e de plano B. A versão final usa a voz de uma pessoa da equipe.
- **Roteiro, cartelas, scripts e montagem:** preparados com ajuda do Claude (Anthropic), a partir do roteiro
  escrito pela equipe; a equipe revisa o texto antes de gravar a voz.
- Sem música (nenhum direito autoral envolvido). Fonte Montserrat sob licença SIL OFL.
