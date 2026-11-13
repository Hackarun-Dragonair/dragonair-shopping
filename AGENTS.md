# Contexto do projeto para qualquer IA (Cursor, Claude, Gemini, ChatGPT...)

> O Cursor lê este arquivo sozinho. Em IA de site (Gemini, ChatGPT), cole o arquivo da sua área em `docs/contexto-ia/`.

## O projeto
**Ronda Viva**: sistema web responsivo para shopping. Equipe Dragonair, HackaRun 2026, Desafio 09 (eficiência operacional).
- O funcionário lê o QR da zona e toca **OK / Atenção / Problema**.
- Uma IA offline sugere categoria e prioridade. O supervisor confirma.
- O mapa fica **cinza** quando ninguém conferiu a zona no prazo.
- Toda ocorrência tem uma **linha do tempo** que não pode ser apagada.
- Fumaça, fogo, choque ou pessoa presa → **P1** e **"Avise a brigada pelo rádio"**. Nunca rebaixa; o sistema nunca chama ninguém sozinho.
- Indicadores por zona e equipe, **nunca por pessoa**.

## Tecnologia (não trocar)
Python 3.11+ · **Flask** · Jinja2 · SQLite (`sqlite3` puro, sem ORM) · Bootstrap 5 local em `app/static/vendor` · JavaScript puro (`fetch`) · scikit-learn · pytest.
**Sem** API paga, sem React, sem banco externo. Biblioteca nova só se a equipe combinar.

## Estrutura (não criar pastas novas)
```
wsgi.py                 liga o servidor                       BACKEND
app/__init__.py         cria o app e semeia dados             BACKEND
app/rotas/*.py          API JSON (zona, problemas, mapa...)   BACKEND
app/rotas/telas.py      telas HTML (fila, painel, IA)         TELAS
app/dominio.py          regras (risco, cor da zona)           BACKEND + IA
app/modelo.py           IA (treino e previsão)                IA
app/db.py, servico.py, consultas.py, seed.py   banco e dados  BACKEND
app/templates/*.html    telas                                 TELAS
app/static/css|js       visual e JavaScript                   TELAS
data/*.csv              frases de treino e teste cego         DADOS
tests/test_*.py         testes                                cada área
docs/                   documentos                            todos
```

## Regras para a IA seguir
1. Siga **`docs/contrato.md`**: nomes, valores, rotas e funções. Não invente nomes novos.
2. Mexa **só nos arquivos da tarefa** pedida. Não reescreva arquivos inteiros de outra área.
3. **Não mude a API JSON** (as telas e os testes dependem dela). Tela nova = template + rota em `app/rotas/telas.py`.
4. Mudanças **pequenas**. Código simples que um aluno do 1º período consiga explicar para a banca.
5. Nomes de variáveis e comentários **em português**.
6. Depois de mudar, rode `python -m pytest`. Tudo precisa passar.
7. Nunca coloque senha, chave de API ou dado pessoal no código.
8. **Planta do shopping é dado sensível:** não usar imagem, PDF nem posições copiadas dela. Nunca cole a planta numa IA.
9. Explique em 3 linhas o que o código faz, para a pessoa registrar em `docs/IA.md`.

## Como rodar
```bash
pip install -r requirements.txt
python wsgi.py              # abre em http://127.0.0.1:8000
python -m pytest            # testes
```
