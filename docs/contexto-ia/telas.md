# Contexto para IA: TELAS (front-end e responsividade)

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

Minha área: TELAS (front-end e responsividade)
Meus arquivos: app/templates/*.html, app/static/css/ronda.css, app/static/js/*.js, app/rotas/telas.py, tests/test_telas.py
Minhas tarefas no quadro: #4 visual das telas, #5 responsividade no celular (requisito da roleta!), #10 mapa
Contrato da minha parte: As telas leem os dados pela API JSON (fetch com Accept: application/json) ou pelas funções de app/consultas.py. Cores da zona: ok, atencao, problema, cinza. Celular primeiro. Bootstrap já está em app/static/vendor (sem CDN).
```

**Exemplo de pedido depois do contexto:**
> Leia app/templates/base.html e app/static/css/ronda.css. Quero deixar o mapa (templates/inicio.html) mais bonito no celular, mantendo os blocos e as cores. Faça uma mudança pequena de cada vez.

✅ Antes de abrir o PR: rode `python -m pytest` e registre o uso de IA em `docs/IA.md`.
