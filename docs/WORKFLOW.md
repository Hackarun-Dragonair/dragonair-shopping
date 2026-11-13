# 🔁 Como a equipe trabalha (leia em 3 minutos)

## Por que um repositório só (e não um para back, front e banco)
- A banca recebe **um link** e roda **um comando**.
- Aqui o próprio servidor entrega as telas, então separar só criaria trabalho para juntar.
- Cada área tem sua **pasta**. Isso já evita a bagunça que repos separados tentariam evitar.

## Quem mexe onde
| Área | Pastas e arquivos | Quadro |
|---|---|---|
| Backend | `app/main.py`, `app/banco.py` | #2 #3 #11 #12 |
| Telas | `app/templates/`, `app/static/` | #4 #5 #10 |
| IA | `ia/` | #6 #7 |
| Dados | `dados/`, `app/status.py` | #8 #9 #10 |

Os nomes que todos usam estão em **[`contrato.md`](contrato.md)**. A estrutura já está pronta: **não crie pastas novas**.

## O ciclo de cada tarefa
1. No [quadro](https://github.com/orgs/Hackarun-Dragonair/projects/1), arraste seu cartão para **Fazendo**.
2. Atualize: `git switch main` e depois `git pull`.
3. Crie a branch: `git switch -c tarefa-NUMERO` (ex.: `tarefa-7`).
4. Programe (com IA, usando o arquivo da sua área em `contexto-ia/`).
5. Teste: `pytest -q`. Precisa dar tudo verde.
6. Envie: `git add .` → `git commit -m "feat: o que fez"` → `git push -u origin tarefa-7`.
7. No GitHub: **Compare & pull request** → escreva `Closes #7` → **Create**.
8. Outra pessoa olha e clica em **Merge**. O cartão vai para **Feito** sozinho.

> Sem Git no PC? Planilhas (`dados/*.csv`) e textos dá para editar direto no site: lápis ✏️ → **Commit changes** → escolha **"Create a new branch"** → PR.

## 🧯 O que pode dar errado e o que fazer
| Problema | Solução |
|---|---|
| Esperar o colega terminar | Use os dados de exemplo e o contrato. Todo mundo começa já, com o app rodando. |
| IA inventa nomes, pastas ou tecnologia | Sempre comece colando o contexto da sua área. Se ela inventar, diga: "siga o contrato". |
| Dois mexendo no mesmo arquivo (conflito) | Cada um na sua pasta. Arquivo de outra área? Peça para o dono. Conflito: chame o Paulo ou um mentor. |
| PR que quebra o app | O GitHub roda os testes sozinho. ❌ vermelho = não fazer merge. |
| PR gigante que ninguém consegue revisar | Um PR por tarefa, pequeno. Abriu PR? Avise no grupo. |
| `pip install` falha (Python muito novo) | Use Python 3.12. Ou peça ajuda no grupo com o print do erro. |
| Internet cai na demo | Bootstrap e IA já ficam no projeto. Rode no notebook e conecte o celular no mesmo Wi-Fi ou hotspot. |
| Esquecer de registrar o uso de IA | É item do PR: uma linha em `docs/IA.md` por tarefa. |
| Imagem da planta no repo público | Proibido até a organização liberar. O `.gitignore` já bloqueia os nomes conhecidos. |
| Alguém some ou trava | Duplas de apoio: Backend ↔ IA e Telas ↔ Dados. Travou 30 min? Fala no grupo. |
| Ninguém sabe explicar o código para a banca | Cada PR explica em 3 linhas o que faz. Código simples > código esperto. |
| Mexer na reta final e quebrar | **Sábado 8h: congelamento.** Depois disso, só correção com PR revisado. |

## Combinados de horário
- **18h:** status no grupo em 3 linhas: fiz / vou fazer / travei em.
- **19h:** integração presencial e teste no celular.
- **Sábado 8h:** congela. **10h:** entrega.
