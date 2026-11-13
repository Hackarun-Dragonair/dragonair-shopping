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
docs/
  desafio.md           ← texto oficial do desafio
  IA.md                ← onde declaramos todo uso de IA (OBRIGATÓRIO)
  missao-1/README.md   ← modelo da 1ª entrega: problema, público, telas, arquitetura...
  missao-1/telas/      ← fotos/prints dos esboços das telas
  evidencias/          ← prints, fotos e testes (contam 20% da nota)
.github/               ← modelo automático de Pull Request
.gitignore             ← lista do que o Git NÃO deve enviar (senhas, lixo)
```

---

## 💻 Para quem vai programar

### 1. Preparar (uma vez só)
```bash
git clone https://github.com/Hackarun-Dragonair/dragonair-shopping.git
cd dragonair-shopping
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
# instruções de instalação e execução entram na Missão 2 (a partir de 13/11 10h)
```
> 💡 No **VS Code**: `File → Open Folder` na pasta do projeto. A aba **Source Control** (ícone de ramificação) faz commit e push com botões, sem terminal.

### 2. Fluxo de cada tarefa
```bash
git switch main && git pull                 # 1. atualizar
git switch -c feature/nome-da-tarefa        # 2. criar sua branch
# ... programar ...
git add arquivo1.py arquivo2.py             # 3. escolher o que salvar
git commit -m "feat: o que você fez"        # 4. salvar
git push -u origin feature/nome-da-tarefa   # 5. enviar
```
6. No GitHub, clique em **Compare & pull request** → descreva → **Create pull request**.
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
4. **Pegou uma tarefa? Avise** comentando na issue: "peguei esta".
5. **Código entra na `main` só por Pull Request**, depois que o protótipo existir.

---

## ▶️ Como executar
Pré-requisito: Python 3.10+. Siga o passo 1 de "Para quem vai programar".

## 🤖 Uso de IA
Declarado em [docs/IA.md](docs/IA.md).

## 📜 Créditos e licenças
- _(serão listados na Missão 2: Flask, scikit-learn, Pico.css, htmx)_
