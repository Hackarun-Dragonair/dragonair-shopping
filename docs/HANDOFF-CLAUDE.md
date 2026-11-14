# Passagem de bastão para outra sessão de IA (Claude)

> Para continuar o trabalho com outra conta/sessão. Leia junto com `AGENTS.md`, `docs/CHECKLIST-ENTREGA.md` e `docs/IA.md`.
> Atualizado: sexta 13/11, ~22h30.

## Estado agora
- **No ar:** https://ronda-viva-0ek7.onrender.com (Render grátis; cada merge no `main` publica sozinho; dorme após 15 min).
- **Já no `main` (= `origin/main`, commit `90f295a`), 64 testes passando:**
  - Backend do Paulo (PR #30), front novo (PR #31), Easter Egg sexta-13, 80 frases do Pedro.
  - **Login por crachá** (antigo ramo `login-perfis`): Gestor (ADM) = supervisor/coordenação → painel, editar mapa, etiquetas PDF, confirmar IA. Funcionário = encarregado/manutenção → ronda, assumir, resolver. QR (`/z/<codigo>`) funciona sem entrar ("Campo"). Crachás demo: OTTO e LIA (gestor), RITA e CAIO (funcionário).
  - **Editor de mapa** (`/telas/mapa/editar`): o gestor envia uma imagem de fundo por piso e pinta bloquinhos por zona. A imagem fica só em `instance/` (fora do Git).
  - **Teste cego limpo** (20 frases da equipe) + `data/teste_campo.csv` (16 do Pedro, rótulos a revisar) + `app/avaliar.py` → `docs/evidencias/modelo/` (acurácia, recall de P1, matriz, regras × modelo × modelo+regra), também na tela "Sobre a IA".
  - Design profissional (ramo `design-pro`), mapa atualizando a cada 5 s, "Não enviado: sem conexão" na tela da zona.
- **Ramo `qa-fixes` (pronto, NÃO juntado; esperando o OK do Arthur), 67 testes passando:**
  - 8 commits `fix:` do QA ponta a ponta (PC 1366 px + celular 390 px). Lista e prints em `docs/evidencias/qa/`.
  - 1 commit `style:` com o visual bronze/bege a partir de uma referência em HTML do Arthur: cabeçalho branco + faixa dourada de abas, barra branca embaixo no celular, mapa com cartão "Pavimento" e painel lateral (indicadores + ocorrências ativas) em telas ≥ 1200 px.
  - **Da referência NÃO entrou:** desenho/coordenadas e nomes de lojas reais (planta é dado sensível) e fonte/ícones/CSS de CDN (a demo precisa rodar sem internet).
  - Registro em `docs/IA.md` e `docs/evidencias/README.md` (vão no mesmo ramo).

## Pendências (ordem de prioridade)
1. **Arthur dar OK → juntar `qa-fixes` no `main` e enviar** (rodar `.venv/bin/python -m pytest -q` antes; esperado 67 passed). Depois conferir o site no Render.
2. **Teste de usabilidade real com 3 pessoas de fora** → preencher `docs/missao-2/teste-usabilidade.md` (o roteiro está pronto; o QA automático **não** substitui, regra 6.5).
3. **Prints** que faltam no checklist: gato 🐈‍⬛ no mapa (só vale no dia 13!) e telas no celular de verdade → `docs/evidencias/`.
4. **README** "Como executar" testado por quem não escreveu o código; `docs/IA.md` final.
5. Fila recarrega a cada 15 s (o mapa já usa 5 s). Baixar para 5 s se der tempo.
6. Selo "IA local · X ms" e top-2 na sugestão (cortar se atrasar).
7. Passagem de turno por template (cortar).

**Cortar:** modo pico, CSV por contrato, "Minha ronda", LLM, câmera/sensores, modo escuro e filtros de status no mapa (vistos na referência HTML; não entram depois do congelamento das 22h).

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
