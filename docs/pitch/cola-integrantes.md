# Cola para quem não programou (1 página)

A banca pode perguntar para **qualquer** integrante. Leia isto 2 vezes e treine as 5 respostas do fim em voz alta.

## O sistema em 6 passos
1. **Cada área do shopping é uma "zona"** e tem um **QR** colado sempre no mesmo tipo de lugar.
2. O funcionário lê o QR com o celular (sem instalar nada, sem senha) e toca **OK, Atenção ou Problema**.
3. No **Problema**, escreve do jeito dele. A **IA sugere** a categoria (ex.: Elétrica) e a prioridade (P1 a P4), e a pessoa pode mudar.
4. Se a frase tem **fumaça, fogo, choque ou pessoa presa**, vira **P1** e aparece **"Avise a brigada pelo rádio"**. Ninguém baixa essa prioridade.
5. O **gestor** entra com crachá e **confirma**. A ocorrência vai para a **fila** da equipe certa: Aberto → Em atendimento → Resolvido. Cada passo entra numa **linha do tempo que não se apaga**.
6. O **mapa** mostra cada zona com uma cor. **Cinza = ninguém conferiu no prazo.** O **painel** mostra os números por zona e equipe, nunca por pessoa.

## Onde fica cada parte
| Pasta ou arquivo | O que faz (em palavras simples) |
|---|---|
| `wsgi.py` | O "botão de ligar" do sistema |
| `app/rotas/` | Os endereços do site: o que acontece quando alguém abre uma página ou clica num botão |
| `app/templates/` | O desenho de cada tela (HTML) |
| `app/static/` | Cores, estilos e o JavaScript que faz os botões funcionarem sem recarregar |
| `app/dominio.py` | As **regras**: palavra de risco vira P1, cor da zona, categorias |
| `app/modelo.py` | A **IA**: aprende com as frases e faz a sugestão |
| `app/avaliar.py` | Mede a IA e escreve o relatório em `docs/evidencias/modelo/` |
| `app/db.py`, `servico.py`, `consultas.py` | O banco de dados: guardar e buscar zonas, conferências, problemas e a linha do tempo |
| `app/seed.py` | Os **dados de exemplo** fictícios (11 zonas, crachás OTTO, LIA, RITA, CAIO) |
| `data/treino.csv` | As 145 frases que ensinam a IA |
| `data/teste_cego.csv` | 20 frases separadas, que a IA nunca viu, para medir o acerto |
| `tests/` | 77 testes automáticos que conferem se tudo continua funcionando |
| `docs/` | Documentos, evidências e declaração de uso de IA |

## Como a IA funciona (comparação do dia a dia)
- **Pedaços de letras (TF-IDF):** a IA não lê a palavra inteira. Ela quebra em pedacinhos de 3 a 5 letras. "vazando" vira "vaz", "aza", "zan", "and"... Por isso ela entende "vazano" (com erro de digitação): os pedaços são quase os mesmos. Pedaços que aparecem em todas as frases (como "do", "no") contam pouco; pedaços raros e típicos contam mais.
- **Regressão logística:** é como uma **balança com pesos**. Cada pedaço puxa um pouco para uma categoria: "vaz" puxa para Hidráulica, "lamp" para Elétrica. Ela soma tudo e a categoria mais pesada ganha. A **confiança** é o quanto ela ganhou com folga.
- **Treino:** ela aprendeu esses pesos olhando as 145 frases de exemplo, já com a resposta certa. Treina em segundos, toda vez que o sistema liga.
- Roda **dentro do nosso servidor**, sem internet e sem pagar nada por uso.

## Como medimos (e o limite)
- **Teste cego:** 20 frases escritas e rotuladas à mão pela equipe, **guardadas fora do treino**. É como prova com questões que o aluno nunca viu. Resultado: **100%** na categoria, **95%** na prioridade.
- **Recall de P1:** dos casos que eram P1 de verdade, quantos o sistema marcou P1. Resultado: **6 de 6**. Só com regras de palavras seriam 4 de 6.
- **Teste de campo:** 16 frases reais, do jeito que a equipe de campo escreve. Cai para **81%** e **62%**. Os rótulos dessas frases ainda precisam ser revisados por pessoas.
- **Limite:** o teste cego é pequeno e foi escrito por nós. O 100% não é garantia no shopping de verdade. **Por isso a IA só sugere e o gestor confirma.**

## A regra que ninguém quebra
Fumaça, fogo, choque ou pessoa presa → **P1** + "Avise a brigada pelo rádio".
- A IA não consegue baixar. O gestor tenta P3 e o sistema responde "Prioridade mantida em P1".
- O sistema **não chama ninguém sozinho**: quem decide é a brigada.

## As 5 perguntas mais prováveis
1. **"Qual o diferencial?"** — Mostra o que **não** aconteceu: a zona cinza é onde ninguém olhou. Folha de papel e checklist só mostram o que foi feito.
2. **"A IA acerta quanto?"** — No teste cego de 20 frases, 100% na categoria e todos os 6 casos de risco. Com frases reais, 81%. O teste é pequeno, então ela só sugere e o gestor confirma.
3. **"E se a IA errar?"** — A pessoa corrige na hora, o gestor confirma, e a correção fica na linha do tempo. Abaixo de 50% de confiança, a tela pergunta "É mais X ou Y?" com dois botões quando ela fica entre duas categorias; sem segunda opção, avisa "IA em dúvida, confira". Isso acontece na maioria das vezes, então a pessoa sempre confere.
4. **"Vocês vigiam o funcionário?"** — Não. Tudo é por zona e equipe, nunca por pessoa. Os nomes da demo são inventados.
5. **"Funciona sem internet?"** — Sim, num notebook com rede local: a IA está dentro do sistema. Só o celular precisa estar na mesma rede (pode ser o hotspot).

Pergunta que você não sabe? Diga: **"Boa pergunta. Quem pode detalhar é ___ , mas o princípio é: a IA sugere, a pessoa decide, e tudo fica registrado."**
