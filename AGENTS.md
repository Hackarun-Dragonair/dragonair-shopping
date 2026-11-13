# Contexto do projeto para qualquer IA (Cursor, Claude, Gemini, ChatGPT...)

> Cursor lê este arquivo sozinho. Em IA de site (Gemini, ChatGPT), cole o arquivo da sua área em `docs/contexto-ia/`.

## O projeto
**Ronda Viva**: sistema web responsivo para o shopping. Equipe Dragonair, HackaRun 2026, Desafio 09 (eficiência operacional).
- Funcionário lê o QR da zona e toca **OK / Atenção / Problema**.
- Uma IA offline sugere categoria, prioridade e equipe. O supervisor confirma.
- O mapa fica **cinza** quando ninguém conferiu a zona no prazo.
- Toda ocorrência tem uma **linha do tempo** que não pode ser apagada.
- Palavras de risco (fumaça, fogo, choque...) mostram **"Avise a brigada pelo rádio"**. A prioridade nunca baixa e o sistema nunca chama ninguém sozinho.
- Indicadores por zona e equipe, **nunca por pessoa**.

## Tecnologia (não trocar)
Python 3.10+ · FastAPI · Jinja2 · SQLite (`sqlite3` puro, sem ORM) · Bootstrap 5 local em `app/static/vendor` · scikit-learn · pytest.
**Sem** API paga, sem login, sem React, sem banco externo. Biblioteca nova só se a equipe combinar.

## Estrutura (não criar pastas novas)
```
app/main.py          rotas                       BACKEND
app/banco.py         tabelas SQLite              BACKEND
app/status.py        cor da zona no mapa         DADOS + TELAS
app/templates/*.html telas                       TELAS
app/static/css|js    estilo e JS                 TELAS
ia/                  modelo, risco, treino       IA
dados/*.csv          zonas e frases              DADOS
tests/test_*.py      um teste por área           cada área
docs/                documentos                  todos
```

## Regras para a IA seguir
1. Siga **`docs/contrato.md`**: nomes de campos, valores, rotas e funções. Não invente nomes novos.
2. Mexa **só nos arquivos da tarefa** pedida. Não reescreva arquivos inteiros de outra área.
3. Mudanças **pequenas**. Código simples que um aluno do 1º período consiga explicar para a banca.
4. Nomes de variáveis e comentários **em português**.
5. Depois de mudar, rode `pytest -q`. Tudo precisa passar.
6. Nunca coloque senha, chave de API, dado pessoal ou imagem da planta do shopping no código.
7. Explique em 3 linhas o que o código faz, para a pessoa registrar em `docs/IA.md`.

## Como rodar
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0    # abre em http://localhost:8000
pytest -q                                        # testes
```
