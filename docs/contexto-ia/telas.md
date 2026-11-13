# Contexto para IA: TELAS (front-end e responsividade)

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

Minha área: TELAS (front-end e responsividade)
Meus arquivos: app/templates/*.html, app/static/css/ronda.css, app/static/js/ronda.js
Minhas tarefas no quadro: #4 protótipo → templates, #5 responsividade (requisito da roleta!), #10 mapa (com DADOS)
Contrato da minha parte: Telas usam Bootstrap 5 que já está em app/static/vendor (sem CDN). Cores do mapa: verde, amarelo, vermelho, cinza. Celular primeiro.
```

**Exemplo de pedido depois do contexto:**
> Estou na tarefa #4. Vou colar o HTML do protótipo (sem as imagens piso1/piso2) e o app/templates/base.html. Quero transformar as telas num template Jinja que estende base.html, sem números fixos e sem as imagens da planta.

✅ Antes de abrir o PR: rode `pytest -q` e registre o uso de IA em `docs/IA.md`.
