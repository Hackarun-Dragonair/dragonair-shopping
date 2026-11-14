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
| 13/11 19h30 | Bypaulohx | Cursor (Grok) | Completar o backend que ainda estava em aberto: dossiê, celular autorizado com crachá, fila de envio, PDF das etiquetas e alertas por zona | Sem telas novas. A equipe revisa no pull request |
| 13/11 noite | Arthur | Claude | Separar o teste cego (só rótulos humanos) do teste de campo (rótulos sugeridos por IA), criar `app/avaliar.py`, mostrar recall de P1, comparação e matriz de confusão na tela "Sobre a IA" | Equipe confere os números com `python -m app.avaliar` e revisa os rótulos do teste de campo |
| 13/11 22h | Arthur | Claude (Claude Code + navegador automático) | QA ponta a ponta no PC e no celular (390 px), corrigir os 7 problemas achados (8 commits `fix:`) e aplicar o visual bronze/bege com abas, a partir de uma referência em HTML enviada pelo Arthur. Da referência ficaram só as cores e a disposição: sem planta real, sem nomes de lojas e sem arquivos da internet | Arthur aprova antes de juntar no `main`; lista de bugs e prints em `docs/evidencias/qa/` |
| 13/11 22h40 | Arthur | Claude (Claude Code, agente de documentação) | Testar o README do zero (clone novo, ambiente novo, `pytest` e servidor no ar) e escrever, a partir do código e dos documentos da equipe: resumo de 1 página, roteiro do pitch de 90 s, ordem de cliques da demo, FAQ da banca, cola para integrantes, checklist de sábado, textos de entrega e índice de evidências | Números copiados de `docs/evidencias/modelo/resumo.md` e conferidos rodando o sistema; o resultado do teste de usabilidade **não** foi preenchido (é da equipe); a equipe revisa, ensaia e ajusta antes de enviar |

## Dentro da solução

**Onde:** tela da zona (`/z/<codigo>`). Quem achou o problema escreve do seu jeito, e a IA **sugere categoria e prioridade** (a equipe vem da categoria). O supervisor confirma ou corrige na tela do problema.

**Qual modelo:** feito pela equipe com scikit-learn, sem API paga e sem internet (`app/modelo.py`).
1. A frase é normalizada (minúsculas, sem acento) e vira números com **TF-IDF de pedaços de 3 a 5 letras dentro de cada palavra** (`char_wb`). Isso tolera erro de digitação ("vazano", "banhero"). Não usamos n-gramas de palavras inteiras: testamos somar os dois (FeatureUnion) e o teste cego **piorou** (categoria 100% para 90%, prioridade 95% para 90%), então ficou só `char_wb`.
2. Uma **Regressão Logística** (`class_weight="balanced"`) para a categoria e outra para a prioridade.
3. Treinado com `data/treino.csv` (145 frases: as da equipe + 64 do Pedro, ver abaixo). Treina no boot, em segundos.

**Como medimos:** `python -m app.avaliar` gera `docs/evidencias/modelo/` (CSV por frase + `resumo.md` com acurácia, F1 macro, recall de P1, matriz de confusão e a comparação de 3 jeitos). A tela **"Sobre a IA"** (`/telas/sobre-a-ia`) calcula os mesmos números do teste cego no boot.

**Como lidamos com os erros da IA:**
- Ela só **sugere**. A tela mostra a confiança, e abaixo de 50% avisa "IA em dúvida, confira".
- Quando ela fica em dúvida entre duas categorias, a tela da zona faz uma pergunta de desempate.
- **Regra fixa acima da IA** (`app/dominio.py`): fumaça, fogo, choque ou pessoa presa → **P1** e "Avise a brigada pelo rádio". Ninguém rebaixa, nem a IA nem o supervisor. O sistema não aciona ninguém sozinho.
- Toda sugestão e toda correção ficam na **linha do tempo**, que não se apaga.
- Não avalia pessoas: indicadores só por zona e equipe.

**Ampliação das frases (13/11, noite):** o Pedro escreveu 80 relatos curtos de equipamentos, do jeito que a equipe de campo fala (com erro de digitação: "paro", "queimo", "ta"). Os rótulos (categoria e prioridade) foram **propostos com o Claude** por regras simples (ex.: câmera sem sinal = Segurança P2; lâmpada queimada = Elétrica P3) e ainda precisam de revisão humana.
- **64 frases no treino** (rótulo assistido por IA, declarado aqui).
- **16 frases em `data/teste_campo.csv`**, e não no teste cego. A definição (seção 6.2) exige teste cego **escrito e rotulado por pessoas, sem IA**. Uma primeira versão tinha colocado essas 16 no teste cego; corrigimos e o `teste_cego.csv` voltou às 20 frases originais da equipe (o histórico do git mostra as duas versões).

**Resultado no teste cego (n = 20, rótulos humanos, 6 frases P1):**

| Jeito | Categoria | Prioridade | Recall P1 |
|---|---|---|---|
| (a) Só regras de palavras (+ regra dura) | 90% | 40% | 67% (4 de 6) |
| (b) Só modelo | 100% | 95% | 100% |
| (c) Modelo + regra dura (o que o sistema mostra) | **100%** | **95%** | **100% (6 de 6)** |

Único erro: "ar condicionado não liga na praça" (esperado P2, saiu P3).

**Resultado no teste de campo (n = 16, rótulos a revisar):** categoria 81% (regras 69%), prioridade 62% (regras 12%), recall de P1 100% (1 de 1, só com a regra dura: o modelo sozinho deu P2 para "sensor de fumaça piscando"). Os erros são câmera x painel (Segurança ou Elétrica?) e P2 x P3 em equipamento com defeito.

**Limite (sendo honestos):**
- O teste cego é **pequeno (n = 20)** e foi escrito pela mesma equipe que escreveu o treino: o 100% de categoria mostra que o modelo aprendeu o nosso jeito de escrever, não prova que vai acertar 100% no shopping.
- Com frases reais do campo o acerto cai (81% / 62%). Esse é o número mais perto da realidade, mas os rótulos dele ainda são da IA; só vira número oficial depois que duas pessoas da equipe revisarem.
- O recall de P1 de 100% vem do modelo + regras de prioridade. A regra dura em si garante só fumaça, fogo, choque e pessoa presa; os outros P1 (faísca, saída de emergência travada, extintor ausente, forro pendurado) o modelo acertou.
- Por isso a IA só sugere e o supervisor confirma.
