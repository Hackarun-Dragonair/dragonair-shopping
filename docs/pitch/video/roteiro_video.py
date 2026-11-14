"""Texto da locução do vídeo (fonte única para legenda, voz guia, montagem e texto-locucao.md).

Versão 2 (depois da banca simulada 1). Cada fala tem:
  - id:    nome curto, usado pela montagem para encaixar as cenas na fala certa;
  - texto: o que aparece na legenda e o que a pessoa lê;
  - tts:   o mesmo texto escrito do jeito que a voz sintética pronuncia melhor;
  - bloco: parte do roteiro;
  - pausa: silêncio depois da fala, em segundos (dentro do bloco).
"""

BLOCOS = {
    "problema": "O problema",
    "solucao": "A solução no dia a dia",
    "ia": "Funcionalidades (1): IA com senso crítico + regra de risco",
    "gestor": "Funcionalidades (2): supervisor, linha do tempo, mapa, painel",
    "acerto": "Funcionalidades (3): o que medimos da IA",
    "diferencial": "Diferencial",
    "fecho": "Próximo passo",
}

INICIO = 0.6          # silêncio antes da primeira fala
PAUSA_BLOCO = 0.7     # silêncio na troca de bloco
FOLGA_FINAL = 1.5     # cartela final depois da última fala
DURACAO_MIN = 80.0    # se a voz for curta, a cartela final segura até aqui (regulamento: mínimo 75 s)
MAX_PALAVRAS_SEG = 2.6  # ritmo máximo por frase (fala + pausa), para dar para ler sem correr

FALAS = [
    # O problema
    dict(id="p1", bloco="problema", pausa=0.3, texto="Sábado, meio-dia, shopping lotado."),
    dict(id="p2", bloco="problema", pausa=0.35, texto="Alguém conferiu o banheiro na última hora?"),
    dict(id="p3", bloco="problema", pausa=0.25, texto="Hoje, a resposta é uma folha assinada depois."),
    dict(id="p4", bloco="problema", pausa=0.0, texto="Se alguém escorrega ali, ninguém sabe quando foi conferido."),
    # A solução no dia a dia
    dict(id="s1", bloco="solucao", pausa=0.3, texto="Por isso criamos a Ronda Viva."),
    dict(id="s2", bloco="solucao", pausa=0.15, texto="Cada zona tem um QR:", tts="Cada zona tem um quê érre:"),
    dict(id="s3", bloco="solucao", pausa=0.3, texto="o funcionário aponta o celular e toca OK, Atenção ou Problema.",
         tts="o funcionário aponta o celular e toca ô quê, Atenção ou Problema."),
    dict(id="s4", bloco="solucao", pausa=0.0, texto="Tocou OK, a zona fica verde.", tts="Tocou ô quê, a zona fica verde."),
    # IA com senso crítico + regra de risco
    dict(id="i1", bloco="ia", pausa=0.25, texto="Viu fumaça no quadro de luz e escreveu."),
    dict(id="i2", bloco="ia", pausa=0.25, texto="A IA ficou em dúvida, só 24%, e perguntou: Limpeza ou Elétrica?",
         tts="A i á ficou em dúvida, só vinte e quatro por cento, e perguntou: Limpeza, ou Elétrica?"),
    dict(id="i3", bloco="ia", pausa=0.3, texto="Ele escolheu Elétrica."),
    dict(id="i4", bloco="ia", pausa=0.2, texto="Mas fumaça é risco: vira P1, prioridade máxima, e manda avisar a brigada.",
         tts="Mas fumaça é risco: vira pê um, prioridade máxima, e manda avisar a brigada."),
    dict(id="i5", bloco="ia", pausa=0.0, texto="Essa regra fica acima da IA.", tts="Essa regra fica acima da i á."),
    # Supervisor, linha do tempo, mapa, painel
    dict(id="g1", bloco="gestor", pausa=0.3, texto="Se o supervisor tenta baixar para P3, o sistema mantém P1.",
         tts="Se o supervisor tenta baixar para pê três, o sistema mantém pê um."),
    dict(id="g2", bloco="gestor", pausa=0.3,
         texto="Fica registrado: a IA sugeriu Limpeza, o supervisor confirmou Elétrica, com hora e nome.",
         tts="Fica registrado: a i á sugeriu Limpeza, o supervisor confirmou Elétrica, com hora e nome."),
    dict(id="g3", bloco="gestor", pausa=0.25, texto="No mapa, cinza é zona sem conferência no prazo."),
    dict(id="g4", bloco="gestor", pausa=0.0, texto="O painel mede por zona e equipe, nunca por pessoa."),
    # O que medimos da IA
    dict(id="a1", bloco="acerto", pausa=0.1, texto="Em 20 frases que a IA nunca viu, palavras-chave pegavam 4 dos 6 riscos;",
         tts="Em vinte frases que a i á nunca viu, palavras-chave pegavam quatro dos seis riscos;"),
    dict(id="a2", bloco="acerto", pausa=0.3, texto="com a IA, os 6.", tts="com a i á, os seis."),
    dict(id="a3", bloco="acerto", pausa=0.15, texto="Em frases reais, a categoria cai para 81%.",
         tts="Em frases reais, a categoria cai para oitenta e um por cento."),
    dict(id="a4", bloco="acerto", pausa=0.0, texto="Por isso uma pessoa confirma."),
    # Diferencial
    dict(id="d1", bloco="diferencial", pausa=0.3, texto="Checklist cobra a tarefa.", tts="Chéque-lista cobra a tarefa."),
    dict(id="d2", bloco="diferencial", pausa=0.0,
         texto="A Ronda Viva mostra o lugar: a zona esquecida fica cinza antes da reclamação."),
    # Próximo passo
    dict(id="f1", bloco="fecho", pausa=0.1,
         texto="Próximo passo: piloto de 30 dias em sanitários e praça de alimentação,",
         tts="Próximo passo: piloto de trinta dias em sanitários e praça de alimentação,"),
    dict(id="f2", bloco="fecho", pausa=0.0, texto="com etiquetas e o celular da equipe."),
]

for f in FALAS:
    f.setdefault("tts", f["texto"])


def palavras(texto=None) -> int:
    if texto is not None:
        return len(texto.split())
    return sum(len(f["texto"].split()) for f in FALAS)


if __name__ == "__main__":
    print(len(FALAS), "falas,", palavras(), "palavras")
