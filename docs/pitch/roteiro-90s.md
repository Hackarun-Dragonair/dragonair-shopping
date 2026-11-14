# Roteiro do pitch — 90 segundos

**Regra oficial:** vídeo de 1min15 a 2min, mostrando **problema, solução, principais funcionalidades e diferencial**.
**Nossa meta:** 90 s (sobra folga para os dois lados).
**Fala:** 217 palavras. Ensaie com cronômetro. Se passar de 95 s, corte a frase marcada com (corte 1), depois a (corte 2). Não acelere a fala.

> Tudo o que aparece na tela tem que ser **o app de verdade funcionando**. Sem planta do shopping, sem logo do shopping, sem nome nem rosto de funcionários reais.
> Ordem exata de cliques da demo: [`demo-cliques.md`](demo-cliques.md).

## Quem fala
Duas vozes, para a banca ver que mais de uma pessoa domina o projeto. A equipe escolhe:
- **Voz 1** (problema, solução e fechamento): ____________
- **Voz 2** (demo): ____________

Se for gravar com uma voz só, a pessoa de voz mais clara lê tudo.

## Tabela cronometrada

| Tempo | Quem | O que aparece na tela | Fala (palavra por palavra) |
|---|---|---|---|
| **0:00–0:15** · Problema | Voz 1 | Texto grande sobre fundo bronze: **"Alguém conferiu o banheiro na última hora?"** Depois, ícones de folha de papel e rádio | "Sábado, meio-dia, shopping lotado. Alguém conferiu o banheiro do segundo piso na última hora? Hoje, a resposta é uma folha de papel assinada depois. E os problemas se perdem no rádio e na troca de turno." |
| **0:15–0:30** · Solução | Voz 1 | Nome **Ronda Viva** + slogan. Depois, celular lendo o QR e a tela da zona com os 3 botões | "Por isso criamos a Ronda Viva: mostra o que ninguém conferiu e registra que cuidou. Cada zona tem um QR. O funcionário aponta o celular e toca OK, Atenção ou Problema. Sem instalar nada." |
| **0:30–0:45** · Funcionalidades (1): IA + regra de risco | Voz 2 | Celular: toca **Problema**, digita *"cheiro de fumaça no quadro"*, toca **Ver sugestão da IA**. Aparece a caixa vermelha da brigada, P1 e a pergunta "É mais Limpeza ou Elétrica?"; toca **Elétrica** | "Aqui ele escreveu: cheiro de fumaça no quadro. Nossa IA, treinada pela equipe e sem internet, sugere categoria e prioridade, e avisa quando está em dúvida. Mas fumaça é risco: P1 e avise a brigada pelo rádio. Essa regra fica acima da IA." |
| **0:45–1:05** · Funcionalidades (2): gestor, linha do tempo, mapa, painel | Voz 2 | Computador (OTTO): abre a ocorrência, troca para P3, **Confirmar** → aviso "Prioridade mantida em P1". Rola a **linha do tempo**. Corta para o **mapa** com zonas cinza. Corta para o **painel** | "No computador, o gestor confirma. Se tenta baixar para P3, o sistema mantém P1, e tudo entra numa linha do tempo que não se apaga. No mapa, cinza é a zona que ninguém conferiu no prazo. O painel mede por zona e equipe, nunca por pessoa. (corte 2)" |
| **1:05–1:15** · Funcionalidades (3): acerto real da IA | Voz 2 | Tela **Inteligência artificial** (Sobre a IA): os números e a tabela "Regras x modelo x modelo + regra dura" | "E mostramos o acerto real: no teste cego, os seis casos de risco viraram P1. Mas o teste é pequeno, por isso a IA só sugere." |
| **1:15–1:30** · Diferencial + fechamento | Voz 1 | Mapa com zonas cinza em destaque → nome **Ronda Viva** + slogan + "Equipe Dragonair · HackaRun 2026" | "Folha e checklist mostram o que foi feito. A Ronda Viva mostra o que ninguém conferiu e prova que o shopping cuidou. (corte 1) Ronda Viva: mostra o que ninguém conferiu, registra que cuidou." |

**(corte 1)** = tirar "Folha e checklist mostram o que foi feito." · **(corte 2)** = tirar "O painel mede por zona e equipe, nunca por pessoa."

## Fala corrida (para ensaiar)

> Sábado, meio-dia, shopping lotado. Alguém conferiu o banheiro do segundo piso na última hora? Hoje, a resposta é uma folha de papel assinada depois. E os problemas se perdem no rádio e na troca de turno.
>
> Por isso criamos a Ronda Viva: mostra o que ninguém conferiu e registra que cuidou. Cada zona tem um QR. O funcionário aponta o celular e toca OK, Atenção ou Problema. Sem instalar nada.
>
> Aqui ele escreveu: cheiro de fumaça no quadro. Nossa IA, treinada pela equipe e sem internet, sugere categoria e prioridade, e avisa quando está em dúvida. Mas fumaça é risco: P1 e avise a brigada pelo rádio. Essa regra fica acima da IA.
>
> No computador, o gestor confirma. Se tenta baixar para P3, o sistema mantém P1, e tudo entra numa linha do tempo que não se apaga. No mapa, cinza é a zona que ninguém conferiu no prazo. O painel mede por zona e equipe, nunca por pessoa.
>
> E mostramos o acerto real: no teste cego, os seis casos de risco viraram P1. Mas o teste é pequeno, por isso a IA só sugere.
>
> Folha e checklist mostram o que foi feito. A Ronda Viva mostra o que ninguém conferiu e prova que o shopping cuidou. Ronda Viva: mostra o que ninguém conferiu, registra que cuidou.

## Por que cada frase está aí (para responder à banca)
- **"seis casos de risco viraram P1"**: teste cego com 20 frases; 6 eram P1 e o sistema marcou as 6 (`docs/evidencias/modelo/resumo.md`). Não dizemos "a IA acerta 100%": o teste é pequeno.
- **"avisa quando está em dúvida"**: quando a IA fica entre duas categorias, a tela pergunta "É mais X ou Y?" (sem segunda opção e com confiança abaixo de 50%, mostra "IA em dúvida, confira"). Na frase da demo é um caso real: a IA hesita entre Limpeza e Elétrica e a pessoa decide com um toque.
- **"o sistema mantém P1"**: o gestor escolhe P3, clica em Confirmar e aparece "Prioridade mantida em P1. Palavra de risco não pode ser rebaixada." (testado no QA, `docs/evidencias/qa/`).
- **"linha do tempo que não se apaga"**: o banco tem uma trava que bloqueia apagar ou alterar os eventos.
- **"nunca por pessoa"**: o painel não tem nenhum número por funcionário.

## O que NÃO falar no vídeo
- "A IA acerta 100%." (o teste é pequeno e foi escrito pela equipe)
- "Chama os bombeiros sozinho." (o sistema **não** aciona ninguém)
- "Funciona offline no celular." (sem rede, a tela avisa "Não enviado: sem conexão" e a pessoa tenta de novo; offline completo é próximo passo)
- "Já testamos no shopping." (só dados fictícios)
