# 🐉 Dragonair Shopping — HackaRun 2026

> Equipe **Dragonair** · Desafio **09: Eficiência operacional e infraestrutura** · UniCatólica, 12 a 14/11/2026

**O problema:** um shopping precisa acompanhar as condições dos ambientes, identificar ocorrências, organizar atividades operacionais e garantir que os serviços não parem. ([texto oficial](docs/desafio.md))

**Nossa solução: Ronda Viva** — *"Mostra o que ninguém conferiu. Registra que cuidou."* Sistema web responsivo que mostra quais ambientes ninguém conferiu, usa uma IA treinada pela equipe (offline) para classificar e encaminhar cada problema achado na ronda, e registra cada passo numa linha do tempo.

📌 **Entrega 1 — Planejamento técnico: [`docs/missao-1/ENTREGA-1.md`](docs/missao-1/ENTREGA-1.md)**

➡️ Planejamento detalhado: [`docs/missao-1/README.md`](docs/missao-1/README.md) · Pitch e perguntas difíceis: [`docs/missao-1/pitch-e-faq.md`](docs/missao-1/pitch-e-faq.md)

---

## 🧭 Comece aqui (para todos)

**Você NÃO precisa saber Git para ajudar.** Quase tudo dá para fazer pelo site do GitHub.

| Quero... | Onde / como |
|---|---|
| Dar opinião sobre a ideia | Aba **Issues** → abrir a issue → escrever no campo de comentário no fim da página → **Comment** |
| Ver o que cada um está fazendo | Aba **Issues** (cada tarefa é uma issue, com o nome de quem pegou) |
| Escrever um texto da Missão 1 | Abrir o arquivo em `docs/missao-1/` → ícone de **lápis ✏️** → escrever → **Commit changes** |
| Subir foto ou print (evidência) | Entrar na pasta `docs/evidencias/` → **Add file** → **Upload files** → arrastar → **Commit changes** |
| Registrar que usei IA | Editar `docs/IA.md` (lápis ✏️) e adicionar uma linha na tabela |

### 📖 Mini-dicionário
- **Repositório (repo):** a "pasta do projeto" na nuvem. É este aqui.
- **Commit:** salvar uma alteração com uma frase explicando o que mudou.
- **Issue:** um tópico de conversa ou uma tarefa (como um post com comentários).
- **Branch:** uma cópia de trabalho para mexer no código sem quebrar a versão principal (`main`).
- **Pull Request (PR):** pedido para juntar sua branch na `main`. Outra pessoa revisa antes.

### ✍️ Como escrever a mensagem do commit
Comece com o tipo e diga o que mudou:
- `docs: escreve proposta de valor` · `feat: tela de nova ocorrência` · `fix: corrige erro ao salvar`
- ❌ Evite: `ajustes`, `teste`, `final2` — a banca olha o histórico.

---

## 📁 O que tem em cada pasta

```
README.md              ← você está aqui (guia da equipe)
AGENTS.md              ← contexto do projeto para qualquer IA (Cursor lê sozinho)
wsgi.py                ← liga o servidor Flask (python wsgi.py)
app/
  __init__.py          ← cria o app Flask e semeia os dados de exemplo
  rotas/               ← endereços: API em JSON (zona, problemas, mapa, painel) e telas (telas.py)
  dominio.py           ← regras: risco → P1 + brigada, cor da zona, categorias
  modelo.py            ← IA: treina e prevê categoria e prioridade
  servico.py, consultas.py, db.py, seed.py ← banco SQLite, consultas e dados fictícios
  templates/           ← telas HTML (Jinja)
  static/              ← CSS, JavaScript e Bootstrap local
data/                  ← frases de treino e teste cego da IA
tests/                 ← pytest
docs/
  contrato.md          ← nomes que todos usam (valores, rotas, funções)
  WORKFLOW.md          ← como a equipe trabalha + problemas previstos
  contexto-ia/         ← texto pronto para colar na IA de cada área
  IA.md                ← onde declaramos todo uso de IA (OBRIGATÓRIO)
  missao-1/, missao-2/, missao-3/ ← entregas e roteiros (teste, vídeo)
  evidencias/          ← prints, fotos e testes (contam 20% da nota)
.github/               ← modelo de Pull Request e testes automáticos
.gitignore             ← lista do que o Git NÃO deve enviar (senhas, lixo, planta)
render.yaml            ← serviço gratuito no Render (link público; a demo não depende dele)
```

---

## 💻 Para quem vai programar

**Leia primeiro:** [`docs/WORKFLOW.md`](docs/WORKFLOW.md) (como trabalhamos) e [`docs/contrato.md`](docs/contrato.md) (nomes que todos usam).
**Vai usar IA?** Cole o arquivo da sua área em [`docs/contexto-ia/`](docs/contexto-ia/) no início da conversa. No Cursor não precisa: ele lê o `AGENTS.md`.
📋 **Quadro de tarefas:** https://github.com/orgs/Hackarun-Dragonair/projects/1

### 1. Preparar (uma vez só)
```bash
git clone https://github.com/Hackarun-Dragonair/dragonair-shopping.git
cd dragonair-shopping
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
# execução: seção "Como executar" abaixo
```
> 💡 No **VS Code**: `File → Open Folder` na pasta do projeto. A aba **Source Control** (ícone de ramificação) faz commit e push com botões, sem terminal.

### 2. Fluxo de cada tarefa
```bash
git switch main && git pull                 # 1. atualizar
git switch -c tarefa-NUMERO                 # 2. criar sua branch (ex.: tarefa-9)
# ... programar ...
git add arquivo1.py arquivo2.py             # 3. escolher o que salvar
git commit -m "feat: o que você fez"        # 4. salvar
git push -u origin tarefa-NUMERO            # 5. enviar
```
6. No GitHub, clique em **Compare & pull request** → escreva `Closes #NUMERO` → **Create pull request**.
7. Outra pessoa revisa e clica em **Merge**.

### 3. Deu problema?
- **Conflito** (`<<<<<<<` no arquivo): escolha o trecho certo, apague as marcas, salve, `git add`, `git commit`. Na dúvida, chame alguém ou um mentor.
- **Desfazer mudança local:** `git restore arquivo`
- 🚫 **Nunca** use `git push --force` nem `git reset --hard` na `main`.

---

## ⚠️ Regras da equipe
1. **Nada de senhas, chaves de API ou dados pessoais** no repo (ele é público).
2. **Usou IA? Registre em [`docs/IA.md`](docs/IA.md).** É exigido pelo regulamento.
3. **Fez algo? Guarde evidência** em `docs/evidencias/` (print, foto, resultado de teste).
4. **Pegou uma tarefa?** Arraste o cartão para **Fazendo** no [quadro](https://github.com/orgs/Hackarun-Dragonair/projects/1).
5. **Código entra na `main` só por Pull Request.** O GitHub roda os testes sozinho: ❌ vermelho = não juntar.
6. **Planta do shopping é dado sensível:** nunca no repo, na IA, na demo ou no vídeo. O mapa é desenho nosso.

---

## ▶️ Como executar
Pré-requisito: Python 3.11+. Na Missão 2 o servidor é **Flask** (alternativa já prevista na Entrega 1). A API segue em JSON. A página inicial e a rota do QR já abrem no navegador.

**Windows (PowerShell)**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python wsgi.py
```

**macOS / Linux**
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python wsgi.py
```

`python wsgi.py` sobe o servidor, recria o banco com os dados de exemplo e abre http://127.0.0.1:8000/ no navegador. A rota do QR de exemplo é http://127.0.0.1:8000/z/sanitario-piso1 (nome da zona e os botões OK, Atenção e Problema). O OK grava uma conferência no SQLite.

**Telas (abrem no navegador, celular ou computador):**

| Tela | Endereço |
|---|---|
| Mapa das zonas (cinza = ninguém conferiu) | `/` |
| Tela do QR da zona (OK / Atenção / Problema + sugestão da IA) | `/z/sanitario-piso1` |
| Fila de problemas | `/telas/fila` |
| Problema + linha do tempo + dossiê | `/telas/problemas/<id>` |
| Painel | `/telas/painel` |
| Sobre a IA (acerto real) | `/telas/sobre-a-ia` |

No celular, conecte no mesmo Wi-Fi ou hotspot do notebook e abra `http://IP-DO-NOTEBOOK:8000`.

Para o cliente que pede JSON, envie `Accept: application/json` ou `?format=json`. `GET /` nesse modo lista os endpoints. Os principais:

| Método | Caminho | Uso |
|---|---|---|
| GET | `/mapa` | zonas, estado (ok, atencao, problema, cinza) e a URL para o QR |
| GET | `/z/<codigo>` | uma zona, histórico e botões daquele tipo |
| POST | `/z/<codigo>/conferir` | `{resultado: ok\|atencao\|problema, origem: qr\|lista}` |
| POST | `/z/<codigo>/triagem` | `{descricao}` → sugestão da IA |
| POST | `/z/<codigo>/problema` | grava o problema na fila |
| GET | `/fila` | problemas; filtros `piso`, `equipe`, `prioridade`, `status` |
| POST | `/problemas/<id>/confirmar` | supervisor confirma categoria, prioridade e equipe |
| POST | `/problemas/<id>/assumir` | em atendimento |
| POST | `/problemas/<id>/resolver` | resolvido; a linha do tempo só cresce |
| GET | `/painel` | os três indicadores, por zona e equipe |
| GET | `/sobre-o-modelo` | acerto medido no teste cego |
| GET | `/usuarios` | usuários fictícios da demo |
| POST | `/entrar` | `{usuario_codigo}` grava a sessão; ou envie o cabeçalho `X-Usuario` |

Ao iniciar, o banco é recriado com os dados de exemplo. Para preservar o arquivo local entre uma subida e outra, use `SEED_ON_START=0`. `PUBLIC_BASE_URL` é o endereço que entra no QR.

Testes: `python -m pytest`.

**Link público:** o `render.yaml` sobe um Web Service gratuito (um worker, porque o banco é SQLite). O disco some quando o serviço dorme; por isso o cenário é recriado na subida. A apresentação usa o notebook.

## 🤖 Uso de IA
Declarado em [docs/IA.md](docs/IA.md). Dentro do produto, o modelo é scikit-learn (TF-IDF + regressão logística), treinado nas frases de `data/treino.csv`. O acerto medido no teste cego sai em `GET /sobre-o-modelo`.

## 📜 Créditos e licenças
- Flask (BSD) — API
- scikit-learn (BSD) — modelo local de triagem
- Ultralytics YOLOv8n (AGPL-3.0) — contagem de pessoas na câmera (proposta, pasta `camera/`)
- Roboflow supervision (MIT) — rastreio, zonas e pixelização
- Bootstrap 5.3 (MIT) — visual das telas, incluído no projeto para funcionar sem internet
- Protótipo visual inicial: Mateus Castro (equipe, com apoio do Gemini)
- Dados de treino, zonas e usuários: fictícios, criados pela equipe
- Mapa: desenho próprio em blocos (não usa a planta do shopping)
