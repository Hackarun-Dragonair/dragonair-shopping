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
| 13/11 13h | Arthur | Claude | Montar o quadro de tarefas, o contrato de nomes, a estrutura de pastas com esqueleto que roda, os testes automáticos e os contextos de IA por área | Arthur definiu a divisão; cada área revisa e completa os TODO das suas tarefas |
| 13/11 14h | Arthur | Claude | Implementar a IA da solução (#6 e #7): treino, sugestão, regra de risco, tela "Sobre a IA" e testes | Arthur revisa e ensaia a explicação abaixo antes de juntar na main |
| | | | | |

## Dentro da solução

**Onde:** tela da zona (`/z/{id}`). Enquanto a pessoa escreve o que viu, a IA sugere **categoria, prioridade e equipe**. Quem decide é o supervisor.

**Qual modelo:** feito pela equipe com scikit-learn, sem API paga e sem internet.
1. A frase vira números com **TF-IDF**: palavras inteiras + pedaços de 3 a 5 letras (ajuda com erro de digitação).
2. Uma **Regressão Logística** por campo aprende quais palavras indicam cada valor.
3. Treinado com `dados/frases.csv` (frases **fictícias** escritas pela equipe). Código: `ia/treinar.py` e `ia/modelo.py`.

**Como medimos:** validação cruzada: o modelo é testado em frases que ficaram fora do treino, em várias rodadas. A tela **"Sobre a IA"** mostra o acerto nelas, ao lado de um "chute" que sempre responde o valor mais comum. Os números são reais, calculados toda vez que o modelo treina.

**Como lidamos com os erros da IA:**
- Ela só **sugere**. Nunca fecha ocorrência nem decide sozinha.
- Mostra a **confiança**. Abaixo de 50%, a tela avisa "IA em dúvida, confira".
- **Regra fixa acima da IA:** palavras de risco (fumaça, fogo, choque, pessoa presa, gás...) deixam a prioridade **urgente** e mostram **"Avise a brigada pelo rádio"**, mesmo se o modelo errar. Testado em `tests/test_risco.py`.
- Não avalia pessoas: indicadores só por zona e equipe.

**Limites (sendo honestos):** com poucas frases o acerto é baixo. Ele melhora com mais exemplos e, no uso real, as correções do supervisor viram novos dados de treino.
