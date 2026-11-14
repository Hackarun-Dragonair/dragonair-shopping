# Relatório da noite — sexta 13/11 para sábado 14/11

> Trabalho feito por agentes de IA (Claude Code) com autorização do Arthur, seguindo as regras dele: escopo congelado, revisor aprova antes do `main`, testes antes de cada commit, conferir o Render depois de cada envio. Declarado em `docs/IA.md`.
> Itens combinados terminaram às 23h50 de sexta. Pedido extra do Arthur (0h): mapa com formas de shopping — entregue às 0h35.

## Resultado em uma linha
Tudo combinado está no `main`, publicado no site e marcado com a tag **`v-missao2-entrega`**. São **78 testes** passando. Cada lote passou por um revisor independente antes do `main`.

## O que foi feito
| # | Item | Situação | Onde ver |
|---|---|---|---|
| 1 | QA + visual novo no `main` | ✅ no ar | `docs/evidencias/qa/` |
| 2 | QR de verdade | ✅ as 11 etiquetas do site no ar foram lidas por imagem; cada uma abre a zona certa sem login. O desenho do QR foi corrigido para ler melhor depois de impresso | `docs/evidencias/qr/` |
| 3 | Pergunta de desempate da IA | ✅ na frase da demo ("cheiro de fumaça no quadro") a tela pergunta "É mais Limpeza ou Elétrica?" e continua P1 com o aviso da brigada | tela da zona |
| 4 | Fila a cada 5 s | ✅ mantém a rolagem e não recarrega com o filtro aberto. O quadro ao lado do mapa também atualiza a cada 5 s | fila e mapa |
| 5 | Documentação | ✅ README testado do zero (clone novo, ambiente novo, testes, servidor), `RESUMO.md`, `ENTREGA.md` com os textos prontos, IA.md e índice de evidências | `README.md`, `docs/` |
| 6 | Pitch | ✅ roteiro de 90 s cronometrado, ordem de cliques da demo, perguntas da banca, cola para os integrantes e checklist de sábado | `docs/pitch/` |
| + | Mapa com formas de shopping (pedido extra) | ✅ zonas em polígono; os 4 pisos redesenhados do zero com formas irregulares e nomes fictícios; revisor confirmou por programa que nada veio da planta real nem do HTML de referência | `docs/evidencias/mapa/` |
| + | Prints do gato da sexta-feira 13 | ✅ tirados às 22h32 do dia 13 (só valiam naquele dia) | `docs/evidencias/` |

Tags: `v-missao2-entrega` é a versão da entrega. `v-missao2-final` (antes do mapa novo) e `v-missao2-estavel` são pontos de segurança anteriores.

## O que falhou ou deu trabalho
- O limite de uso de uma conta acabou às 23h30, com o revisor no meio do trabalho. O revisor foi retomado na outra conta e terminou. Nada se perdeu, porque tudo já estava em commit e no GitHub.
- O agente de documentação não tinha permissão de push. O coordenador enviou o ramo dele.
- Os ramos dos construtores partiram de uma versão anterior do `main`. Foram reaplicados por cima, com 2 conflitos só em documentação, resolvidos mantendo as duas versões.
- Problemas apontados pelos revisores e já corrigidos: registro duplicado com cliques rápidos, quadro "ao vivo" que não atualizava sozinho, fresta de 2 px no cabeçalho, textos da documentação desatualizados.

## Depois da meia-noite (atualizado sábado 8h40)
| Hora | O que aconteceu |
|---|---|
| 0h35 | Mapa com formas de shopping no `main` e no site (revisor aprovou; nada copiado da planta real) |
| 0h40–2h15 | **Vídeo de 90 s:** versão 1 (88,6 s, telas reais do app, legendas, voz guia). Banca simulada rodada 1: **6,3** (pitch/comunicação) e **7,35** (técnica/negócio). Versão 2 feita com as 10 mudanças pedidas (gancho em movimento, IA contando a própria dúvida, comparação de números no lugar do "100%", diferencial sem exagero, fechamento com piloto de 30 dias e "testes · demo online") |
| 1h45–2h15 | Correções pedidas pela banca técnica, revisadas e no `main`: teste de usabilidade descrito como **pendente**; limites da IA explicados (teste cego pequeno, escrito pela equipe e usado para escolher o modelo; confiança média 37%); FAQ com 6 perguntas difíceis novas (100%, fumaça com 24%, checklist, linha do tempo × demo, gás, planta pública); limite de 9 MB no envio de arquivos com mensagem clara |
| 2h20 | **Limite de uso da conta atingido**: o trabalho parou até de manhã. Nada se perdeu (tudo no GitHub) |
| 8h30 | Produtor retomado para fechar a v2; banca rodada 2 avaliando |

## Decisão que é da equipe (não foi mexido)
- **"Gás" não está na regra fixa de P1.** Hoje "cheiro de gás no restaurante" vira Limpeza P2, sem aviso da brigada. Incluir é uma linha em `app/dominio.py` + um teste, mas muda o contrato da equipe. A FAQ (pergunta 20) já tem a resposta honesta para a banca.

## O que sobrou (só vocês podem fazer)
1. **Teste de usabilidade com 3 pessoas de fora** → `docs/missao-2/teste-usabilidade.md`. Se não der tempo, **apaguem a linha dele** do texto de entrega (está marcada em `docs/ENTREGA.md`): declarar teste não feito é proibido.
2. **Enviar a Missão 2 até 9h45** com o texto pronto de `docs/ENTREGA.md`, e guardar o print do envio em `docs/evidencias/`.
3. **10h:** colar as orientações da Missão 3 em `docs/desafio.md` e conferir se pedem algo além do que está pronto.
4. **Vídeo de 90 s:** já está montado em `/home/arthur/Vídeos/ronda-viva-pitch/` (sem voz e com voz guia). Falta **gravar a voz** (5 min, `docs/pitch/video/GRAVAR-VOZ.md`) e rodar `bash docs/pitch/video/montar_com_voz.sh voz.m4a`. Se não der, enviar a versão com voz guia e declarar no `IA.md`.
5. **Entrega final até 12h** e **vídeo + resumo às 13h** (`docs/RESUMO.md`).
6. Cada um ler `docs/pitch/cola-integrantes.md`: a banca pode perguntar para qualquer um.

## Riscos para a demo
- No celular, os botões de zoom (+/−) cobrem a borda direita da Área técnica (L2) no mapa. Toque no meio da zona.
- O site no ar dorme depois de 15 min e leva ~1 min para acordar. Plano B: rodar no notebook (`python wsgi.py`), descrito em `docs/pitch/demo-cliques.md`.
- O gato da sexta-feira 13 só aparece com `SEXTA13=1 python wsgi.py`, no notebook.
- A planta enviada no "Editar mapa" some quando o site reinicia. Para a demo, usem o desenho fictício.
