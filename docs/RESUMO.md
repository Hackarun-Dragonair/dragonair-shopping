# Ronda Viva — resumo

**Equipe Dragonair · HackaRun 2026 · Desafio 09: Eficiência operacional e infraestrutura**
*"Mostra o que ninguém conferiu. Registra que cuidou."*

## O problema
A administração do shopping não sabe em que condição cada ambiente está agora, nem quando foi conferido pela última vez. A ronda vive numa folha de papel que qualquer um assina depois. Os problemas chegam soltos pelo rádio, sem prioridade nem dono, e se perdem na troca de turno. Quando algo dá errado, não há registro confiável do que foi feito.

## A solução
Um site responsivo (celular, tablet e computador, sem instalar nada) para a ronda operacional:
- cada zona tem um **QR**; o funcionário aponta o celular e toca **OK, Atenção ou Problema**;
- uma **IA própria, sem internet**, sugere a categoria e a prioridade do problema; o gestor confirma;
- o **mapa fica cinza** onde ninguém conferiu no prazo;
- cada ocorrência tem uma **linha do tempo que não se apaga**.

## Como funciona
1. **Funcionário (celular):** lê o QR da zona. Não precisa entrar com crachá. Toca OK, Atenção ou Problema. No Problema, escreve do seu jeito ou toca um botão pronto ("Vaso entupido", "Quadro aberto"...).
2. **IA:** sugere categoria (Hidráulica, Elétrica, Climatização, Limpeza, Segurança, Estrutura), prioridade (P1 a P4) e equipe. Mostra a confiança; quando fica entre duas categorias, pergunta "É mais X ou Y?" (sem segunda opção e abaixo de 50%, avisa "IA em dúvida, confira"). A pessoa pode mudar antes de registrar.
   Quando a IA fica em dúvida entre duas categorias, a tela da zona faz uma pergunta de desempate.
3. **Regra de risco acima da IA:** fumaça, fogo, choque ou pessoa presa → **P1** e "Avise a brigada pelo rádio". Ninguém rebaixa (nem a IA, nem o gestor). O sistema não chama ninguém sozinho.
4. **Gestor (computador):** entra com crachá, confirma ou corrige a sugestão. A ocorrência vai para a **fila** (Aberto → Em atendimento → Resolvido) da equipe certa. A fila se atualiza sozinha a cada 5 s.
5. **Linha do tempo:** registro, sugestão da IA, aviso de risco, quem assumiu, confirmação e solução, cada um com hora. O banco bloqueia apagar ou alterar esses registros. Vira um dossiê para imprimir.
6. **Mapa e painel:** o mapa mostra o estado de cada zona e atualiza sozinho a cada 5 s. O painel mostra % de zonas no prazo, zonas sem conferência, tempo médio de solução, reincidência e o acerto da IA. Tudo por zona e equipe, **nunca por pessoa**.

Também existe: editor de mapa (o gestor envia uma imagem de fundo e pinta bloquinhos por zona), etiquetas QR em PDF, alertas por zona, e o Easter Egg da sexta-feira 13 (um gato preto se esconde na zona mais esquecida).

## Diferencial
- **Mostra o que NÃO aconteceu.** Folha, rádio e apps de checklist registram a tarefa feita. A zona cinza mostra onde ninguém olhou.
- **IA que funciona sem internet e foi medida com honestidade**, com uma regra de segurança que ela não consegue desfazer.
- **Registro que não se apaga:** o shopping consegue mostrar que cuidou.

## Uso crítico de IA
**Na solução:** modelo feito pela equipe com scikit-learn (TF-IDF de pedaços de 3 a 5 letras + regressão logística), treinado com 145 frases fictícias. Roda dentro do servidor, sem API paga.

**Como medimos** (`python -m app.avaliar` → `docs/evidencias/modelo/resumo.md`):

| Teste | n | Categoria | Prioridade | Recall de P1 |
|---|---|---|---|---|
| Teste cego (rótulos humanos, sem IA) — só regras de palavras | 20 | 90% | 40% | 67% (4 de 6) |
| Teste cego — **modelo + regra dura (o que o sistema mostra)** | 20 | **100%** | **95%** | **100% (6 de 6)** |
| Teste de campo (frases reais, rótulos ainda a revisar) | 16 | 81% | 62% | 100% (1 de 1) |

"Recall de P1" = dos casos que eram P1 de verdade, quantos o sistema marcou como P1.

**Limite (sendo honestos):** o teste cego é pequeno (20 frases) e foi escrito pela mesma equipe do treino. O 100% mostra que o modelo aprendeu o nosso jeito de escrever, não que vai acertar 100% no shopping. Com frases reais o acerto cai (81% e 62%), e esses rótulos ainda precisam de revisão humana. No teste de campo, o modelo sozinho deu P2 para "sensor de fumaça piscando"; foi a regra dura que garantiu o P1. Por isso a IA só sugere e o gestor confirma.

**No desenvolvimento:** Claude, Cursor e Gemini ajudaram em ideias, código, telas, testes e documentos. Tudo declarado e revisado pela equipe em `docs/IA.md`.

## Tecnologia
Python 3.11+ · Flask · Jinja2 · SQLite · Bootstrap 5 (local, sem internet) · JavaScript puro · scikit-learn · segno (QR) · pytest (73 testes) · GitHub Actions (testes em todo PR) · Render (link público).
Tecnologia sorteada: **Responsividade** — testada em 6 larguras, de 375 px a 1920 px (`docs/evidencias/responsividade/`).

## Links
- **Repositório:** https://github.com/Hackarun-Dragonair/dragonair-shopping (versão estável da Missão 2: tag `v-missao2-estavel`)
- **Demo online:** https://ronda-viva-0ek7.onrender.com (grátis: o 1º acesso leva cerca de 1 min; dados de exemplo voltam a cada reinício)
- **Como executar:** `README.md`, seção "Como executar"
- **Evidências:** `docs/evidencias/` · **Uso de IA:** `docs/IA.md`
- **Prova de que o QR das etiquetas abre a zona certa:** [`docs/evidencias/qr/`](evidencias/qr/README.md)
- **Crachás da demo (fictícios):** OTTO e LIA = Gestor; RITA e CAIO = Funcionário. O QR funciona sem entrar.

## Equipe
**Dragonair** — HackaRun 2026, UniCatólica. Todos os dados, zonas e usuários da demo são fictícios. O mapa é um desenho da equipe, não a planta do shopping.
