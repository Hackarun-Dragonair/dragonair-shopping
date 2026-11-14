# Evidência: o QR das etiquetas funciona de verdade

**Quando:** sexta, 13/11/2026, 22:40–22:47 (horário de Brasília).
**Imagem:** `m2_13-2242_etiquetas-qr.png` é a 1ª página do PDF baixado do site no ar às 22:42, renderizada com PyMuPDF (150 dpi). Nada foi editado.

## Como testamos

1. Entramos como gestor com o crachá fictício `OTTO` (`POST /entrar/cracha`, `cracha=OTTO&perfil=gestor`) e baixamos `GET /etiquetas.pdf`.
2. Cada página do PDF virou imagem (PyMuPDF) e o QR foi **lido da imagem** pelo OpenCV (`cv2.QRCodeDetector`). Conferimos com uma segunda leitora (zxing-cpp, a mesma base de muitos leitores de celular).
3. Cada URL lida foi aberta **sem cookie** (como quem não tem crachá) e conferimos: HTTP 200 e a tela da zona com os botões OK / Atenção / Problema.
4. Feito em três cenários: (a) app local com `PUBLIC_BASE_URL` vazio; (b) app local com `PUBLIC_BASE_URL=https://ronda-viva-0ek7.onrender.com`; (c) PDF baixado do site no ar no Render.

As ferramentas de leitura ficaram num ambiente separado, fora do `requirements.txt` do projeto.

## Resultado no site no ar (Render)

11 zonas no sistema, 11 páginas no PDF, 11 QR lidos, 11 telas abertas.

| Zona | URL lida do QR | HTTP |
|---|---|---|
| Doca 1 | https://ronda-viva-0ek7.onrender.com/z/doca-1 | 200 |
| Entrada principal | https://ronda-viva-0ek7.onrender.com/z/entrada-principal | 200 |
| Banheiro L1 sul | https://ronda-viva-0ek7.onrender.com/z/banheiro-l1-sul | 200 |
| Corredor mall norte | https://ronda-viva-0ek7.onrender.com/z/corredor-norte | 200 |
| Escada rolante norte | https://ronda-viva-0ek7.onrender.com/z/escada-norte | 200 |
| Praça de alimentação — setor A | https://ronda-viva-0ek7.onrender.com/z/praca-a | 200 |
| Praça de alimentação — setor B | https://ronda-viva-0ek7.onrender.com/z/praca-b | 200 |
| Sanitário piso 1 | https://ronda-viva-0ek7.onrender.com/z/sanitario-piso1 | 200 |
| Banheiro L2 norte | https://ronda-viva-0ek7.onrender.com/z/banheiro-l2-norte | 200 |
| Área técnica L2 | https://ronda-viva-0ek7.onrender.com/z/area-tecnica-l2 | 200 |
| Estacionamento G1 | https://ronda-viva-0ek7.onrender.com/z/estacionamento-g1 | 200 |

Todas com `https` e o endereço público (nenhuma com `127.0.0.1` ou `localhost`). O Render não tem `PUBLIC_BASE_URL` configurado; o endereço certo vem dos cabeçalhos do proxy (ProxyFix).

## Resultado local

| Cenário | QR lidos | URLs | HTTP |
|---|---|---|---|
| `PUBLIC_BASE_URL` vazio | 11/11 | `http://127.0.0.1:8773/z/<codigo>` (endereço de quem pediu) | 11× 200 |
| `PUBLIC_BASE_URL` = site do Render | 11/11 | `https://ronda-viva-0ek7.onrender.com/z/<codigo>` | 11× 200 |

## O que falhou e como corrigimos

Nada impediu o QR de funcionar, então não houve mudança no código do app.
Observação: o OpenCV não leu 1 de 11 QR quando a página foi renderizada em 300 dpi (e nenhum em 600 dpi), por causa de filetes brancos finos entre os quadradinhos do desenho. O zxing-cpp leu os 11 em 72, 150, 300 e 600 dpi, e o OpenCV leu todos em 72–200 dpi. Não mexemos para não mudar escopo; se algum celular falhar na demo, imprima em "qualidade normal".

Para não quebrar no futuro, entraram 3 testes em `tests/test_backlog.py`: a URL usa `PUBLIC_BASE_URL` quando configurado; atrás do proxy do Render usa `https` e o host público; e cada URL abre sem login com os três botões.

## Como imprimir as etiquetas e testar com o celular na demo

1. Uns 2 minutos antes, abra https://ronda-viva-0ek7.onrender.com no celular para "acordar" o site (no plano grátis ele dorme e o 1º acesso demora até ~1 min).
2. No computador, entre com o crachá `OTTO` (gestor), abra o Painel e clique em "Etiquetas QR (PDF)".
3. Imprima em A4, tamanho real (100%, sem "ajustar à página"); cada folha é uma zona.
4. Com a câmera do celular (sem login), aponte para o QR: deve abrir a tela da zona com OK / Atenção / Problema.
5. Toque em OK e confira no mapa (no computador) que a zona ficou verde.
