# Contexto para IA: IA (modelo de sugestão e risco)

**Como usar:** copie tudo dentro da caixa abaixo e cole como **primeira mensagem** na sua IA (Gemini, ChatGPT, Claude...). Depois cole também o `docs/contrato.md`. No Cursor não precisa: ele já lê o `AGENTS.md`.

```text
Você vai me ajudar no projeto **Ronda Viva** (hackathon, equipe de 4 alunos iniciantes).
É um sistema web responsivo para shopping: o funcionário lê o QR de uma zona (banheiro, praça, doca...)
e toca OK / Atenção / Problema. Uma IA offline sugere categoria, prioridade e equipe. O mapa fica cinza
quando ninguém conferiu a zona no prazo. Toda ocorrência tem linha do tempo que não pode ser apagada.

Tecnologia FIXA: Python + FastAPI + Jinja2 + SQLite (sqlite3 puro) + Bootstrap 5 local + scikit-learn + pytest.
Não sugira outras tecnologias, API paga, login, React nem banco externo.

Regras:
- Use exatamente os nomes do contrato abaixo. Não invente campos, rotas ou pastas.
- Mexa só nos meus arquivos (lista abaixo).
- Passos pequenos e código simples, com comentários em português, que eu consiga explicar.
- No fim, me diga como testar e um resumo de 3 linhas para eu registrar o uso de IA.

Minha área: IA (modelo de sugestão e risco)
Meus arquivos: ia/modelo.py, ia/risco.py, ia/treinar.py, tests/test_risco.py
Minhas tarefas no quadro: #6 modelo que sugere categoria/prioridade/equipe, #7 palavras de risco
Contrato da minha parte: Função `sugerir(texto) -> dict` com as chaves categoria, prioridade, equipe, confianca, risco, aviso (seção 4). Treino com dados/frases.csv. Risco nunca baixa prioridade.
```

**Exemplo de pedido depois do contexto:**
> Estou na tarefa #7. Leia ia/risco.py e tests/test_risco.py. Implemente detectar_risco ignorando maiúsculas e acentos, e me diga qual linha apagar no teste.

✅ Antes de abrir o PR: rode `pytest -q` e registre o uso de IA em `docs/IA.md`.
