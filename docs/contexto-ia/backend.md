# Contexto para IA: BACKEND (servidor Flask e banco)

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

Minha área: BACKEND (servidor Flask e banco)
Meus arquivos: wsgi.py, app/__init__.py, app/rotas/*.py (menos telas.py), app/db.py, app/servico.py, app/consultas.py, app/seed.py, tests/test_fluxo.py
Minhas tarefas no quadro: #2 base, #3 tela /z/<codigo>, #11 fila, #12 linha do tempo
Contrato da minha parte: A API devolve JSON e as telas dependem dela: não mude nomes de campos. Eventos só são inseridos, nunca alterados.
```

**Exemplo de pedido depois do contexto:**
> Leia app/rotas/problemas.py e app/servico.py. Quero entender, em passos simples, o que acontece do momento em que alguém registra um problema até ele ser resolvido, para eu explicar à banca.

✅ Antes de abrir o PR: rode `python -m pytest` e registre o uso de IA em `docs/IA.md`.
