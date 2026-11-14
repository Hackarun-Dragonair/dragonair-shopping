# Ronda Viva — Dragonair · HackaRun 2026

> Equipe **Dragonair** · Desafio **09: Eficiência operacional e infraestrutura** · UniCatólica, 12 a 14/11/2026

**O problema:** um shopping precisa acompanhar as condições dos ambientes, identificar ocorrências, organizar atividades operacionais e garantir que os serviços não parem. ([texto oficial](docs/desafio.md))

**Nossa solução: Ronda Viva** — *"Mostra o que ninguém conferiu. Registra que cuidou."* Sistema web responsivo que mostra quais ambientes ninguém conferiu, usa uma IA treinada pela equipe (sem internet) para sugerir categoria e prioridade de cada problema achado na ronda, e registra cada passo numa linha do tempo que não se apaga.

## Links rápidos

| O quê | Onde |
|---|---|
| Site da demo (Render grátis) | https://ronda-viva-0ek7.onrender.com — dorme após 15 min; o 1º acesso leva cerca de 1 min |
| Repositório | https://github.com/Hackarun-Dragonair/dragonair-shopping |
| Versão estável da Missão 2 (tag) | `v-missao2-estavel` |
| **Como executar** | [seção abaixo](#como-executar) |
| Resumo de 1 página | [`docs/RESUMO.md`](docs/RESUMO.md) |
| Checklist e textos de entrega | [`docs/ENTREGA.md`](docs/ENTREGA.md) |
| Uso de IA (declaração) | [`docs/IA.md`](docs/IA.md) |
| Evidências (testes, QA, IA, prints) | [`docs/evidencias/`](docs/evidencias/README.md) |
| Pitch de 90 s, demo, FAQ da banca | [`docs/pitch/`](docs/pitch/) |
| Missão 1 (planejamento técnico) | [`docs/missao-1/ENTREGA-1.md`](docs/missao-1/ENTREGA-1.md) · [planejamento detalhado](docs/missao-1/README.md) |

---

## Como executar

Testado do zero em 13/11/2026 à noite: `git clone` numa pasta vazia, ambiente novo, instalação, `python -m pytest -q` e servidor no ar respondendo em `/saude` e `/` (Linux, Python 3.14). O GitHub roda os mesmos testes com Python 3.12 e o Render usa Python 3.11. Os comandos de Windows abaixo são os padrões do Python, mas não foram testados nesta rodada.

### 1. Pré-requisitos
- **Python 3.11 ou mais novo** (`python --version` ou `python3 --version`).
- **Git** (`git --version`). Sem Git: no GitHub, botão **Code → Download ZIP** e descompacte.
- Internet só para instalar. Depois de instalado, o sistema roda sem internet (a IA e o visual estão dentro do projeto).

### 2. Baixar e instalar (uma vez só)

**Linux / macOS**
```bash
git clone https://github.com/Hackarun-Dragonair/dragonair-shopping.git
cd dragonair-shopping
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

**Windows (PowerShell)**
```powershell
git clone https://github.com/Hackarun-Dragonair/dragonair-shopping.git
cd dragonair-shopping
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

O `venv` é uma "caixa" só deste projeto para as bibliotecas (Flask, scikit-learn, pytest, segno). Toda vez que abrir um terminal novo, ative de novo (`source .venv/bin/activate` ou `.\.venv\Scripts\Activate.ps1`).

### 3. Configurar (opcional)
Funciona sem configurar nada. Estas variáveis mudam o comportamento (nomes conferidos em `app/__init__.py` e `wsgi.py`):

| Variável | Padrão | Para que serve |
|---|---|---|
| `PORT` | `8000` | Porta do servidor |
| `SECRET_KEY` | `demo-ronda-viva` | Chave que protege a sessão (o crachá). Em servidor público, troque |
| `SEED_ON_START` | `1` | `1` = recria o banco com os dados de exemplo a cada início. `0` = guarda o que foi registrado |
| `DATABASE_PATH` | `instance/ronda.sqlite3` | Onde fica o arquivo do banco SQLite |
| `PUBLIC_BASE_URL` | vazio | Endereço que entra no QR das etiquetas (ex.: `http://192.168.0.10:8000`). Vazio = usa o endereço aberto no navegador |
| `SEXTA13` | `auto` | Easter Egg do gato preto: `auto` só na sexta-feira 13, `1` sempre, `0` nunca |

Como usar uma variável:
```bash
PORT=8001 SEXTA13=1 python wsgi.py          # Linux / macOS
```
```powershell
$env:PORT="8001"; $env:SEXTA13="1"; python wsgi.py    # Windows (PowerShell)
```

### 4. Executar
```bash
python wsgi.py
```
Abre em **http://127.0.0.1:8000** (o navegador abre sozinho depois de 1 segundo). Para desligar: `Ctrl+C` no terminal.

Teste rápido de que está no ar: abra http://127.0.0.1:8000/saude — deve aparecer `{"servico":"ronda-viva","status":"ok"}`.

Ao iniciar, o banco é recriado com dados de exemplo: 11 zonas fictícias, algumas cinza (ninguém conferiu), uma ocorrência aberta e duas resolvidas.

### 5. Rodar os testes
```bash
python -m pytest -q
```
Esperado: **73 passed**. Leva de 2 a 8 minutos, dependendo do computador, porque a IA é treinada várias vezes nos testes.

### 6. Usar no celular (mesma rede)
1. Notebook e celular no **mesmo Wi-Fi** ou no hotspot do celular.
2. Descubra o IP do notebook: Linux `hostname -I` · macOS `ipconfig getifaddr en0` · Windows `ipconfig` (linha "Endereço IPv4").
3. No celular, abra `http://IP-DO-NOTEBOOK:8000` (ex.: `http://192.168.0.10:8000`). O servidor já aceita conexões da rede (o terminal mostra `Running on http://...`).
4. Para imprimir etiquetas QR que abram no celular, gere o PDF abrindo o sistema **pelo IP** (não por `127.0.0.1`) ou ligue com `PUBLIC_BASE_URL=http://IP-DO-NOTEBOOK:8000`.

### 7. Crachás da demo (fictícios)
Botão **Entrar com crachá** (no celular: **Entrar**, no menu de baixo).

| Crachá | Perfil | O que pode |
|---|---|---|
| `OTTO` | Gestor (ADM) · supervisor | Painel, confirmar a sugestão da IA, editar mapa, etiquetas QR (PDF) |
| `LIA` | Gestor (ADM) · coordenação | O mesmo do OTTO |
| `RITA` | Funcionário · encarregada | Ronda pelo QR, assumir e resolver ocorrências |
| `CAIO` | Funcionário · manutenção | O mesmo da RITA |

**O QR funciona sem entrar:** quem abre `/z/<codigo>` registra como "Campo (sem crachá)".

### 8. Problemas comuns
| Aconteceu | O que fazer |
|---|---|
| `python` não é reconhecido (Windows) | Reinstale o Python marcando **"Add python.exe to PATH"**, ou use `py` no lugar de `python` |
| PowerShell bloqueia o `Activate.ps1` | Rode `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` e ative de novo |
| `pip install` falha no scikit-learn | Use Python 3.11 ou 3.12 e atualize o pip: `python -m pip install --upgrade pip` |
| `Address already in use` / porta ocupada | Outro programa usa a 8000. Rode com outra porta: `PORT=8001 python wsgi.py` |
| O celular não abre o endereço | Confira se estão na mesma rede; no Windows, aceite o aviso do Firewall para "Redes privadas"; Wi-Fi de evento às vezes bloqueia aparelhos entre si: use o hotspot do celular |
| O QR da etiqueta abre `127.0.0.1` no celular | Gere o PDF abrindo o sistema pelo IP, ou use `PUBLIC_BASE_URL` (item 6) |
| O que registrei sumiu ao reiniciar | É de propósito (dados de exemplo). Para guardar: `SEED_ON_START=0 python wsgi.py` |
| O gato preto não aparece | Ele só aparece na sexta-feira 13 ou com `SEXTA13=1`, e só se houver zona cinza |
| Site do Render demora ou mostra página de espera | Está acordando (plano grátis). Espere cerca de 1 min. Os dados voltam ao exemplo a cada reinício, e a planta enviada no editor some |

---

## Telas

| Tela | Endereço | Quem |
|---|---|---|
| Mapa das zonas (cinza = ninguém conferiu no prazo) | `/` | todos |
| Tela do QR da zona (OK / Atenção / Problema + sugestão da IA) | `/z/sanitario-piso1` (troque pelo código da zona) | todos, sem entrar |
| Fila de ocorrências | `/telas/fila` | todos |
| Ocorrência + linha do tempo + dossiê | `/telas/problemas/<id>` | todos (confirmar: só gestor) |
| Painel de gestão | `/telas/painel` | gestor |
| Editar mapa (imagem de fundo + bloquinhos por zona) | `/telas/mapa/editar` | gestor |
| Etiquetas QR (PDF) | `/etiquetas.pdf` | gestor |
| Sobre a IA (acerto medido) | `/telas/sobre-a-ia` | todos |
| Entrar com crachá | `/entrar` | todos |

## API (JSON)
Para receber JSON, envie `Accept: application/json` ou `?format=json`. `GET /` nesse modo lista os endpoints.

| Método | Caminho | Uso |
|---|---|---|
| GET | `/saude` | confirma que o servidor está no ar |
| GET | `/mapa` | zonas, estado (ok, atencao, problema, cinza) e a URL para o QR |
| GET | `/z/<codigo>` | uma zona, histórico e botões daquele tipo |
| POST | `/z/<codigo>/conferir` | `{resultado: ok\|atencao\|problema, origem: qr\|lista}` |
| POST | `/z/<codigo>/triagem` | `{descricao}` → sugestão da IA |
| POST | `/z/<codigo>/problema` | grava o problema na fila |
| GET | `/fila` | problemas; filtros `piso`, `equipe`, `prioridade`, `status` |
| POST | `/problemas/<id>/confirmar` | gestor confirma categoria, prioridade e equipe (P1 de risco não baixa) |
| POST | `/problemas/<id>/assumir` | em atendimento |
| POST | `/problemas/<id>/resolver` | resolvido; a linha do tempo só cresce |
| GET | `/problemas/<id>/dossie` | resumo para imprimir (JSON, ou texto com `Accept: text/plain`) |
| POST | `/dispositivos` | autoriza o celular `{apelido, token}` |
| POST | `/crachas/entrar` | `{codigo, token}` troca o usuário se o aparelho e o crachá forem válidos |
| POST | `/fila-envio` | reenvia conferências e problemas guardados quando a rede voltou |
| GET | `/alertas` | OK divergente e semana sem achados, por zona |
| GET | `/zonas/<codigo>/ritmo` | prazo sugerido pelo histórico; em 24/12, 25/12 e 31/12 o prazo cai pela metade |
| GET | `/etiquetas` · `/etiquetas.pdf` | nome da zona, onde colar e a URL (o PDF tem o QR) |
| GET | `/painel` | os indicadores, por zona e equipe |
| GET | `/sobre-o-modelo` | acerto medido no teste cego |
| GET | `/usuarios` | usuários fictícios da demo |

**Link público:** o `render.yaml` sobe um Web Service gratuito (um worker, porque o banco é SQLite). O disco some quando o serviço reinicia; por isso o cenário é recriado na subida. Na apresentação, o plano B é rodar no notebook ([`docs/pitch/demo-cliques.md`](docs/pitch/demo-cliques.md)).

## Easter Egg: sexta-feira 13
Na sexta-feira 13, um **gato preto** se esconde na zona que **ninguém confere há mais tempo** (a mais esquecida entre as cinzas).
- O mapa mostra a frase uma vez no topo e o gato em **uma zona só**.
- Quem confere a zona pelo QR **espanta o gato**, e ele pula para a próxima zona esquecida. Sem zona cinza, o gato vai embora.
- É o diferencial da Ronda Viva (o que ninguém conferiu) virando brincadeira: o gato mostra onde a ronda deve ir primeiro.

Para demonstrar em outro dia (ex.: final de sábado): `SEXTA13=1 python wsgi.py` (Windows: `$env:SEXTA13="1"; python wsgi.py`). No Render, seria preciso criar a variável `SEXTA13=1` no painel do serviço. Código: `app/sexta13.py`, testes: `tests/test_sexta13.py`.

## Uso de IA
Declarado em [`docs/IA.md`](docs/IA.md). Dentro do produto, o modelo é scikit-learn (TF-IDF de pedaços de letras + regressão logística), treinado nas frases de `data/treino.csv`, sem internet e sem API paga. O acerto medido no teste cego aparece na tela "Sobre a IA" e em `docs/evidencias/modelo/resumo.md` (gerado por `python -m app.avaliar`).

---

## Para a equipe

### Comece aqui
**Você NÃO precisa saber Git para ajudar.** Quase tudo dá para fazer pelo site do GitHub.

| Quero... | Onde / como |
|---|---|
| Dar opinião sobre a ideia | Aba **Issues** → abrir a issue → escrever no campo de comentário no fim da página → **Comment** |
| Ver o que cada um está fazendo | Aba **Issues** (cada tarefa é uma issue, com o nome de quem pegou) |
| Escrever um texto | Abrir o arquivo em `docs/` → ícone de **lápis** → escrever → **Commit changes** |
| Subir foto ou print (evidência) | Entrar na pasta `docs/evidencias/` → **Add file** → **Upload files** → arrastar → **Commit changes** |
| Registrar que usei IA | Editar `docs/IA.md` (lápis) e adicionar uma linha na tabela |

**Mini-dicionário**
- **Repositório (repo):** a "pasta do projeto" na nuvem. É este aqui.
- **Commit:** salvar uma alteração com uma frase explicando o que mudou.
- **Issue:** um tópico de conversa ou uma tarefa (como um post com comentários).
- **Branch (ramo):** uma cópia de trabalho para mexer no código sem quebrar a versão principal (`main`).
- **Pull Request (PR):** pedido para juntar sua branch na `main`. Outra pessoa revisa antes.

**Mensagem de commit:** comece com o tipo e diga o que mudou: `docs: escreve proposta de valor` · `feat: tela de nova ocorrência` · `fix: corrige erro ao salvar`. Evite `ajustes`, `teste`, `final2` — a banca olha o histórico.

### O que tem em cada pasta
```
README.md              ← você está aqui
AGENTS.md              ← contexto do projeto para qualquer IA (Cursor lê sozinho)
wsgi.py                ← liga o servidor Flask (python wsgi.py)
app/
  __init__.py          ← cria o app Flask e semeia os dados de exemplo
  rotas/               ← endereços: API em JSON e telas (telas.py)
  dominio.py           ← regras: risco → P1 + brigada, cor da zona, categorias
  modelo.py            ← IA: treina e prevê categoria e prioridade
  avaliar.py           ← mede a IA e gera docs/evidencias/modelo/
  servico.py, consultas.py, db.py, seed.py ← banco SQLite, consultas e dados fictícios
  templates/           ← telas HTML (Jinja)
  static/              ← CSS, JavaScript e Bootstrap local
data/                  ← frases de treino, teste cego e teste de campo da IA
tests/                 ← pytest
docs/
  RESUMO.md, ENTREGA.md ← resumo de 1 página e checklist/textos de entrega
  pitch/               ← roteiro de 90 s, cliques da demo, FAQ da banca, cola, checklist de sábado
  contrato.md          ← nomes que todos usam (valores, rotas, funções)
  WORKFLOW.md          ← como a equipe trabalha + problemas previstos
  contexto-ia/         ← texto pronto para colar na IA de cada área
  IA.md                ← onde declaramos todo uso de IA (OBRIGATÓRIO)
  missao-1/, missao-2/, missao-3/ ← entregas e roteiros (teste, vídeo)
  evidencias/          ← prints, QA, avaliação da IA (contam 20% da nota)
.github/               ← modelo de Pull Request e testes automáticos
render.yaml            ← serviço gratuito no Render (link público)
```

### Para quem vai programar
**Leia primeiro:** [`docs/WORKFLOW.md`](docs/WORKFLOW.md) e [`docs/contrato.md`](docs/contrato.md). **Vai usar IA?** Cole o arquivo da sua área em [`docs/contexto-ia/`](docs/contexto-ia/). No Cursor não precisa: ele lê o `AGENTS.md`.
Quadro de tarefas: https://github.com/orgs/Hackarun-Dragonair/projects/1

Fluxo de cada tarefa (depois de instalar, ver [Como executar](#como-executar)):
```bash
git switch main && git pull                 # 1. atualizar
git switch -c tarefa-NUMERO                 # 2. criar sua branch (ex.: tarefa-9)
# ... programar ...
python -m pytest -q                         # 3. testar (tudo verde)
git add arquivo1.py arquivo2.py             # 4. escolher o que salvar
git commit -m "feat: o que você fez"        # 5. salvar
git push -u origin tarefa-NUMERO            # 6. enviar
```
No GitHub, clique em **Compare & pull request** → escreva `Closes #NUMERO` → **Create pull request**. Outra pessoa revisa e clica em **Merge**.

**Deu problema?** Conflito (`<<<<<<<` no arquivo): escolha o trecho certo, apague as marcas, salve, `git add`, `git commit`. Desfazer mudança local: `git restore arquivo`. **Nunca** use `git push --force` nem `git reset --hard` na `main`.

### Regras da equipe
1. **Nada de senhas, chaves de API ou dados pessoais** no repo (ele é público).
2. **Usou IA? Registre em [`docs/IA.md`](docs/IA.md).** É exigido pelo regulamento.
3. **Fez algo? Guarde evidência** em `docs/evidencias/` (print, foto, resultado de teste).
4. **Código entra na `main` só por Pull Request.** O GitHub roda os testes sozinho: vermelho = não juntar.
5. **Planta do shopping é dado sensível:** nunca no repo, na IA, na demo ou no vídeo. O mapa é desenho nosso.

## Créditos e licenças
- Flask (BSD) — servidor e telas
- scikit-learn (BSD) — modelo local de triagem
- segno (BSD) — QR das etiquetas
- Bootstrap 5.3 (MIT) — visual das telas, incluído no projeto para funcionar sem internet
- Protótipo visual inicial: Mateus Castro (equipe, com apoio do Gemini)
- Dados de treino, zonas e usuários: fictícios, criados pela equipe
- Mapa: desenho próprio em blocos (não usa a planta do shopping)
