# Texto da locução — pitch de 90 s (Ronda Viva)

Leia em voz alta, **no seu jeito de falar**, como quem conta para um amigo o que o sistema faz.
Os tempos são da voz guia (`pitch-90s-voz-guia.mp4`): assista uma vez antes, para pegar o ritmo.
Não precisa bater no segundo: o script `montar_com_voz.sh` encaixa a sua voz e acerta as legendas sozinho.

**Como ler as marcas**
- `/` = respira curto (meio segundo).
- `//` = pausa de troca de assunto (1 a 2 segundos). **Faça essas pausas**: é por elas que o script acha onde começa cada parte do vídeo.
- **Negrito** = palavra para dar ênfase.
- Pode falar "pra" no lugar de "para" e "tá" no lugar de "está", se sair mais natural. Não troque o resto: a legenda segue este texto.
- "P1" se fala **pê um**; "P3", **pê três**; "QR", **quê érre**; "IA", **i á**.

Duração total da fala: **cerca de 84 segundos** (o vídeo tem 88,6 s; a cartela final fica 4 s em silêncio).
Ritmo: calmo, cerca de **2,6 palavras por segundo**. Se passar de 90 s, o script acelera no máximo 6%, sem cortar nada.

---

## [0:00–0:14] O problema
*Tom: pergunta de verdade, como quem já viu isso acontecer.*

> Sábado, meio-dia, shopping lotado. /
> Alguém conferiu o banheiro do segundo piso **na última hora**? /
> Hoje, a resposta é uma folha de papel assinada **depois**. /
> E os problemas se perdem no rádio e na troca de turno.

`//`

## [0:14–0:27] A solução
*Tom: firme, é a virada. Diga o nome com orgulho.*

> Por isso criamos a **Ronda Viva**: mostra o que **ninguém conferiu** e registra que **cuidou**. /
> Cada zona tem um QR. /
> O funcionário aponta o celular e toca OK, Atenção ou Problema. /
> **Sem instalar nada.**

`//`

## [0:28–0:46] Funcionalidades: IA e regra de risco
*Tom: mostrando a tela para alguém do lado.*

> Aqui ele escreveu: cheiro de fumaça no quadro. /
> A IA, treinada pela equipe, roda **sem internet** e sugere categoria e prioridade, /
> e **avisa quando fica em dúvida**. /
> Mas fumaça é risco: vira **P1**, e a tela manda avisar a brigada pelo rádio. /
> Essa regra fica **acima da IA**.

`//`

## [0:46–1:02] Funcionalidades: gestor, linha do tempo, mapa e painel
*Tom: tranquilo, um item por frase.*

> No computador, o gestor confirma. /
> Se tenta baixar para P3, o sistema **mantém P1**. /
> E tudo fica numa linha do tempo que **não se apaga**. /
> No mapa, **cinza** é a zona que ninguém conferiu no prazo. /
> O painel mede por zona e equipe, **nunca por pessoa**.

`//`

## [1:03–1:12] Acerto real da IA
*Tom: honesto, sem exagero.*

> E o acerto é real: no teste cego, os **seis** casos de risco viraram P1. /
> Mas o teste é pequeno, então a IA **só sugere**.

`//`

## [1:14–1:25] Diferencial e fechamento
*Tom: devagar no final. A última frase é o slogan: sorria ao falar.*

> Folha e checklist mostram o que foi feito. /
> A Ronda Viva mostra o que **ninguém conferiu** e **prova** que o shopping cuidou. //
> Ronda Viva: mostra o que ninguém conferiu, / registra que cuidou.

---

## Tempos de cada frase (voz guia)

| Tempo | Frase |
|---|---|
| 0:00,6–0:02,8 | Sábado, meio-dia, shopping lotado. |
| 0:03,1–0:06,3 | Alguém conferiu o banheiro do segundo piso na última hora? |
| 0:06,8–0:10,5 | Hoje, a resposta é uma folha de papel assinada depois. |
| 0:10,8–0:13,8 | E os problemas se perdem no rádio e na troca de turno. |
| 0:14,5–0:18,8 | Por isso criamos a Ronda Viva: mostra o que ninguém conferiu e registra que cuidou. |
| 0:19,3–0:20,6 | Cada zona tem um QR. |
| 0:20,8–0:25,5 | O funcionário aponta o celular e toca OK, Atenção ou Problema. |
| 0:25,7–0:26,8 | Sem instalar nada. |
| 0:28,6–0:31,4 | Aqui ele escreveu: cheiro de fumaça no quadro. |
| 0:31,7–0:37,2 | A IA, treinada pela equipe, roda sem internet e sugere categoria e prioridade, |
| 0:37,2–0:39,0 | e avisa quando fica em dúvida. |
| 0:39,3–0:44,0 | Mas fumaça é risco: vira P1, e a tela manda avisar a brigada pelo rádio. |
| 0:44,2–0:46,0 | Essa regra fica acima da IA. |
| 0:46,9–0:49,0 | No computador, o gestor confirma. |
| 0:49,2–0:52,4 | Se tenta baixar para P3, o sistema mantém P1. |
| 0:52,6–0:55,0 | E tudo fica numa linha do tempo que não se apaga. |
| 0:55,4–0:58,6 | No mapa, cinza é a zona que ninguém conferiu no prazo. |
| 0:58,9–1:02,3 | O painel mede por zona e equipe, nunca por pessoa. |
| 1:03,4–1:08,2 | E o acerto é real: no teste cego, os seis casos de risco viraram P1. |
| 1:08,4–1:11,5 | Mas o teste é pequeno, então a IA só sugere. |
| 1:13,8–1:16,5 | Folha e checklist mostram o que foi feito. |
| 1:16,7–1:20,4 | A Ronda Viva mostra o que ninguém conferiu e prova que o shopping cuidou. |
| 1:21,0–1:24,4 | Ronda Viva: mostra o que ninguém conferiu, registra que cuidou. |

221 palavras. O texto vem de `roteiro_video.py` (fonte única: legenda, voz guia e este arquivo).
Se mudar uma frase lá, mude aqui também e rode de novo o `fazer_video.sh`.

## O que NÃO falar (do roteiro oficial)
- "A IA acerta 100%." · "Chama os bombeiros sozinho." · "Funciona offline no celular." · "Já testamos no shopping."
