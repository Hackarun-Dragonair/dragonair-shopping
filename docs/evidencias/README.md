# Evidências

Critério "Cumprimento das missões e qualidade das evidências" vale 20%. Tudo aqui é do projeto de verdade: nenhum print montado, nenhum teste simulado.

**Nome dos arquivos:** `m<missão>_<dia>-<hora>_<descricao>.png` · Ex.: `m2_14-0930_teste-usabilidade-pessoa1.png`
**Proibido:** dados pessoais de colegas ou visitantes, chaves de API, planta do shopping, evidência simulada.

## Índice por missão

### Missão 1 — problema, requisitos e planejamento técnico (12 e 13/11)
| Evidência | O que mostra |
|---|---|
| [`desafio-09.png`](desafio-09.png) | Tira oficial do desafio sorteado (transcrita em [`../desafio.md`](../desafio.md)) |
| [`primeira-entrega-orientacoes.jpg`](primeira-entrega-orientacoes.jpg) | Orientações da 1ª entrega (grupo, 12/11) |
| [`m1_13-1153_confirmacao-entrega1.png`](m1_13-1153_confirmacao-entrega1.png) | Comprovante do envio da Entrega 1 ("Sua resposta foi registrada", 13/11 11h53) |
| [`../missao-1/ENTREGA-1.md`](../missao-1/ENTREGA-1.md) + PDFs na mesma pasta | O documento entregue (telas, arquitetura, tecnologias, responsividade) |
| [`../missao-1/README.md`](../missao-1/README.md) | Planejamento detalhado: problema, público, Canvas, backlog priorizado |
| Issue #1 no GitHub | Discussão da ideia pela equipe |

### Missão 2 — protótipo funcional, testes e correções (13 e 14/11)
| Evidência | O que mostra |
|---|---|
| [`qa/`](qa/README.md) (README + 10 prints) | QA ponta a ponta (13/11, 22h) no computador (1366 px) e no celular (390 px): 7 problemas achados e corrigidos em 8 commits `fix:`, com prints da versão final |
| [`responsividade/`](responsividade/README.md) (README + 8 prints) | Tecnologia sorteada: as 6 telas em 6 larguras (375 a 1920 px), sem vazar para o lado, menu certo, botões fáceis de tocar; 1 correção feita no teste |
| [`modelo/`](modelo/resumo.md) (`resumo.md` + 2 CSVs) | Avaliação da IA gerada por `python -m app.avaliar`: teste cego (n = 20: 100% categoria, 95% prioridade, 6 de 6 P1) e teste de campo (n = 16, rótulos a revisar: 81% e 62%), comparação regras x modelo x modelo + regra dura, matriz de confusão, erro por frase |
| [`m2_13-2240_gato-sexta13-no-mapa.png`](m2_13-2240_gato-sexta13-no-mapa.png) · [`m2_13-2240_gato-sexta13-celular.png`](m2_13-2240_gato-sexta13-celular.png) | Easter Egg: gato preto na zona esquecida há mais tempo (print real do dia 13/11, 22h32) |
| [`m2_13-2240_gato-espantado.png`](m2_13-2240_gato-espantado.png) | Conferir a zona espanta o gato: "Gato preto espantado!" |
| [`qr/`](qr/README.md) (README + `m2_13-2242_etiquetas-qr.png`) | QR de verdade: o PDF de etiquetas (local e do site no ar) virou imagem e cada QR foi lido: 11 zonas → endereço certo → abre sem login (HTTP 200). Depois, correção do desenho do QR (`fix:`) para ler melhor impresso |
| [`mapa/`](mapa/README.md) (README + 8 prints) | Mapa com formas de shopping: zonas em polígono, 4 pisos redesenhados do zero (fictício, sem a planta real), no computador e no celular |
| [`../missao-2/teste-usabilidade.md`](../missao-2/teste-usabilidade.md) | Teste com 3 pessoas de fora: roteiro, folha de anotação e resumo (preenchido pela equipe no dia) |
| Testes automáticos: pasta `tests/` + GitHub Actions | 77 testes (pytest) rodando em todo pull request (aba **Actions** do repositório) |
| Histórico do git (commits `fix:`) | Cada correção com uma frase explicando o que mudou |
| Print do envio da Missão 2 | *(a salvar aqui no sábado: `m2_14-0945_envio-missao2.png`)* |

### Missão 3 — versão final, documentação e pitch (14/11)
| Evidência | O que mostra |
|---|---|
| [`../../README.md`](../../README.md#como-executar) | Instruções de execução testadas do zero (clone novo, ambiente novo, testes e servidor) |
| [`../RESUMO.md`](../RESUMO.md) | Resumo de 1 página |
| [`../pitch/`](../pitch/) | Roteiro de 90 s, cliques da demo, FAQ da banca, cola para integrantes, checklist de sábado |
| [`../ENTREGA.md`](../ENTREGA.md) | Checklist final e textos de entrega |
| [`../IA.md`](../IA.md) | Declaração de uso de IA (desenvolvimento e dentro da solução) |
| Orientações da Missão 3 | *(colar em [`../desafio.md`](../desafio.md) às 10h)* |
| Print do envio final e do vídeo | *(a salvar aqui: `m3_14-1200_envio-final.png`, `m3_14-1300_envio-video.png`)* |
