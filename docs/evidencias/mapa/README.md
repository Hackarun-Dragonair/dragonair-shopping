# Novo desenho do mapa (formas irregulares)

**Desenho fictício feito do zero; não usa a planta do shopping.** Nenhum nome de loja ou marca real (o teste `tests/test_mapa_desenho.py` confere).

## O que mudou
- Antes o mapa era "retângulo dentro de retângulo". Agora cada piso tem contorno irregular, como uma planta de shopping: fachada curva no Térreo, átrio redondo, duas âncoras nas pontas, praça de alimentação em leque no L1, cinema e vão do átrio no L2, rampa curva e vagas inclinadas no estacionamento.
- O mapa passou a aceitar zona em **polígono** (`pts`) e decoração em polígono ou caminho curvo (`d`), além do retângulo antigo. Ou seja: a geometria irregular já está pronta para quando o desenho real das zonas for definido pela equipe.
- No celular (390 px) as letras do mapa crescem e alguns nomes ficam curtos ("Praça A", "Banheiro sul"), para continuar legível com o mapa inteiro na tela.
- Continua igual: cores por estado, toque/Enter abre o painel da zona, gato preto no canto da zona, zoom e arrasto, legenda, contadores e atualização a cada 5 s. O "modo planta" do editor não mudou.

## Como foi conferido (Chrome via Playwright, 1366 px e 390 px)
- 4 pisos, 11 zonas: todas aparecem, nome e estado cabem dentro de cada zona, sem erro de JavaScript.
- Clique em cada uma das 11 zonas abre o painel certo (nas duas larguras); Enter no teclado também abre.
- Cores mudam: OK pelo painel (cinza → verde), Atenção pelo painel (cinza → amarelo), problema registrado pela tela da zona (verde → vermelho) aparece sozinho em até 5 s.

## Prints (14/11, 00:19)
| Piso | Computador | Celular |
|---|---|---|
| Térreo | `m2_14-0019_mapa-terreo-pc.png` | `m2_14-0019_mapa-terreo-cel.png` |
| L1 | `m2_14-0019_mapa-l1-pc.png` | `m2_14-0019_mapa-l1-cel.png` |
| L2 | `m2_14-0019_mapa-l2-pc.png` | `m2_14-0019_mapa-l2-cel.png` |
| Estacionamento | `m2_14-0019_mapa-estacionamento-pc.png` | `m2_14-0019_mapa-estacionamento-cel.png` |

Mapa denso (14/11, 10h11, computador 1366 px): `m2_14-1011_mapa-denso-terreo.png`, `-l1`, `-l2`, `-estacionamento` — desenho fictício com dezenas de lojas geradas por função (Térreo 71, L1 68, L2 44 blocos; garagem com vagas); as 11 zonas iguais, tocáveis, zero erro de JS, conferido também em 390 px.
