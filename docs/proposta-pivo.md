# Proposta: a Ronda Viva ganha olhos (câmera + sensor)

> Sugestão do mentor: "tirar o máximo da mão das pessoas e dar ao sistema".
> **Nada do que fizemos vai para o lixo.** A câmera é só mais uma forma de abrir ocorrência na fila que já existe.

**Frase:** a câmera percebe o movimento, a equipe confere, e o painel mostra o que ninguém olhou e o que foi resolvido. Sem rosto, sem nome, só números.

## O que muda (pouco)
| Entrada | Onde | O que faz |
|---|---|---|
| 📱 QR (já pronto) | Banheiros e lugares sem câmera | Igual a hoje |
| 📹 Câmera (novo) | Praça de alimentação, corredores | Conta pessoas por zona. Movimento alto → sugere "Reforçar limpeza" (P3) |
| 📟 Sensor (novo, **SIMULADO**) | Doca, casa de máquinas | Fumaça → P1 + "Avise a brigada" (regra que já existe) |

**Limpeza por demanda, não por horário fixo.** É isso que a câmera traz de novo.

## O que fica de cada um (tudo continua)
| Quem | O que já fez | Como entra na proposta |
|---|---|---|
| Paulo | Backend Flask, regra de risco P1, linha do tempo | A câmera e o sensor usam **a mesma** fila, regra P1 e linha do tempo |
| Mateus | Telas (mapa, zona, fila) | O mapa ganha "📹 N pessoas agora" e a fila ganha o selo "Câmera/Sensor" |
| Pedro | Frases da IA de triagem | A IA de texto continua no QR; a câmera é uma 2ª IA (visão) |
| Arthur | Docs, IA.md, organização | Proposta, roteiro da demo, evidências |

## Regras que a banca rigorosa pediu
- A câmera **sugere** e uma **pessoa confirma**. A zona só sai do cinza com conferência humana.
- 3 leituras seguidas acima do limite (sem alarme por 1 pico) e nada de duplicar a ocorrência.
- Demo com **replay**: o YOLO roda antes num vídeo nosso, e a demo reenvia os números. Não falha ao vivo.
- Sem câmera no banheiro, sem vídeo cru no repo, rostos pixelados. Sensor escrito **SIMULADO**.
- **Prazo de corte:** se não estiver funcionando até 01h, fica só o produto atual (o `main` não muda até o grupo aprovar).

## Já feito no branch `proposta-camera` (testado: 40 testes passando)
- `POST /eventos/camera`, `POST /eventos/sensor`, `GET /eventos/movimento`
- Contagem no mapa, selo na fila, botão "Simular sensor (SIMULADO)" na zona
- `camera/contador.py` (YOLO + supervision), `camera/replay.py`, `camera/simular_sensor.py`
- 10 testes novos em `tests/test_eventos.py`

## Falta (se o grupo aprovar)
1. Gravar 30 s da equipe andando (com consentimento) e rodar o `contador.py` → `contagens.json` real
2. Mateus: conferir no celular o mapa com a contagem
3. Atualizar o roteiro do vídeo (Missão 3) e o `docs/IA.md`
4. Prints e vídeo pixelado em `docs/evidencias/`

## Como isso pesa na nota
- **Resolução do problema (25):** identifica ocorrência sem depender de alguém passar.
- **Inovação (20):** 2 IAs (texto + visão) com regra de segurança que a IA não pode rebaixar.
- **Implementação (25):** testes novos e demo que não quebra (replay).
- **UX (15):** ninguém precisa digitar nada; o celular só confirma.
