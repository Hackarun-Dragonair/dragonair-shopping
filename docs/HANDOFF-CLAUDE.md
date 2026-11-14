# Passagem de bastão para outra sessão de IA (Claude)

> Para continuar o trabalho com outra conta/sessão. Leia junto com `AGENTS.md`, `docs/CHECKLIST-ENTREGA.md` e `docs/IA.md`.
> Atualizado: sexta 13/11, 23h45. Regra da noite: commit + push a cada passo pequeno; este arquivo é atualizado depois de cada passo.

## Estado agora (sábado 14/11, 0h40) — TUDO DA NOITE ESTÁ NO MAIN E NO AR
- **No ar:** https://ronda-viva-0ek7.onrender.com — conferido às 23h40 no navegador (celular: pergunta de desempate na frase da demo; PC: OTTO cai no painel, mapa com abas e quadro lateral; nenhum erro de JS).
- **`main` = `origin/main`, 77 testes passando.** Tags: `v-missao2-entrega` (versão da entrega da Missão 2, com o mapa novo), `v-missao2-final` (antes do mapa novo) e `v-missao2-estavel` (ponto de segurança anterior, c153cdd).
- Entrou na noite (2 revisões independentes aprovadas, sem 🔴): QA + 7 bugs corrigidos, visual bronze/bege com abas, pergunta de desempate, fila e quadro do mapa a cada 5 s, QR de verdade (11/11 etiquetas do Render abrem a zona certa) + desenho do QR corrigido, README testado do zero, `docs/RESUMO.md`, `docs/ENTREGA.md`, `docs/pitch/` (roteiro 90 s, cliques, FAQ, cola, checklist), IA.md e índice de evidências.
- Ramos `noite/*` e `qa-fixes` já estão no main; podem ser apagados depois da entrega.

## Próximo passo exato
- **EM ANDAMENTO — VÍDEO DE 90 s, ciclo da noite até 6h. Situação (01h50): versão 1 pronta (88,6 s; ramo `noite/video-pitch`, commit 301f8a4); banca rodada 1 avaliando (2 avaliadores: pitch/comunicação e técnica/negócio; notas em `/tmp/claude-1000/-home-arthur-dragonair-shopping/3215d6be-1483-4889-9083-26ba89cb4b6c/scratchpad/banca/`). Próximo: mandar as notas ao produtor para a versão 2.** decisão do Arthur: **voz humana de manhã** (opção A). À noite: produtor faz o vídeo (ramo `noite/video-pitch`; scripts em `docs/pitch/video/`; vídeos em `/home/arthur/Vídeos/ronda-viva-pitch/`, fora do git) → banca simulada rigorosa avalia (pesos oficiais; extrai quadros, lê legenda/locução, mede duração; nota 0–10 por critério; arquivo `docs/pitch/video/avaliacoes/rodada-N.md`) → produtor refaz → repete até a nota parar de subir ou 6h. Entregáveis: `pitch-90s-sem-voz.mp4`, `pitch-90s-voz-guia.mp4` (voz Piper, plano B), `montar_com_voz.sh voz.m4a`, `GRAVAR-VOZ.md`, `texto-locucao.md`. Ao terminar: juntar os docs no main (revisados), atualizar RELATORIO-NOITE.md.
- **Concluído 0h35:** mapa com formas de shopping (polígonos, do zero) aprovado pelo revisor, no main e no Render. Tag da entrega: `v-missao2-entrega`.
- Nada de código pendente. Escopo congelado.
- Às 6h: escrever `docs/RELATORIO-NOITE.md` (feito / falhou / sobrou) e push.
- Sábado: seguir `docs/pitch/checklist-sabado.md` e `docs/ENTREGA.md`.

## O que só humanos fazem no sábado
Teste de usabilidade com 3 pessoas (`docs/missao-2/teste-usabilidade.md`), gravar o vídeo de 90 s (`docs/pitch/roteiro-90s.md`), enviar Missão 2 até 9h45 e entrega final até 12h (`docs/ENTREGA.md`), colar orientações da Missão 3 às 10h em `docs/desafio.md`, preencher nomes de quem fala no roteiro.

## Como refazer o QA
Servidor de teste com banco separado (não mexe em `instance/`):
`create_app({"DATABASE": "<pasta temporária>/ronda.sqlite3", "PLANTAS_DIR": "<pasta temporária>/plantas", "TEMPLATES_AUTO_RELOAD": True})`.
Navegador: Playwright num ambiente separado (não entra no `requirements.txt`), usando o Chrome instalado (`channel="chrome"`).

## Regras que não mudam
- Planta do shopping é dado sensível: nunca no repo, demo ou vídeo. O mapa é desenho fictício.
- Só dados fictícios. Nada de chave ou dado pessoal.
- Declarar todo uso de IA em `docs/IA.md`.
- A IA só sugere; a regra P1 (fumaça/fogo/choque/pessoa presa) nunca é rebaixada.
- Pedir OK do Arthur antes de juntar no `main`. Rodar os testes antes de cada commit.
- Respostas curtas e explicações simples para a equipe.

## Prazos
- **Missão 2:** sábado **9h45**.
- **Entrega final:** sábado **12h**.
- **Vídeo:** antes das 12h.
