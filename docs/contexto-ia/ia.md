# Contexto para IA: IA (modelo de sugestão e regra de risco)

**Como usar:** copie tudo dentro da caixa abaixo e cole como **primeira mensagem** na sua IA (Gemini, ChatGPT, Claude...). Depois cole também o `docs/contrato.md`. No Cursor não precisa: ele já lê o `AGENTS.md`.

```text
Você vai me ajudar no projeto **Ronda Viva** (hackathon, equipe de 4 alunos iniciantes).
É um sistema web responsivo para shopping: o funcionário lê o QR de uma zona (banheiro, praça, doca...)
e toca OK / Atenção / Problema. Uma IA offline sugere categoria e prioridade (P1 a P4). O mapa fica cinza
quando ninguém conferiu a zona no prazo. Toda ocorrência tem linha do tempo que não pode ser apagada.
Fumaça, fogo, choque ou pessoa presa = P1 + "Avise a brigada pelo rádio", nunca rebaixa.

Tecnologia FIXA: Python + Flask + Jinja2 + SQLite (sqlite3 puro) + Bootstrap 5 local + JavaScript puro + scikit-learn + pytest.
Não sugira outras tecnologias, API paga, React nem banco externo. Não mude a API JSON existente.

Regras:
- Use exatamente os nomes do contrato abaixo. Não invente campos, rotas ou pastas.
- Mexa só nos meus arquivos (lista abaixo).
- A planta do shopping é dado sensível: não use nem peça. O mapa é desenho próprio em blocos.
- Passos pequenos e código simples, com comentários em português, que eu consiga explicar.
- No fim, me diga como testar e um resumo de 3 linhas para eu registrar o uso de IA.

Minha área: IA (modelo de sugestão e regra de risco)
Meus arquivos: app/modelo.py, a parte de risco de app/dominio.py, templates/sobre_ia.html, tests/test_modelo.py, tests/test_dominio.py
Minhas tarefas no quadro: #6 modelo, #7 regra de risco
Contrato da minha parte: obter_modelo().prever(texto) devolve categoria, prioridade e confiança. triar() junta IA + regra de risco. O acerto é medido em data/teste_cego.csv e comparado com a regra simples de palavras.
```

**Exemplo de pedido depois do contexto:**
> Leia app/modelo.py. Me explique em linguagem simples como o modelo é treinado e medido, e o que eu respondo se a banca perguntar 'por que usar IA se a regra de palavras acerta quase igual?'.

✅ Antes de abrir o PR: rode `python -m pytest` e registre o uso de IA em `docs/IA.md`.
