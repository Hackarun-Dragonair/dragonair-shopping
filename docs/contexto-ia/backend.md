# Contexto para IA: BACKEND (servidor e banco)

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

Minha área: BACKEND (servidor e banco)
Meus arquivos: app/main.py, app/banco.py, tests/test_app.py
Minhas tarefas no quadro: #2 esqueleto, #3 tela /z/{zona}, #11 fila, #12 linha do tempo + dossiê
Contrato da minha parte: Rotas da seção 5 e tabelas da seção 3. Chame a IA só por `sugerir(texto)` de ia/modelo.py.
```

**Exemplo de pedido depois do contexto:**
> Estou na tarefa #3. Leia app/main.py. Quero que, ao salvar com status diferente de ok, crie a ocorrência usando sugerir(texto) e grave o evento 'criada'. Faça em passos pequenos.

✅ Antes de abrir o PR: rode `pytest -q` e registre o uso de IA em `docs/IA.md`.
