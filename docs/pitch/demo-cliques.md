# Demo: ordem exata de cliques

Serve para o vídeo e para a apresentação ao vivo. Fala que acompanha: [`roteiro-90s.md`](roteiro-90s.md).
Resultado conferido em 13/11 à noite com o banco de exemplo (servidor local de teste).

## Antes de começar (5 min)
- [ ] **Escolha onde roda:** site do Render (https://ronda-viva-0ek7.onrender.com) ou notebook (plano B, abaixo). Para o gato da sexta-feira 13, **só no notebook**.
- [ ] **Render:** abra o site 2 minutos antes. O plano grátis dorme depois de 15 min e o 1º acesso leva cerca de 1 min.
- [ ] **Dados limpos:** o banco volta ao exemplo a cada reinício. No notebook, desligue (`Ctrl+C`) e ligue de novo antes de gravar.
- [ ] **Dois aparelhos:** celular (funcionário, **sem entrar**) e computador (gestor OTTO). Se for usar um navegador só, use uma janela anônima para o gestor, porque o crachá fica guardado no navegador.
- [ ] Etiqueta QR impressa da **Área técnica L2** (ou o endereço `/z/area-tecnica-l2` salvo no celular).
- [ ] Nada da planta do shopping aberto no computador. Não envie imagem no editor de mapa durante a gravação.

## Parte 1 — Celular (funcionário, sem crachá)

| # | Faça | O que deve aparecer |
|---|---|---|
| 1 | Aponte a câmera para o **QR da Área técnica L2** e abra o link (ou digite `/z/area-tecnica-l2`) | Tela da zona: nome, piso L2, "Registrando como: Campo (sem crachá)", botões **Tudo OK**, **Atenção**, **Problema** |
| 2 | Toque **Problema** | Abre "O que você viu?" com botões prontos ("Vazamento", "Quadro aberto", "Cheiro de queimado") |
| 3 | Escreva **cheiro de fumaça no quadro**. Em "Perto de", escolha **quadro** | — |
| 4 | Toque **Ver sugestão da IA** | Caixa vermelha: **"Avise a brigada pelo rádio. O sistema não aciona ninguém e não rebaixa este risco."** · Prioridade **P1** · pergunta **"A IA ficou em dúvida. É mais Limpeza ou Elétrica?"** |
| 5 | A IA ficou em dúvida e chutou **Limpeza** (errado). Toque **Elétrica** na pergunta | Categoria vira **Elétrica** e Equipe vira **Manutenção**. É o momento de mostrar que **a IA admite a dúvida e a pessoa decide** |
| 6 | Toque **Registrar problema** | Caixa vermelha da brigada de novo + "Ocorrência #N registrada e enviada para Manutenção. Ver linha do tempo" |

## Parte 2 — Computador (gestor OTTO)

| # | Faça | O que deve aparecer |
|---|---|---|
| 7 | Clique **Entrar com crachá** → perfil **Gestor** → crachá **OTTO** → Entrar | Abre o **Painel de gestão** |
| 8 | Menu **Fila de ocorrências** | A ocorrência nova (P1) na coluna **Aberto** |
| 9 | Abra a ocorrência. Em **Prioridade**, escolha **P3**. Clique **Confirmar** | Aviso: **"Prioridade mantida em P1. Palavra de risco não pode ser rebaixada."** A prioridade continua P1 |
| 10 | Mostre a **Linha do tempo** (à direita) | Registro pelo QR → "IA sugeriu…" → "Palavra de risco. Prioridade P1…" → "Otto Lima (Supervisor) confirmou Elétrica · P1 · Manutenção" |
| 11 | Volte à **Fila**. Use o filtro de prioridade **P1** | Só a ocorrência de risco |
| 12 | Menu **Mapa das zonas** | Área técnica L2 em vermelho (Problema). Contador **"Ninguém conferiu"** e as zonas **cinza** |
| 13 | Menu **Painel de gestão** | Zonas no prazo (%), Sem conferência, Tempo médio, Acerto da IA; tabela "Situação das zonas"; "nunca por pessoa" |
| 14 | Menu **Inteligência artificial** | 100% categoria · 95% prioridade · 100% dos P1 (6 de 6) · 90% da regra simples; tabela "Regras x modelo x modelo + regra dura"; matriz |

A fila se atualiza sozinha a cada 5 s, então a ocorrência do celular aparece sem recarregar.

## Parte 3 — Gato da sexta-feira 13 (só no notebook)
No sábado o gato só aparece ligando o servidor com a variável `SEXTA13=1`. No Render ele **não** aparece (seria preciso criar a variável no painel do serviço).

| # | Faça | O que deve aparecer |
|---|---|---|
| 15 | No notebook: `SEXTA13=1 python wsgi.py` (Windows: `$env:SEXTA13="1"; python wsgi.py`) | — |
| 16 | Abra o **Mapa** | Frase da sexta-feira 13 no topo e o gato preto em **uma** zona cinza (a mais esquecida) |
| 17 | No celular, abra essa zona e toque **Tudo OK** | "Gato preto espantado! Esta zona não está mais esquecida." No mapa, o gato pula para a próxima zona esquecida |

## Plano B — internet ou Render falhou
A IA e o visual estão dentro do projeto: **não precisa de internet**, só de uma rede entre notebook e celular.
1. Ligue o **hotspot do celular** e conecte o notebook nele (Wi-Fi de evento costuma bloquear aparelhos entre si).
2. No notebook, na pasta do projeto: ative o venv e rode `python wsgi.py` (passo a passo no README, "Como executar").
3. Descubra o IP: Linux `hostname -I` · macOS `ipconfig getifaddr en0` · Windows `ipconfig`.
4. No celular, abra `http://IP-DO-NOTEBOOK:8000/z/area-tecnica-l2`.
5. Sem celular funcionando: faça tudo no notebook, abrindo `http://127.0.0.1:8000/z/area-tecnica-l2` numa janela estreita (a tela é a mesma).
6. Último recurso: mostrar os prints de `docs/evidencias/qa/` (são do app de verdade, 13/11).

Deixe o projeto **instalado e testado no notebook antes de sábado 8h** (`python -m pytest -q` → 78 passed).

## Dicas de gravação
- **Resolução:** grave o computador em 1920×1080 (ou 1366×768) com zoom do navegador em 110–125%, para a banca ler. Esconda a barra de favoritos e feche abas com nomes pessoais.
- **Celular:** gravador de tela do próprio celular. Modo "não perturbe" ligado (sem notificações na tela).
- **Espera do Render:** acorde o site antes de gravar. Se mesmo assim aparecer tela de carregamento, **corte esse trecho** na edição.
- **Voz separada da tela:** grave cada linha da tabela do roteiro como um áudio separado, em sala fechada, celular a um palmo da boca. Assim dá para regravar só o trecho que errou.
- **Montagem:** CapCut ou Canva. Legenda automática (a banca pode assistir sem som). Música bem baixa, da biblioteca do próprio editor.
- **Conferir antes de enviar:**
  - [ ] duração entre 1min15 e 2min (meta 90 s);
  - [ ] áudio audível e legenda certa;
  - [ ] nada da planta do shopping, nenhum logo do shopping;
  - [ ] nenhum nome ou rosto de pessoa real (crachás OTTO, LIA, RITA e CAIO são fictícios);
  - [ ] tudo o que aparece é o app funcionando de verdade.
- **Exportar** em 1080p, MP4.
