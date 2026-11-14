# Avaliação do modelo (gerado por `python -m app.avaliar`)

Modelo: TF-IDF de pedaços de palavra (char_wb, 3 a 5 letras) + Regressão Logística. Treinado com 145 frases de `data/treino.csv`. Nenhuma frase de teste entra no treino.

## Teste cego (número oficial)

`data/teste_cego.csv`: frases escritas e rotuladas à mão pela equipe, sem IA. É o número que vai para a tela e para o pitch. n pequeno: ler como indicação, não como garantia.

- **n = 20** frases (detalhe por frase: `avaliacao_teste_cego.csv`)
- Acurácia categoria: **100%** (F1 macro 1.00)
- Acurácia prioridade: **95%** (F1 macro 0.94)
- Recall de P1: **100%** (6 de 6 P1)

### Comparação

| Jeito | Categoria | Prioridade | Recall P1 |
|---|---|---|---|
| Só regras de palavras | 90% | 40% | 67% |
| Só modelo | 100% | 95% | 100% |
| Modelo + regra dura | 100% | 95% | 100% |

(a) só regras: palavras-chave para categoria e prioridade + regra dura de risco, sem modelo. (b) só modelo: o que o modelo previu, sem regra nenhuma. (c) modelo + regra dura: o que o sistema mostra (`triar`); a prioridade nunca fica abaixo da regra.

### Matriz de confusão da categoria (sistema final)

Linha = rótulo esperado; coluna = previsto.

| Esperado \ Previsto | Hidráulica | Elétrica | Climatização | Limpeza | Segurança | Estrutura |
|---|---|---|---|---|---|---|
| Hidráulica | 3 | 0 | 0 | 0 | 0 | 0 |
| Elétrica | 0 | 3 | 0 | 0 | 0 | 0 |
| Climatização | 0 | 0 | 3 | 0 | 0 | 0 |
| Limpeza | 0 | 0 | 0 | 3 | 0 | 0 |
| Segurança | 0 | 0 | 0 | 0 | 5 | 0 |
| Estrutura | 0 | 0 | 0 | 0 | 0 | 3 |

### Erros do sistema final

- "ar condicionado nao liga na praca": esperado climatizacao/P2, previsto climatizacao/P3

## Teste de campo (rótulos a revisar)

`data/teste_campo.csv`: **rótulos a revisar.** Frases reais do jeito que a equipe de campo escreve (Pedro), mas a categoria e a prioridade foram **sugeridas por IA** e ainda não foram revisadas por duas pessoas. Não conta como teste cego; serve para ver onde o modelo sofre com linguagem real.

- **n = 16** frases (detalhe por frase: `avaliacao_teste_campo.csv`)
- Acurácia categoria: **81%** (F1 macro 0.81)
- Acurácia prioridade: **62%** (F1 macro 0.56)
- Recall de P1: **100%** (1 de 1 P1)

### Comparação

| Jeito | Categoria | Prioridade | Recall P1 |
|---|---|---|---|
| Só regras de palavras | 69% | 12% | 100% |
| Só modelo | 81% | 56% | 0% |
| Modelo + regra dura | 81% | 62% | 100% |

(a) só regras: palavras-chave para categoria e prioridade + regra dura de risco, sem modelo. (b) só modelo: o que o modelo previu, sem regra nenhuma. (c) modelo + regra dura: o que o sistema mostra (`triar`); a prioridade nunca fica abaixo da regra.

### Matriz de confusão da categoria (sistema final)

Linha = rótulo esperado; coluna = previsto.

| Esperado \ Previsto | Hidráulica | Elétrica | Climatização | Limpeza | Segurança | Estrutura |
|---|---|---|---|---|---|---|
| Hidráulica | 0 | 0 | 0 | 0 | 0 | 0 |
| Elétrica | 0 | 8 | 0 | 0 | 1 | 0 |
| Climatização | 0 | 0 | 0 | 0 | 0 | 0 |
| Limpeza | 0 | 0 | 0 | 0 | 0 | 0 |
| Segurança | 0 | 2 | 0 | 0 | 5 | 0 |
| Estrutura | 0 | 0 | 0 | 0 | 0 | 0 |

### Erros do sistema final

- "Painel digital do estacionamento apago o visor e nao mostra os numero.": esperado eletrica/P3, previsto eletrica/P2
- "Fita de led da sanca ta com metade dos ponto queimado e a outra metade piscando.": esperado eletrica/P4, previsto eletrica/P3
- "Camera do corredor do cinema fico girando sem parar e nao obedece comando.": esperado seguranca/P3, previsto eletrica/P2
- "Sensor de fumaca ta com a luzinha piscando rapido e dando erro no painel.": esperado seguranca/P1, previsto eletrica/P1
- "Painel de senha apago o visor e saiu da rede do sistema.": esperado eletrica/P3, previsto eletrica/P2
- "Camera 11 ta com a imagem chuviscando muito e falhando o video.": esperado seguranca/P3, previsto seguranca/P2
- "Painel informativo travo numa tela branca e perdeu o sinal.": esperado eletrica/P3, previsto seguranca/P2
