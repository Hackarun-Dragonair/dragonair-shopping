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
| 13/11 22h40–23h45 | Arthur | Claude (Claude Code, agentes construtores) | Pergunta de desempate quando a IA fica entre duas categorias ("É mais X ou Y?", só preenche categoria e equipe; a regra P1 continua no servidor); fila e quadro do mapa a cada 5 s; prova do QR de verdade (PDF de etiquetas do site no ar lido por imagem: 11/11 zonas certas, sem login) e correção do desenho do QR | Cada ramo passou por um agente revisor independente (testes, navegador em 1366 e 390 px, regras do contrato) antes de entrar no `main`; Arthur definiu o escopo e as regras |
| 13/11 22h40–23h45 | Arthur | Claude (Claude Code, 2 agentes revisores) | Revisar o QA/visual e depois a integração da noite: código, testes (73), navegador, QR e documentação | Os achados viraram commits `fix:`/`docs:`; nada entrou no `main` sem veredito "APROVADO" |
| 14/11 0h–0h35 | Arthur | Claude (Claude Code, agente construtor + agente revisor) | Mapa com zonas em polígono (formas irregulares) e os 4 pisos redesenhados do ZERO como shopping genérico (fachada curva, átrio, âncoras, praça em leque, rampa), com nomes fictícios; letras maiores e nomes curtos no celular | O revisor comparou por programa as coordenadas com o HTML de referência (nenhuma cópia), conferiu 4 pisos em 1366/390 px e o modo planta; teste garante as 11 zonas e nenhuma marca real |
| 14/11 madrugada | Arthur | Claude (Claude Code, agente de vídeo) | Montar o vídeo do pitch: gravação automatizada da tela do app real (o sistema funcionando de verdade, sem montagem), cartelas, legendas e uma voz sintética usada **só como guia de tempo e plano B** | A voz final será humana, gravada pela equipe no sábado (se não der tempo, vai a voz sintética e isso fica declarado aqui). A equipe confere se cada tela mostrada existe e funciona no app |
| 14/11 madrugada | Arthur | Claude (Claude Code, agentes de "banca simulada" + agente construtor + agente revisor) | Bancas simuladas avaliaram o vídeo, os documentos e o código como fariam os avaliadores. A partir delas: teste de usabilidade marcado como pendente até ser feito, limites da IA explicados com números medidos (confiança, teste cego usado na escolha do modelo), FAQ com as perguntas mais duras e limite de 9 MB no envio de arquivos (`fix:`) | Cada correção passou por um agente revisor antes de entrar no `main`, dentro das regras que o Arthur definiu para a noite (ramo separado, testes verdes, revisor aprova); a equipe revisa no sábado. A regra de risco e o contrato **não** foram mudados: isso é decisão da equipe |
| 14/11 manhã | Arthur | Claude (Claude Code) | Ajustar a entrega às instruções finais da organização: resumo de 1 página nos 8 tópicos (`RESUMO.md` + `RESUMO.pdf`), seção de arquitetura no README, guia do vídeo e checklist | **O vídeo de 90 s montado por agentes na madrugada NÃO será entregue:** a organização proibiu vídeo produzido com IA. O vídeo oficial é gravado por um integrante, com as próprias palavras (`docs/pitch/video-90s.md` traz só tópicos) |
| 14/11 manhã | Arthur | Claude (Claude Code + 2 agentes de banca simulada) | Revisar o resumo de 1 página (a equipe copia à mão) e escrever um roteiro-base para o vídeo de 90 s; a banca apontou exageros (ex.: "manda avisar a brigada" → o sistema só pede na tela) e textos longos | O **vídeo é gravado por um integrante, com as próprias palavras** (o roteiro é só base de treino, sem leitura); nenhuma parte do vídeo é produzida com IA. O resumo à mão é escrito pela equipe a partir de `docs/RESUMO.md` |

## Dentro da solução

**Onde:** tela da zona (`/z/<codigo>`). Quem achou o problema escreve do seu jeito, e a IA **sugere categoria e prioridade** (a equipe vem da categoria). O supervisor confirma ou corrige na tela do problema.

**Qual modelo:** feito pela equipe com scikit-learn, sem API paga e sem internet (`app/modelo.py`).
1. A frase é normalizada (minúsculas, sem acento) e vira números com **TF-IDF de pedaços de 3 a 5 letras dentro de cada palavra** (`char_wb`). Isso tolera erro de digitação ("vazano", "banhero"). Não usamos n-gramas de palavras inteiras: testamos somar os dois (FeatureUnion) e o teste cego **piorou** (categoria 100% para 90%, prioridade 95% para 90%), então ficou só `char_wb`.
2. Uma **Regressão Logística** (`class_weight="balanced"`) para a categoria e outra para a prioridade.
3. Treinado com `data/treino.csv` (145 frases: as da equipe + 64 do Pedro, ver abaixo). Treina no boot, em segundos.

**Como medimos:** `python -m app.avaliar` gera `docs/evidencias/modelo/` (CSV por frase + `resumo.md` com acurácia, F1 macro, recall de P1, matriz de confusão e a comparação de 3 jeitos). A tela **"Sobre a IA"** (`/telas/sobre-a-ia`) calcula os mesmos números do teste cego no boot.

**Como lidamos com os erros da IA:**
- Ela só **sugere**. A tela mostra a confiança, e abaixo de 50% avisa "IA em dúvida, confira". Esse aviso **aparece na maioria das vezes**, não só em casos raros (ver "Limite" abaixo). Por isso a pessoa e o gestor sempre conferem.
- Quando ela fica em dúvida entre duas categorias, a tela da zona faz uma pergunta de desempate.
- **Regra fixa acima da IA** (`app/dominio.py`): fumaça, fogo, gás, choque ou pessoa presa → **P1** e "Avise a brigada pelo rádio". Ninguém rebaixa, nem a IA nem o supervisor. O sistema não aciona ninguém sozinho.
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
- O teste cego também foi usado para **escolher entre duas versões** do modelo (a versão com FeatureUnion foi descartada porque piorou nele). E algumas frases dele são **parecidas com frases do treino** (ex.: "pessoa presa dentro do elevador" no teste e "pessoa presa no elevador" no treino). As duas coisas deixam o 100% mais otimista do que a realidade.
- Por isso o número **mais perto do real é o do teste de campo**: 81% de categoria e 62% de prioridade, com rótulos ainda a revisar. Próximo passo: validação cruzada (dividir o treino em partes e testar cada parte com o resto) e um teste novo escrito por pessoas de fora, que não viram o treino.
- **A confiança costuma ficar abaixo de 50%.** Medimos (14/11, `obter_modelo().prever` em cada frase): no teste cego, 16 de 20 frases ficaram abaixo de 50%; no teste de campo, 13 de 16. A média foi 37% nos dois (com 6 categorias, um chute daria 17%). É natural com 145 frases de treino. Na prática, o aviso de dúvida aparece quase sempre, e a pessoa confirma a categoria com um toque. Calibrar a confiança é próximo passo.
- **Onde a IA mais ajuda é na prioridade**, não na categoria. Comparando com as palavras-chave sozinhas: no teste cego, prioridade 95% contra 40%; no campo, 62% contra 12%. Na categoria a diferença é menor (100% contra 90%; 81% contra 69%).
- O recall de P1 de 100% vem do modelo + regras de prioridade. A regra dura em si garante só fumaça, fogo, gás, choque e pessoa presa; os outros P1 (faísca, saída de emergência travada, extintor ausente, forro pendurado) o modelo acertou.
- Por isso a IA só sugere e o supervisor confirma.
