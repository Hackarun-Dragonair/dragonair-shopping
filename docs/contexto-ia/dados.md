# Contexto para IA: DADOS (frases de treino da IA)

**Como usar:** copie tudo dentro da caixa abaixo e cole como **primeira mensagem** na sua IA (Gemini, ChatGPT, Claude...). Depois cole também o `docs/contrato.md`. No Cursor não precisa: ele já lê o `AGENTS.md`.

```text
Você vai me ajudar no projeto **Ronda Viva** (hackathon, equipe de 4 alunos iniciantes).
É um sistema web responsivo para shopping: o funcionário lê o QR de uma zona (banheiro, praça, doca...)
e toca OK / Atenção / Problema. Uma IA offline sugere categoria e prioridade (P1 a P4). O mapa fica cinza
quando ninguém conferiu a zona no prazo. Toda ocorrência tem linha do tempo que não pode ser apagada.
Fumaça, fogo, gás, choque ou pessoa presa = P1 + "Avise a brigada pelo rádio", nunca rebaixa.

Tecnologia FIXA: Python + Flask + Jinja2 + SQLite (sqlite3 puro) + Bootstrap 5 local + JavaScript puro + scikit-learn + pytest.
Não sugira outras tecnologias, API paga, React nem banco externo. Não mude a API JSON existente.

Regras:
- Use exatamente os nomes do contrato abaixo. Não invente campos, rotas ou pastas.
- Mexa só nos meus arquivos (lista abaixo).
- A planta do shopping é dado sensível: não use nem peça. O mapa é desenho próprio em blocos.
- Passos pequenos e código simples, com comentários em português, que eu consiga explicar.
- No fim, me diga como testar e um resumo de 3 linhas para eu registrar o uso de IA.

Minha área: DADOS (frases de treino da IA)
Meus arquivos: data/treino.csv, data/teste_cego.csv
Minhas tarefas no quadro: #8 conferir zonas, #9 frases para treinar a IA
Contrato da minha parte: Colunas: frase,categoria,prioridade. Categorias: hidraulica, eletrica, climatizacao, limpeza, seguranca, estrutura. Prioridades: P1, P2, P3, P4. Frases fictícias, sem nome de pessoas nem lojas. Guia: docs/missao-2/guia-dados.md.
```

**Exemplo de pedido depois do contexto:**
> Crie 30 frases curtas, como um funcionário de shopping digitaria no celular com pressa (gírias, sem acento, alguns erros de digitação), no formato frase,categoria,prioridade. Pelo menos 10 de P4 e 10 de P3.

✅ Antes de abrir o PR: rode `python -m pytest` e registre o uso de IA em `docs/IA.md`.
