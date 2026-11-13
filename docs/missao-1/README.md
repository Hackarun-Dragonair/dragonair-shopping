# Missão 1 — Problema, requisitos e planejamento técnico
**Equipe Dragonair · HackaRun 2026 · Desafio 09: Eficiência operacional e infraestrutura**

> ## Ronda Viva — "Mostra o que ninguém conferiu. Registra que cuidou."
> Sistema web responsivo para a ronda operacional de shoppings. Mostra quais ambientes **ninguém conferiu no prazo**, transforma cada problema encontrado em tarefa com prioridade e equipe certa usando uma **IA treinada pela equipe que funciona sem internet**, e registra numa **linha do tempo que não pode ser apagada** tudo o que foi feito.

Como chegamos aqui: discussão na [Issue #1](../../issues/1), pesquisa e várias rodadas de crítica simulando a banca (declarado em [`docs/IA.md`](../IA.md)). Pitch e perguntas difíceis: [`pitch-e-faq.md`](pitch-e-faq.md).

---
# Parte A — Problema e requisitos

## 1. Problema delimitado
A administração do shopping **não sabe em que condição cada ambiente está agora nem quando ele foi realmente conferido**. A ronda é registrada numa folha de papel que qualquer um assina depois; os problemas chegam como texto solto pelo rádio, sem prioridade nem dono, e se perdem na troca de turno. Quando algo dá errado (ex.: queda em piso molhado), **não há registro confiável do que foi feito** — e é o shopping que precisa demonstrar que sinalizou.

| Texto do desafio | Como a Ronda Viva responde |
|---|---|
| Acompanhar as condições dos ambientes | Cada zona tem estado: OK, Atenção, Problema ou **cinza** (ninguém conferiu no prazo) |
| Identificar ocorrências | QR da zona → "Problema" → **IA classifica** categoria, prioridade e equipe |
| Organizar atividades operacionais | O problema vira tarefa com status e equipe; "Minha ronda" ordena as próximas zonas |
| Garantir a continuidade dos serviços | Zona cinza = serviço que não aconteceu; reincidência; registro de cada passo |

## 2. Público-alvo

| Usuário | Dispositivo | O que faz |
|---|---|---|
| **Encarregado / líder de turno** (usuário principal no início) e equipe de campo | **Celular da equipe** (autorizado) | Lê o QR da zona e registra OK / Atenção / Problema |
| Supervisor / sala de controle | **Tablet** | Mapa ao vivo, confirma sugestões da IA, despacha tarefas |
| Coordenação de operações | **Computador** | Indicadores, relatórios, cadastros (zonas, equipe, encaminhamento) |

**Comprador:** gerência de operações / administradora do shopping.

## 3. Proposta de valor
**Para** a gerência de operações de shoppings, **que** não sabe onde ninguém olhou e não consegue demonstrar o que fez, **a Ronda Viva** mostra as zonas esquecidas, encaminha cada problema para a equipe certa e registra cada passo com hora numa linha do tempo — **diferente de** folha de papel, rádio, WhatsApp ou apps de checklist, que só registram a tarefa feita e não mostram o que **não** aconteceu.

## 4. Canvas simplificado

| Bloco | Conteúdo |
|---|---|
| Problema | Estado dos ambientes invisível; ronda sem registro confiável; problemas soltos no rádio |
| Público | Encarregados e equipe de campo (celular), supervisão (tablet), gestão (computador) |
| Solução | QR por zona → 3 botões → IA sugere categoria, prioridade e equipe → supervisor confirma → mapa com zona cinza → tarefa até resolver (linha do tempo) → painel |
| Proposta de valor | Ver onde ninguém olhou, encaminhar certo sem depender do rádio e registrar que cuidou |
| Diferencial | Zona cinza (mostra o que não aconteceu) + IA própria offline e medida em teste cego + linha do tempo não apagável |
| Uso de IA | Modelo de machine learning próprio (scikit-learn), sem API externa; sugere, nunca decide sozinho |
| Métricas | % de zonas conferidas no prazo · tempo problema → resolvido · reincidência por zona · acerto do modelo |
| Custos e receita *(hipótese)* | Protótipo R$ 0. Produção: hospedagem simples + QR impresso. Modelo SaaS por shopping com implantação, a validar no piloto |

## 5. Backlog priorizado
**MUST — núcleo do MVP (meta: no ar sexta 22h; com testes até sábado 10h)**

| # | História de usuário |
|---|---|
| M1 | Como **encarregado**, quero ler o QR da zona e tocar OK / Atenção / Problema, para registrar a conferência em segundos |
| M2 | Como **encarregado**, quero descrever o problema com botões prontos ou uma frase e receber a sugestão da IA (categoria, prioridade, equipe), com pergunta de desempate quando houver dúvida |
| M3 | Como **supervisor**, quero um mapa por blocos que mostre o estado de cada zona e fique **cinza** quando ninguém conferiu no prazo |
| M4 | Como **supervisor**, quero confirmar a sugestão e acompanhar cada problema (Aberto → Em atendimento → Resolvido) na equipe certa |
| M5 | Como **coordenador**, quero um painel com 3 indicadores e a página "Sobre o modelo" (acerto medido) |
| M6 | Como **gestor**, quero que cada problema tenha uma **linha do tempo que só recebe eventos novos** (nunca apaga), com os passos de segurança e um resumo para imprimir (dossiê mínimo) |
| M7 | Como **equipe**, queremos testar o uso com 3 pessoas de fora (cronometrado) e registrar o resultado como evidência |

**SHOULD — nesta ordem, só depois do núcleo**

| # | Item |
|---|---|
| S1 | Fila de envio quando a conexão falha (com a página já aberta) |
| S2 | Celular autorizado + código do crachá (troca o usuário fictício da demo) |
| S3 | Gerar o PDF de etiquetas QR (nome da zona + onde colar) |
| S4 | Editor do mapa: arrastar para selecionar blocos e dividir/juntar zonas, com histórico |
| S5 | Prazo da zona que aprende o ritmo do prédio (histórico + calendário de Natal/eventos) |
| S6 | Alertas por zona: "OK divergente" e "semana sem achados" |

**Fora do MVP (roadmap):** modo totalmente offline, QR com código rotativo, retreino automático da IA, planta real como fundo do mapa, foto por amostragem, detecção automática de salas na planta.
**Cortado:** chatbot/LLM, QR para clientes, avaliação, ranking ou alertas por pessoa, desconto automático em fatura, NFC.

---
# Parte B — Planejamento técnico

## 6. Telas

| # | Tela | Celular (campo) | Tablet / computador |
|---|---|---|---|
| 1 | **Zona** (abre pelo QR) | Nome da zona, "última conferência há X min", 3 botões grandes | Botões + histórico da zona |
| 2 | **Problema + sugestão da IA** | Botões prontos por tipo de zona + "perto de: saída de ar / cano / quadro / teto / outro" + frase → "IA sugere: Hidráulica · P2 · Manutenção" → Confirmar/Editar | Igual + aviso de reincidência |
| 3 | **Mapa** | Lista das zonas, piores primeiro ("Minha ronda") | Mapa por blocos, cores + ícone + texto, contador de zonas cinza |
| 4 | **Fila de problemas** | Cartões com Assumir / Resolvido | Tabela com filtros por piso, equipe e prioridade |
| 5 | **Painel** | 3 números | Indicadores, reincidência, "Sobre o modelo" |
| 6 | **Entrar (demo)** | Escolher o usuário fictício | Igual |
| 7 | **Cadastros** (gestão) | — | Zonas e local do QR, equipe (por planilha), tabela categoria → equipe |

**Regra de segurança:** palavras de risco (fumaça, fogo, choque, pessoa presa) **sempre** mostram **"avise a brigada pelo rádio"** e a prioridade nunca é rebaixada pelo sistema. A pergunta *"De onde vem?"* só acrescenta contexto para a brigada. O sistema **nunca aciona ninguém sozinho**; quem decide chamar os bombeiros é a brigada.

## 7. Linguagem de programação
**Python 3.11+** — todos da equipe conhecem; tem as bibliotecas de IA prontas.

## 8. Arquitetura proposta
```
[Celular / Tablet / Computador — navegador, mesmo endereço]
        │  HTML + CSS responsivo + atualização automática
        ▼
[Aplicação web em Python (FastAPI)]
   ├── Triagem: regra de risco → modelo de IA → sugestão → confirmação humana
   ├── Encaminhamento: tabela categoria → equipe (definida pelo gestor)
   ├── Saúde das zonas: zona cinza, prazo, reincidência
   ├── Indicadores e relatórios
   ├── Linha do tempo: eventos só são acrescentados, nunca apagados
   └── Banco de dados (SQLite): zonas/blocos, verificações, problemas, eventos, equipes
[Modelo de IA]: frases rotuladas pela equipe → treinar → arquivo do modelo → avaliar em teste cego
```
**Regras de funcionamento**

- **O QR registra a conferência feita no local**; problema pode ser relatado pela lista de zonas (selo "relatado à distância"). QR com código rotativo fica no roadmap.
- **A IA sugere, o supervisor confirma.** Em dúvida, mostra as 2 opções mais prováveis.
- **Indicadores são por zona e equipe, nunca por pessoa.**
- Dados da demonstração são **fictícios**; nenhum dado pessoal no repositório.

## 9. Plataforma e tecnologias

| Camada | Tecnologia | Por quê |
|---|---|---|
| Back-end | Python + **FastAPI** (Flask como alternativa) | Simples, valida os dados da IA e gera a página `/docs` |
| Front-end | HTML (Jinja) + **Pico.css** + **htmx** | Responsivo com controle de layout; atualização ao vivo sem framework pesado |
| Banco | **SQLite** | Zero configuração; dados fictícios recriados a cada início |
| IA | **scikit-learn** (TF-IDF + Regressão Logística) | Offline, milissegundos, sem custo por uso, acerto mensurável |
| Hospedagem | **Demonstração local no notebook** (hotspot) + link no **Render** | O Render gratuito reinicia e apaga o banco; a demo não depende dele |
| Testes | **pytest** + script de avaliação do modelo | Evidência de testes e correções |
| Versionamento | Git + GitHub (organização Hackarun-Dragonair) | Exigido na entrega |

## 10. Tecnologia sorteada: Responsividade

- **Área sorteada na Roleta: Responsividade** (o sistema se adapta a celular, tablet e computador).
- **"Um dado, três lentes"** — a mesma informação no formato certo para cada papel:
  - **Celular (campo):** uma tarefa por tela, botões de 48 px ou mais, uso com uma mão.
  - **Tablet (sala de controle):** mapa em tela cheia, legível a 2 metros.
  - **Computador (gestão):** mapa + painel lado a lado, filtros, relatórios e cadastros.
- **Demonstração:** QR na mesa → celular registra o problema → a zona muda de cor no computador em segundos → redimensionar a tela ao vivo. Evidências: prints nas 3 larguras em `docs/evidencias/`.

---
# Parte C — Implantação e operação
## 11. Padrão de posicionamento do QR (por tipo de zona)
QR de **5 × 5 cm**, alto contraste, entre **1,20 m e 1,50 m**, integrado a uma placa de aviso ou identificação, com a legenda "Controle da equipe". Sempre no **mesmo tipo de lugar** para cada tipo de zona:

| Tipo de zona | Onde fica o QR |
|---|---|
| Sanitário | Placa de aviso na entrada do corredor de acesso aos banheiros |
| Praça de alimentação | Pilares do contorno, 1 QR por setor da praça |
| Corredor (mall) | Placa de identificação no início do corredor |
| Praça central / eventos | Pilar ou totem na borda da praça |
| Escada rolante / elevador | Painel lateral na base |
| Área técnica | Placa da porta, pelo corredor de serviço |
| Doca / depósito | Placa de identificação da doca |
| Entrada / acesso | Lado de dentro, junto à porta |
| Estacionamento | Poste de iluminação (aberto) ou coluna numerada (garagem) |

Cada zona guarda **foto e descrição do local do QR** — reposição e reforma seguem a foto. *Proposta a validar com Operações no piloto.*

## 12. Dia 0 — implantação do piloto em 1 dia

1. **Mapa e zonas:** modelos prontos por tipo de zona (local do QR, prazo, botões prontos) e tabela de encaminhamento pré-preenchida.
2. **Kit de etiquetas:** PDF com todos os QRs, nome da zona e onde colar.
3. **Ronda de instalação:** quem cola lê o QR e tira foto — instalar já é o primeiro uso ("18 de 20 zonas instaladas").
4. **Equipe e celulares:** cadastro por planilha; celular ativado lendo o QR mostrado pelo supervisor.
5. **Treinamento:** 15 min na troca de turno + cartaz de 3 figuras + primeira ronda acompanhada.
6. **Piloto de 30 dias** em sanitários e praça de alimentação, com relatório semanal; depois, expansão por área.

---
## Próximos passos (Missão 2)
A programação começa no lançamento da Missão 2, **sexta 13/11 às 10h** (regulamento, item 5.2). Núcleo M1–M7 no ar até sexta 22h; SHOULD na ordem S1–S6; protótipo, testes e evidências até **sábado 10h**.
