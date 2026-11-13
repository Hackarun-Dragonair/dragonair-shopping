# Declaração de uso de IA

Exigida pelo regulamento: registrar ferramentas e finalidades. Nenhum dado pessoal ou de terceiros foi inserido em ferramentas de IA.

A equipe revisou e responde por todo conteúdo gerado com IA.

## No desenvolvimento
| Data/hora | Quem | Ferramenta | Finalidade | O que a equipe revisou/mudou |
|---|---|---|---|---|
| 12/11 21h | Arthur | Claude | Transcrever o desafio e gerar o esqueleto do repositório (README, .gitignore, pastas de docs) | Conferiu a transcrição com a foto; ajustou estrutura |
| 12/11 21h40 | Arthur | Claude (agente "especialista em gestão de shopping") | Pesquisar dores reais de operação de shopping, indicadores (NBR 5674) e sugerir ideias | Equipe discutiu e adaptou a ideia própria (chamados + mapa + IA) |
| 12/11 22h | Arthur | Claude (agente "banca simulada") | Criticar a ideia v1 como fariam os avaliadores | Críticas levadas para discussão na Issue #1 |
| 12/11 22h | Arthur | Claude | Escrever o README-guia da equipe e a Issue #1 | Revisado pelo Arthur |
| 12/11 23h | Arthur | Claude (agentes: 6 especialistas + 8 avaliadores simulando perfis da banca) | Gerar ideias, criticar e comparar 13 propostas (incluindo a de um integrante) em várias rodadas | Arthur escolheu a Ronda Viva e incorporou peças da proposta do colega |
| 13/11 madrugada | Arthur | Claude | Redigir o documento da Missão 1 a partir das decisões da equipe | Revisado pelo Arthur antes do envio |
| 13/11 7h40 | Arthur | Claude (8 avaliadores simulados) | Rodada de estresse do dossiê completo: perguntas duras, incoerências e promessas exageradas | Equipe aplicou 8 mudanças: regra de risco nunca rebaixa, linha do tempo no lugar do login completo, pitch só com o que será demonstrado, slogan novo |
| 13/11 12h30 | Bypaulohx | Cursor (Grok) | Implementar a base Flask da Missão 2: rotas, SQLite, triagem, mapa, fila, painel e linha do tempo, a partir do planejamento da equipe | A equipe revisa no pull request. As telas HTML geradas nessa sessão foram removidas: o front-end é de outra pessoa. A API ficou em JSON |
| 13/11 manhã | Mateus | Gemini | Gerar o protótipo visual das telas (HTML + Bootstrap) | Equipe usou o protótipo como base do visual. A parte que usava a planta do shopping foi retirada (dado sensível) |
| 13/11 13h | Arthur | Claude | Montar o quadro de tarefas, o guia da equipe, o roteiro do teste com usuários e o roteiro do vídeo | Arthur definiu a divisão; equipe revisa |
| 13/11 15h | Arthur | Claude | Criar as telas responsivas (mapa em blocos, tela da zona com sugestão da IA, fila, linha do tempo, painel, Sobre a IA) em cima da API do Paulo, seguindo o visual do protótipo do Mateus | Arthur revisa e ensaia a explicação; Mateus ajusta o visual |

## Dentro da solução

**Onde:** tela da zona (`/z/<codigo>`). Quem achou o problema escreve do seu jeito, e a IA **sugere categoria e prioridade** (a equipe vem da categoria). O supervisor confirma ou corrige na tela do problema.

**Qual modelo:** feito pela equipe com scikit-learn, sem API paga e sem internet (`app/modelo.py`).
1. A frase vira números com **TF-IDF**: palavras e pedaços de palavra (ajuda com erro de digitação).
2. Uma **Regressão Logística** aprende quais palavras indicam cada categoria e prioridade.
3. Treinado com `data/treino.csv` (frases **fictícias** escritas pela equipe).

**Como medimos:** um **teste cego** (`data/teste_cego.csv`) com frases que o modelo nunca viu, comparado com uma regra simples de palavras-chave. Os números aparecem na tela **"Sobre a IA"** (`/telas/sobre-a-ia`).

**Como lidamos com os erros da IA:**
- Ela só **sugere**. A tela mostra a confiança, e abaixo de 50% avisa "IA em dúvida, confira".
- **Regra fixa acima da IA** (`app/dominio.py`): fumaça, fogo, choque ou pessoa presa → **P1** e "Avise a brigada pelo rádio". Ninguém rebaixa, nem a IA nem o supervisor. O sistema não aciona ninguém sozinho.
- Toda sugestão e toda correção ficam na **linha do tempo**, que não se apaga.
- Não avalia pessoas: indicadores só por zona e equipe.

### 2ª IA (proposta, branch `proposta-camera`): visão computacional
**Onde:** `camera/contador.py`, no notebook, fora do servidor.
**Qual modelo:** YOLOv8n pré-treinado (Ultralytics, **AGPL-3.0**) + PolygonZone (Roboflow supervision, **MIT**). Não treinamos esse modelo; usamos o pronto, só com a classe "pessoa".
**O que sai:** só números (pessoas por zona). Nenhuma imagem vai para o sistema; no vídeo de saída as pessoas ficam pixeladas.
**Erros da IA:** contagem erra com oclusão e multidão. Por isso exigimos 3 leituras seguidas acima do limite, não duplicamos ocorrência e a câmera só **sugere** (uma pessoa confirma). A câmera não tira a zona do cinza.
**Sensor de fumaça:** **SIMULADO** (botão e script). Usa a mesma regra P1 + brigada.

**Limite (sendo honestos):** a regra simples de palavras já acerta bastante no teste cego. A vantagem da IA aparece com frases variadas e erros de digitação, por isso estamos ampliando as frases de treino.
