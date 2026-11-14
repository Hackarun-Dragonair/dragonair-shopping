# Passagem de bastão para outra sessão de IA (Claude)

> Para continuar o trabalho com outra conta/sessão. Leia junto com `AGENTS.md`, `docs/CHECKLIST-ENTREGA.md` e `docs/IA.md`.
> Atualizado: sexta 13/11, 23h20. Regra da noite: commit + push a cada passo pequeno; este arquivo é atualizado depois de cada passo.

## Estado agora (sexta 13/11, 23h40)
- **No ar:** https://ronda-viva-0ek7.onrender.com (Render grátis; cada push no `main` publica sozinho; dorme após 15 min).
- **`main` = `origin/main`:** QA + visual bronze/bege (ramo `qa-fixes`, aprovado pelo revisor e publicado; conferido no Render às 22h54). Tag de segurança: `v-missao2-estavel` (c153cdd). Se algo quebrar: `git revert` ou voltar para a tag.
- **Ramo `noite/integracao` (no GitHub, 17 commits sobre o main, 73 testes passando) — REVISOR: código, testes, navegador e QR aprovados sem 🔴; falta só o veredito da documentação (o revisor parou por limite de tokens às 23h30 e foi retomado). Achados de docs já corrigidos em f38eb68. Veredito parcial: `/tmp/claude-1000/-home-arthur-dragonair-shopping/3215d6be-1483-4889-9083-26ba89cb4b6c/scratchpad/revisor-integracao/veredito.md`:**
  - `fix:` faixa de abas sem fresta; quadro "Indicadores/Ocorrências ativas" do mapa atualiza a cada 5 s; tela da zona ignora nova sugestão durante envio (achados do 1º revisor).
  - `feat:` pergunta de desempate "É mais X ou Y?" quando a IA fica em dúvida (frase da demo "cheiro de fumaça no quadro" → Limpeza ou Elétrica, continua P1).
  - `fix:` fila atualiza a cada 5 s mantendo a rolagem.
  - `test:` + `docs:` QR de verdade: 11/11 etiquetas do Render lidas por imagem → zona certa → HTTP 200 sem login (`docs/evidencias/qr/`). `fix:` QR sem filete branco (lê melhor impresso).
  - `docs:` README testado do zero, `docs/RESUMO.md`, `docs/ENTREGA.md` (textos prontos), `docs/pitch/` (roteiro 90 s, cliques da demo, FAQ, cola, checklist de sábado), IA.md e índice de evidências.
- Ramos de origem (já incorporados na integração, podem ser apagados depois): `noite/ajustes-revisor`, `noite/desempate-fila`, `noite/qr-real`, `noite/docs-pitch`, `qa-fixes`.

## Próximo passo exato
1. Revisor revisa `git diff main..noite/integracao` (testes + navegador 1366/390 px + regras).
2. Se aprovado: `git checkout main && git merge --ff-only noite/integracao`, rodar `.venv/bin/python -m pytest -q` (73 passed), `git push origin main`, esperar o Render (procurar "pergunta-desempate" no HTML de `/z/area-tecnica-l2`) e conferir /saude, /, /z/sanitario-piso1.
3. Criar a tag `v-missao2-final` no commit publicado e dar push (é a versão citada na entrega da Missão 2; atualizar `docs/ENTREGA.md` se o nome mudar).
4. Às 6h: escrever `docs/RELATORIO-NOITE.md` (feito / falhou / sobrou) e push.

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
