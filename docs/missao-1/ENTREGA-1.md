# Entrega 1 — Planejamento técnico inicial
**Equipe Dragonair · HackaRun 2026 · Desafio 09: Eficiência operacional e infraestrutura**

**Solução: Ronda Viva — "Mostra o que ninguém conferiu. Registra que cuidou."**

## Contexto
A administração do shopping não sabe em que condição cada ambiente está agora nem quando foi conferido pela última vez: a ronda vive numa folha de papel e os problemas chegam soltos pelo rádio. A **Ronda Viva** é um sistema web responsivo de ronda operacional:

1. O encarregado lê o **QR da zona** com o celular da equipe e toca **OK / Atenção / Problema**.
2. No "Problema", descreve com botões prontos ou uma frase; nossa **IA própria (sem internet)** sugere categoria, prioridade e equipe.
3. O **supervisor confirma** e o problema vira tarefa para a equipe certa.
4. O **mapa** mostra o estado de cada zona e fica **cinza onde ninguém conferiu no prazo**.
5. Cada passo entra numa **linha do tempo que não pode ser apagada** — o registro de que o shopping cuidou.

## 1. Proposta e estrutura inicial das telas
| # | Tela | Quem usa | O que faz |
|---|---|---|---|
| 1 | **Zona** (abre pelo QR) | Encarregado, no celular | Nome da zona, última conferência, botões OK / Atenção / Problema |
| 2 | **Problema + sugestão da IA** | Encarregado, no celular | Botões prontos + "perto de" + frase → "IA sugere: Hidráulica · P2 · Manutenção" → confirmar |
| 3 | **Mapa** | Supervisor, no tablet | Zonas coloridas por estado; cinza = sem conferência no prazo |
| 4 | **Fila de problemas** | Supervisor / equipes | Aberto → Em atendimento → Resolvido, com a linha do tempo de cada problema |
| 5 | **Painel** | Gestão, no computador | Indicadores (% de zonas conferidas no prazo, tempo de resolução, reincidência) e acerto da IA |

Tela de apoio: escolha do usuário de demonstração (fictício). Esboços em [`telas/`](telas/).

## 2. Documentação inicial do projeto
- **Repositório:** https://github.com/Hackarun-Dragonair/dragonair-shopping
- **README** com objetivo, guia da equipe e estrutura de pastas.
- **Planejamento detalhado** (problema, público, proposta de valor, Canvas, backlog priorizado, regras de funcionamento, implantação): [`README.md`](README.md) desta pasta.
- **Pitch e perguntas difíceis:** [`pitch-e-faq.md`](pitch-e-faq.md) · **Uso de IA declarado:** [`docs/IA.md`](../IA.md) · **Evidências:** [`docs/evidencias/`](../evidencias/) · **Discussão da ideia:** Issue #1.

## 3. Linguagem de programação escolhida
**Python** — todos da equipe conhecem, e tem as bibliotecas de IA prontas.

## 4. Arquitetura proposta
```
[Celular · Tablet · Computador]   ← mesmo site, layout responsivo
              │
              ▼
[Servidor web em Python (FastAPI)]
   ├── Triagem: regra de risco → modelo de IA → supervisor confirma
   ├── Encaminhamento: tabela categoria → equipe (definida pelo gestor)
   ├── Zonas: estado, zona cinza, reincidência
   ├── Linha do tempo: eventos só são acrescentados, nunca apagados
   └── Banco de dados: zonas, conferências, problemas, eventos
[Modelo de IA] treinado pela equipe, roda dentro do servidor (sem API externa)
```
**Regras-chave:**

- A IA **sugere** e o supervisor **decide**.
- Palavra de risco (fumaça, fogo, choque, pessoa presa) **sempre** orienta avisar a brigada pelo rádio — nunca rebaixa a prioridade.
- O QR registra a conferência feita no local; indicadores são por **zona e equipe**, nunca por pessoa.

## 5. Plataforma e tecnologias adotadas
| Camada | Tecnologia |
|---|---|
| Servidor | Python + **FastAPI** (Flask como alternativa equivalente) |
| Telas | HTML (Jinja) + **Bootstrap** ou **Pico.css** |
| Banco de dados | **SQLite** (dados fictícios recriados a cada início) |
| Inteligência artificial | **scikit-learn** (modelo próprio, offline, acerto medido em teste cego) |
| Testes | **pytest** |
| Publicação | Demonstração **local no notebook** + link público no **Render** |
| Versionamento | **Git + GitHub** (organização Hackarun-Dragonair) |

## 6. Tecnologia sorteada: Responsividade
Incorporada como **"um dado, três telas"** — a mesma informação no formato certo para cada papel:

- **Celular (campo):** uma ação por tela, botões grandes, uso com uma mão.
- **Tablet (sala de controle):** mapa em tela cheia, legível de longe.
- **Computador (gestão):** mapa e painel lado a lado, filtros e relatórios.

**Demonstração:** registrar um problema pelo celular e ver a zona mudar de cor no computador em segundos; redimensionar a tela ao vivo. Evidências: prints nas 3 larguras em `docs/evidencias/`.
