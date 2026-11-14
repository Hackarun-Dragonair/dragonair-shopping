"""Texto da locução do vídeo (fonte única para legenda, voz guia e texto-locucao.md).

Cada fala tem:
  - texto: o que aparece na legenda e o que a pessoa lê;
  - tts:   o mesmo texto escrito do jeito que a voz sintética pronuncia melhor;
  - bloco: parte do roteiro (docs/pitch/roteiro-90s.md);
  - pausa: silêncio depois da fala, em segundos.
"""

BLOCOS = {
    "problema": "Problema",
    "solucao": "Solução",
    "ia": "Funcionalidades (1): IA + regra de risco",
    "gestor": "Funcionalidades (2): gestor, linha do tempo, mapa, painel",
    "acerto": "Funcionalidades (3): acerto real da IA",
    "diferencial": "Diferencial + fechamento",
}

# Atraso antes da primeira fala (a primeira cartela aparece sozinha por um instante).
INICIO = 0.6

# Segundo em que cada bloco começa a ser falado (segue a tabela do roteiro-90s.md).
# Se o bloco anterior passar do tempo, o seguinte começa logo depois dele.
ANCORAS = {"problema": 0.6, "solucao": 15.0, "ia": 29.4, "gestor": 46.2, "acerto": 63.0, "diferencial": 74.2}

# Duração final do vídeo, em segundos.
DURACAO = 88.6

FALAS = [
    # 0:00 Problema
    dict(bloco="problema", pausa=0.35, texto="Sábado, meio-dia, shopping lotado."),
    dict(bloco="problema", pausa=0.55, texto="Alguém conferiu o banheiro do segundo piso na última hora?"),
    dict(bloco="problema", pausa=0.25, texto="Hoje, a resposta é uma folha de papel assinada depois."),
    dict(bloco="problema", pausa=0.6, texto="E os problemas se perdem no rádio e na troca de turno."),
    # 0:15 Solução
    dict(bloco="solucao", pausa=0.1, texto="Por isso criamos a Ronda Viva:"),
    dict(bloco="solucao", pausa=0.5, texto="mostra o que ninguém conferiu e registra que cuidou."),
    dict(bloco="solucao", pausa=0.2, texto="Cada zona tem um QR.", tts="Cada zona tem um quê érre."),
    dict(bloco="solucao", pausa=0.2, texto="O funcionário aponta o celular e toca OK, Atenção ou Problema.",
         tts="O funcionário aponta o celular e toca ô quê, Atenção ou Problema."),
    dict(bloco="solucao", pausa=0.5, texto="Sem instalar nada."),
    # 0:30 IA + regra de risco
    dict(bloco="ia", pausa=0.3, texto="Ele escreveu: cheiro de fumaça no quadro."),
    dict(bloco="ia", pausa=0.05, texto="Nossa IA, treinada pela equipe e sem internet, sugere categoria e prioridade,",
         tts="Nossa i á, treinada pela equipe e sem internet, sugere categoria e prioridade,"),
    dict(bloco="ia", pausa=0.35, texto="e avisa quando está em dúvida."),
    dict(bloco="ia", pausa=0.2, texto="Mas fumaça é risco: P1 e avise a brigada pelo rádio.",
         tts="Mas fumaça é risco: pê um, e avise a brigada pelo rádio."),
    dict(bloco="ia", pausa=0.55, texto="Essa regra fica acima da IA.", tts="Essa regra fica acima da i á."),
    # 0:45 Gestor, linha do tempo, mapa, painel
    dict(bloco="gestor", pausa=0.2, texto="No computador, o gestor confirma."),
    dict(bloco="gestor", pausa=0.05, texto="Se tenta baixar para P3, o sistema mantém P1,",
         tts="Se tenta baixar para pê três, o sistema mantém pê um,"),
    dict(bloco="gestor", pausa=0.4, texto="e tudo entra numa linha do tempo que não se apaga."),
    dict(bloco="gestor", pausa=0.35, texto="No mapa, cinza é a zona que ninguém conferiu no prazo."),
    dict(bloco="gestor", pausa=0.5, texto="O painel mede por zona e equipe, nunca por pessoa."),
    # 1:05 Acerto real
    dict(bloco="acerto", pausa=0.2, texto="Mostramos o acerto real: no teste cego, os seis casos de risco viraram P1.",
         tts="Mostramos o acerto real: no teste cego, os seis casos de risco viraram pê um."),
    dict(bloco="acerto", pausa=0.6, texto="Mas o teste é pequeno, por isso a IA só sugere.",
         tts="Mas o teste é pequeno, por isso a i á só sugere."),
    # 1:15 Diferencial + fechamento
    dict(bloco="diferencial", pausa=0.2, texto="Folha e checklist mostram o que foi feito.",
         tts="Folha e chéque-lista mostram o que foi feito."),
    dict(bloco="diferencial", pausa=0.6, texto="A Ronda Viva mostra o que ninguém conferiu e prova que o shopping cuidou."),
    dict(bloco="diferencial", pausa=0.0, texto="Ronda Viva: mostra o que ninguém conferiu, registra que cuidou."),
]

for f in FALAS:
    f.setdefault("tts", f["texto"])


def palavras() -> int:
    return sum(len(f["texto"].split()) for f in FALAS)


if __name__ == "__main__":
    print(len(FALAS), "falas,", palavras(), "palavras")
