# Passagem de bastão para outra sessão de IA (Claude)

> Para continuar o trabalho com outra conta/sessão. Leia junto com `AGENTS.md`, `docs/CHECKLIST-ENTREGA.md` e `docs/IA.md`.
> Atualizado: sexta 13/11, ~21h.

## Estado agora
- **No ar:** https://ronda-viva-0ek7.onrender.com (Render grátis; cada merge no `main` publica sozinho; dorme após 15 min).
- **main:** backend do Paulo (PR #30) + front novo (PR #31: mapa SVG fictício, fila em 3 colunas, painel) + Easter Egg sexta-13 + 80 frases do Pedro.
- **Branch `login-perfis` (PR aberto, NÃO juntado):** login por crachá fictício.
  - Gestor (ADM) = papel supervisor/coordenação → painel, etiquetas PDF, confirmar sugestão da IA.
  - Funcionário = encarregado/manutenção → ronda, assumir, resolver.
  - QR (`/z/<codigo>`) funciona sem entrar, registrado como "Campo (aparelho compartilhado)".
  - Crachás demo: OTTO e LIA (gestor), RITA e CAIO (funcionário). Arquivos: `app/perfis.py`, `app/rotas/acesso_web.py`, `app/templates/entrar.html`, `tests/test_perfis.py`. 55 testes passando.
  - `SECRET_KEY` do Render agora é gerada (`generateValue`).

## Pendências (ordem de prioridade, do PO)
1. Revisar e juntar `login-perfis`.
2. **Teste cego limpo:** as 16 frases do Pedro no fim de `data/teste_cego.csv` têm rótulos feitos pela IA. Tirar de lá e mover para `data/teste_campo.csv` ("rótulos a revisar"). Deixar só as frases originais da equipe no teste cego.
3. `avaliar.py` → `docs/evidencias/modelo/` (CSV por frase, acurácia, **recall de P1**, matriz de confusão, regras × modelo × modelo+regra) e mostrar isso em "Sobre a IA".
4. Mapa e fila atualizando a cada **5 s** (`app/static/js/mapa.js` usa 15 s).
5. `zona.js`: sem rede, mostrar "Não enviado: sem conexão".
6. Teste de usabilidade real com 3 pessoas → `docs/missao-2/teste-usabilidade.md`.
7. Selo "IA local · X ms" e top-2 na sugestão.
8. Passagem de turno por template (cortar se atrasar).

**Cortar:** modo pico, CSV por contrato, "Minha ronda", LLM, câmera/sensores (decisão da equipe).

## Regras que não mudam
- Planta do shopping é dado sensível: nunca no repo, demo ou vídeo. O mapa é desenho fictício.
- Só dados fictícios. Nada de chave ou dado pessoal.
- Declarar todo uso de IA em `docs/IA.md`.
- A IA só sugere; a regra P1 (fumaça/fogo/choque/pessoa presa) nunca é rebaixada.
- Respostas curtas e explicações simples para a equipe.

## Prazos
- **Missão 2:** sábado **9h45**.
- **Entrega final:** sábado **12h**.
- **Vídeo:** antes das 12h.
