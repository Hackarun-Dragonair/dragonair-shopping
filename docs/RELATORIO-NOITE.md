# Relatório da noite — sexta 13/11 para sábado 14/11

> Trabalho feito por agentes de IA (Claude Code) com autorização do Arthur, seguindo as regras dele: escopo congelado, revisor aprova antes do `main`, testes antes de cada commit, conferir o Render depois de cada envio. Declarado em `docs/IA.md`.
> Encerrado às 23h50 de sexta: os 6 itens combinados terminaram antes das 6h.

## Resultado em uma linha
Tudo combinado está no `main`, publicado no site e marcado com a tag **`v-missao2-final`**. São 73 testes passando, e duas revisões independentes aprovaram sem nenhum problema grave.

## O que foi feito
| # | Item | Situação | Onde ver |
|---|---|---|---|
| 1 | QA + visual novo no `main` | ✅ no ar | `docs/evidencias/qa/` |
| 2 | QR de verdade | ✅ as 11 etiquetas do site no ar foram lidas por imagem; cada uma abre a zona certa sem login. O desenho do QR foi corrigido para ler melhor depois de impresso | `docs/evidencias/qr/` |
| 3 | Pergunta de desempate da IA | ✅ na frase da demo ("cheiro de fumaça no quadro") a tela pergunta "É mais Limpeza ou Elétrica?" e continua P1 com o aviso da brigada | tela da zona |
| 4 | Fila a cada 5 s | ✅ mantém a rolagem e não recarrega com o filtro aberto. O quadro ao lado do mapa também atualiza a cada 5 s | fila e mapa |
| 5 | Documentação | ✅ README testado do zero (clone novo, ambiente novo, testes, servidor), `RESUMO.md`, `ENTREGA.md` com os textos prontos, IA.md e índice de evidências | `README.md`, `docs/` |
| 6 | Pitch | ✅ roteiro de 90 s cronometrado, ordem de cliques da demo, perguntas da banca, cola para os integrantes e checklist de sábado | `docs/pitch/` |
| + | Prints do gato da sexta-feira 13 | ✅ tirados às 22h32 do dia 13 (só valiam naquele dia) | `docs/evidencias/` |

Tags: `v-missao2-final` é a versão da entrega. `v-missao2-estavel` é o ponto de segurança anterior.

## O que falhou ou deu trabalho
- O limite de uso de uma conta acabou às 23h30, com o revisor no meio do trabalho. O revisor foi retomado na outra conta e terminou. Nada se perdeu, porque tudo já estava em commit e no GitHub.
- O agente de documentação não tinha permissão de push. O coordenador enviou o ramo dele.
- Os ramos dos construtores partiram de uma versão anterior do `main`. Foram reaplicados por cima, com 2 conflitos só em documentação, resolvidos mantendo as duas versões.
- Problemas apontados pelos revisores e já corrigidos: registro duplicado com cliques rápidos, quadro "ao vivo" que não atualizava sozinho, fresta de 2 px no cabeçalho, textos da documentação desatualizados.

## O que sobrou (só vocês podem fazer)
1. **Teste de usabilidade com 3 pessoas de fora** → `docs/missao-2/teste-usabilidade.md`. Se não der tempo, **apaguem a linha dele** do texto de entrega (está marcada em `docs/ENTREGA.md`): declarar teste não feito é proibido.
2. **Enviar a Missão 2 até 9h45** com o texto pronto de `docs/ENTREGA.md`, e guardar o print do envio em `docs/evidencias/`.
3. **10h:** colar as orientações da Missão 3 em `docs/desafio.md` e conferir se pedem algo além do que está pronto.
4. **Gravar o vídeo de 90 s** seguindo `docs/pitch/roteiro-90s.md` e `docs/pitch/demo-cliques.md`. Preencham quem fala (Voz 1 e Voz 2). Abram o site uns 2 minutos antes, porque ele dorme.
5. **Entrega final até 12h** e **vídeo + resumo às 13h** (`docs/RESUMO.md`).
6. Cada um ler `docs/pitch/cola-integrantes.md`: a banca pode perguntar para qualquer um.

## Riscos para a demo
- O site no ar dorme depois de 15 min e leva ~1 min para acordar. Plano B: rodar no notebook (`python wsgi.py`), descrito em `docs/pitch/demo-cliques.md`.
- O gato da sexta-feira 13 só aparece com `SEXTA13=1 python wsgi.py`, no notebook.
- A planta enviada no "Editar mapa" some quando o site reinicia. Para a demo, usem o desenho fictício.
