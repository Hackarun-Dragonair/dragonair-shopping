# Contexto para IA: DADOS (zonas, frases e cor do mapa)

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
- O mapa é um desenho próprio em blocos. Não use nem peça a planta do shopping (dado sensível).
- Passos pequenos e código simples, com comentários em português, que eu consiga explicar.
- No fim, me diga como testar e um resumo de 3 linhas para eu registrar o uso de IA.

Minha área: DADOS (zonas, frases e cor do mapa)
Meus arquivos: dados/zonas.csv, dados/frases.csv, app/status.py, tests/test_dados.py, tests/test_status.py
Minhas tarefas no quadro: #8 lista de zonas, #9 frases para treinar a IA, #10 mapa (com TELAS)
Contrato da minha parte: Colunas e valores permitidos na seção 1 e 2. Só áreas comuns (sem lojas). Frases sem nome de pessoas.
```

**Exemplo de pedido depois do contexto:**
> Estou na tarefa #9. Veja dados/frases.csv e os valores permitidos. Crie mais 30 frases variadas, do jeito que um funcionário escreveria no celular, equilibrando as categorias.

✅ Antes de abrir o PR: rode `pytest -q` e registre o uso de IA em `docs/IA.md`.
