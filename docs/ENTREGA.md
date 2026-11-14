# Entrega — checklist final e textos prontos

**Equipe Dragonair · HackaRun 2026 · Desafio 09 · Ronda Viva**
Horários de sábado: [`pitch/checklist-sabado.md`](pitch/checklist-sabado.md).

## Links (conferir que cada um abre)

| Item | Link |
|---|---|
| Repositório | https://github.com/Hackarun-Dragonair/dragonair-shopping |
| Site da demo | https://ronda-viva-0ek7.onrender.com (1º acesso: cerca de 1 min) |
| Versão da Missão 2 | tag `v-missao2-entrega` → https://github.com/Hackarun-Dragonair/dragonair-shopping/tree/v-missao2-entrega (pontos de segurança anteriores: `v-missao2-final`, `v-missao2-estavel`) |
| Instruções de execução | https://github.com/Hackarun-Dragonair/dragonair-shopping#como-executar |
| Resumo de 1 página | https://github.com/Hackarun-Dragonair/dragonair-shopping/blob/main/docs/RESUMO.pdf (PDF; a equipe copia à mão) · [texto](https://github.com/Hackarun-Dragonair/dragonair-shopping/blob/main/docs/RESUMO.md) · [versão detalhada](https://github.com/Hackarun-Dragonair/dragonair-shopping/blob/main/docs/RESUMO-detalhado.md) |
| Evidências (índice) | https://github.com/Hackarun-Dragonair/dragonair-shopping/blob/main/docs/evidencias/README.md |
| Avaliação da IA | https://github.com/Hackarun-Dragonair/dragonair-shopping/blob/main/docs/evidencias/modelo/resumo.md |
| QA ponta a ponta (bugs e correções) | https://github.com/Hackarun-Dragonair/dragonair-shopping/blob/main/docs/evidencias/qa/README.md |
| Declaração de uso de IA | https://github.com/Hackarun-Dragonair/dragonair-shopping/blob/main/docs/IA.md |
| Teste de usabilidade | https://github.com/Hackarun-Dragonair/dragonair-shopping/blob/main/docs/missao-2/teste-usabilidade.md ← roteiro pronto; **só deixe esta linha se o teste foi feito e anotado de verdade** (regra 6.5) |
| Pitch (roteiro, demo, FAQ) | https://github.com/Hackarun-Dragonair/dragonair-shopping/tree/main/docs/pitch |
| Missão 1 | https://github.com/Hackarun-Dragonair/dragonair-shopping/blob/main/docs/missao-1/ENTREGA-1.md |
| Vídeo do pitch | `<LINK DO VÍDEO>` |

## Checklist — entrega final (até **12h, sem prorrogação**)
Os 6 itens pedidos pela organização (instruções de sábado, copiadas em [`desafio.md`](desafio.md)):
- [ ] **1. MVP funcional:** site no ar + `main` com a versão final (testes verdes)
- [ ] **2. Repositório:** link acima, público e acessível (testar numa aba anônima)
- [ ] **3. Documentação técnica:** README — seções **"Arquitetura e tecnologias"** e "Como executar" —, `contrato.md`, `IA.md`
- [ ] **4. Instruções de execução:** README "Como executar" (instalar, configurar, executar)
- [ ] **5. Vídeo de até 90 s**, gravado por **um integrante** (só ele aparece), **sem IA** — guia em [`pitch/video-90s.md`](pitch/video-90s.md); link aberto
- [ ] **6. Resumo de 1 página** nos 8 tópicos pedidos: [`RESUMO.md`](RESUMO.md) e **[`RESUMO.pdf`](RESUMO.pdf)** (1 página)
- [ ] Nada de planta do shopping, nome de loja real, dado pessoal ou chave no repositório e no vídeo
- [ ] Depois: **check-in no shopping a partir das 16h** (todos, com o QR de identificação) — evento às 17h

## Só humanos podem fazer
A IA não pode (e não deve) fazer estas tarefas:
1. **Teste de usabilidade com 3 pessoas de fora** e o preenchimento do resultado (só dados reais).
2. **Revisar os rótulos** de `data/teste_campo.csv` (duas pessoas da equipe), para o número do teste de campo virar oficial.
3. **Testar no celular de verdade** (Android e iPhone) e anotar o modelo do aparelho em `docs/evidencias/responsividade/README.md`.
4. **Oficina de vídeo e pitch** depois do lanche das 10h: anotar o que pedirem.
5. **Aprovar e juntar os ramos no `main`** (OK do Arthur) e conferir o site no Render depois.
6. **Gravar o vídeo de até 90 s** (um integrante, sem IA — [`pitch/video-90s.md`](pitch/video-90s.md)), subir e conferir que o link abre.
7. **Enviar a entrega final até 12h** (sem prorrogação), com vídeo e resumo juntos, e **tirar print** do envio.
8. Seguir o README do zero (alguém que não escreveu o código).
9. Apresentar e responder a banca.

---

## Texto para colar — Missão 2 (enviar até 12h)

```text
Equipe Dragonair — HackaRun 2026 — Desafio 09 (Eficiência operacional e infraestrutura)
Missão 2: protótipo funcional — Ronda Viva ("Mostra o que ninguém conferiu. Registra que cuidou.")

Repositório: https://github.com/Hackarun-Dragonair/dragonair-shopping
Versão desta entrega: tag v-missao2-entrega (https://github.com/Hackarun-Dragonair/dragonair-shopping/tree/v-missao2-entrega)
Site da demo: https://ronda-viva-0ek7.onrender.com (plano grátis: o 1º acesso leva cerca de 1 min)
Como executar: README, seção "Como executar" (python wsgi.py → http://127.0.0.1:8000)
Crachás da demo (fictícios): OTTO e LIA = Gestor; RITA e CAIO = Funcionário. O QR da zona funciona sem entrar.

Fluxo principal implementado:
QR da zona → OK / Atenção / Problema → IA própria (sem internet) sugere categoria e prioridade → palavra de risco vira P1 com "Avise a brigada pelo rádio" (ninguém rebaixa) → gestor confirma → fila Aberto / Em atendimento / Resolvido → linha do tempo que não se apaga → mapa com zona cinza (ninguém conferiu no prazo) → painel por zona e equipe.

Evidências de testes e correções:
- 78 testes automáticos (pytest), rodando no GitHub em todo pull request
- QA ponta a ponta no computador e no celular: 7 problemas achados e corrigidos em commits "fix:" (docs/evidencias/qa/)
- QR de verdade: as etiquetas do site no ar foram lidas por imagem e as 11 abrem a zona certa sem login (docs/evidencias/qr/)
- Responsividade (tecnologia sorteada) em 6 larguras de tela (docs/evidencias/responsividade/)
- Avaliação da IA: teste cego n = 20 com 100% categoria, 95% prioridade e 6 de 6 P1; teste de campo n = 16 com 81% e 62% (docs/evidencias/modelo/resumo.md)
- Teste de usabilidade com 3 pessoas de fora (docs/missao-2/teste-usabilidade.md)   ← SÓ DEIXE ESTA LINHA SE O TESTE FOI FEITO E ANOTADO DE VERDADE; se não, apague antes de enviar

Uso de IA declarado: docs/IA.md
Índice de evidências: docs/evidencias/README.md
```


## Texto para colar — entrega final (até 12h)

```text
Equipe Dragonair — HackaRun 2026 — Desafio 09 (Eficiência operacional e infraestrutura)
Entrega final — Ronda Viva ("Mostra o que ninguém conferiu. Registra que cuidou.")

Repositório: https://github.com/Hackarun-Dragonair/dragonair-shopping
Site da demo: https://ronda-viva-0ek7.onrender.com (plano grátis: o 1º acesso leva cerca de 1 min)
Vídeo do pitch: <LINK DO VÍDEO>

Instruções de execução (instalar, configurar, executar): README, seção "Como executar"
  git clone https://github.com/Hackarun-Dragonair/dragonair-shopping.git
  cd dragonair-shopping
  python -m venv .venv  (ativar o venv)
  pip install -r requirements.txt
  python wsgi.py  → http://127.0.0.1:8000
  python -m pytest -q  → testes
Crachás da demo (fictícios): OTTO e LIA = Gestor; RITA e CAIO = Funcionário. O QR funciona sem entrar.

Documentação:
- Resumo de 1 página: docs/RESUMO.md
- Uso de IA (desenvolvimento e dentro da solução): docs/IA.md
- Nomes, regras e rotas: docs/contrato.md
- Pitch, demo e perguntas: docs/pitch/

Evidências das missões: docs/evidencias/README.md (índice por missão)
- Missão 1: docs/missao-1/ENTREGA-1.md
- Missão 2: QA com correções, responsividade, avaliação da IA, teste de usabilidade   ← tire "teste de usabilidade" se ele não foi feito de verdade
- Entrega final (instruções de sábado): MVP no ar, repositório, documentação técnica (README: Arquitetura e tecnologias), instruções de execução, vídeo de até 90 s e resumo de 1 página (docs/RESUMO.pdf)

Tecnologia: Python, Flask, SQLite, Bootstrap local, JavaScript, scikit-learn (modelo próprio, sem internet), pytest. Tecnologia sorteada: Responsividade.
Dados, zonas e pessoas da demo são fictícios. O mapa é um desenho da equipe, não a planta do shopping.
```

## Texto para colar — vídeo + resumo (se o formulário pedir separado; tudo até 12h)

```text
Equipe Dragonair — Desafio 09 — Ronda Viva
Vídeo do pitch: <LINK DO VÍDEO>
Resumo (1 página, PDF): https://github.com/Hackarun-Dragonair/dragonair-shopping/blob/main/docs/RESUMO.pdf
```
Se pedirem arquivo, anexe `docs/RESUMO.pdf`; se pedirem texto, copie `docs/RESUMO.md`.
