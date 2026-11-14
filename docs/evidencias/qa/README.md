# QA ponta a ponta — sexta 13/11, 22h

**Como foi feito:** navegador Chrome automático (Playwright), servidor local com banco limpo.
Dois perfis da demo: **RITA** (Funcionária) e **OTTO** (Gestor). Duas larguras: computador (1366 px) e celular (390 px, toque).

**Roteiro:** QR da zona → Problema → sugestão da IA → registrar → fila → RITA assume → OTTO confirma (tentando baixar um P1 para P3) → RITA resolve → painel → Editar mapa com uma imagem de teste (gradiente colorido, **não** é a planta) → sem internet → QR com código errado.

**O que funcionou de primeira:** regra P1 ("fumaça" → P1 + "Avise a brigada"), o gestor não consegue rebaixar o P1, linha do tempo completa, funcionária barrada no painel e no editor, aviso "Não enviado: sem conexão" na tela da zona, nada vaza para o lado no celular.

## Bugs achados e corrigidos

| # | Gravidade | O que acontecia | Commit |
|---|---|---|---|
| 1 | 🟡 | Depois de registrar uma ocorrência, não dava para registrar outra: o botão ficava travado em "Enviando…" | `fix: tela da zona deixa registrar outra ocorrência sem recarregar` |
| 2 | 🟡 | QR com código errado mostrava o texto `{"erro":"nao_encontrado"}` | `fix: QR ou endereço errado mostra página com caminho de volta` |
| 3 | 🟡 | Planta enviada sem clicar em "Salvar" voltava torta; sem internet o envio ficava parado em "Enviando…" | `fix: editor de mapa salva o formato da planta ao enviar e avisa sem conexão` |
| 4 | 🟡 | Com planta enviada, zona ainda não pintada sumia do mapa (uma zona cinza podia passar despercebida) | `fix: zona sem bloquinho na planta continua aparecendo no mapa` |
| 5 | 🟡 | No celular não existia botão Sair: no aparelho compartilhado, o próximo registraria com o nome do anterior | `fix: celular ganha botão Sair na tela de perfil` |
| 6 | 🟡 | Tabela do painel cortava a coluna Estado no celular | `fix: tabela do painel cabe no celular` + `fix: estado da zona não fica cortado…` |
| 7 | ⚪ | No celular, o desenho do editor ficava escondido embaixo dos controles | `fix: no celular o editor mostra o desenho antes dos controles` |

Depois de cada correção: `python -m pytest -q` passando (de 64 para 67 testes) e o roteiro rodado de novo no navegador.

## Prints (versão final, já com o visual bronze/bege)

| Arquivo | O que mostra |
|---|---|
| m2_13-2220_pc-zona-sugestao-ia-p1.png | "Fumaça" vira P1 com aviso da brigada |
| m2_13-2220_pc-linha-do-tempo-resolvido.png | Linha do tempo: registro → IA → risco → assumiu → gestor confirmou (P1 mantido) → resolvido |
| m2_13-2220_pc-painel.png | Painel do gestor |
| m2_13-2220_pc-mapa-com-painel-lateral.png | Mapa com indicadores e ocorrências ao lado |
| m2_13-2220_pc-mapa-planta-teste-e-zona-sem-lugar.png | Planta de teste + zona "ainda sem lugar na planta" (bug 4 corrigido) |
| m2_13-2220_pc-editor-mapa.png | Editor do mapa depois de recarregar (formato mantido) |
| m2_13-2220_cel-zona-sugestao-ia.png | Tela do QR no celular |
| m2_13-2220_cel-segundo-registro-liberado.png | Segundo registro liberado (bug 1 corrigido) |
| m2_13-2220_cel-fila.png | Fila no celular |
| m2_13-2220_cel-painel.png | Painel no celular, coluna Estado inteira (bug 6 corrigido) |
