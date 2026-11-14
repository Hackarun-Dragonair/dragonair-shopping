# Perguntas difíceis da banca (e respostas honestas)

Regra de ouro: **só afirmar o que dá para mostrar funcionando.** O resto é "próximo passo".
Respostas curtas. Se não souber, diga: "Não medimos isso ainda; o próximo passo seria…".

## Técnica

**1. Por que Flask e SQLite, e não algo maior?**
Porque é simples, roda em qualquer notebook e a equipe consegue explicar cada linha. SQLite é um banco num arquivo só, sem servidor para instalar. Para um piloto num shopping é suficiente; para vários shoppings ao mesmo tempo, trocaríamos por um banco servidor (ex.: PostgreSQL).

**2. E se duas pessoas registram ao mesmo tempo? Aguenta?**
Num shopping, são poucos registros por minuto, e o SQLite dá conta. No Render usamos um processo só, de propósito, por causa do SQLite. Não fizemos teste de carga; seria um passo antes de produção.

**3. Funciona sem internet?**
A IA e o visual estão dentro do projeto: o sistema roda num notebook sem internet, só com uma rede local (até o hotspot do celular). Se o celular perde a rede no meio do registro, a tela avisa "Não enviado: sem conexão" e a pessoa tenta de novo. A API já tem um endereço para reenviar o que ficou guardado (`/fila-envio`), mas a tela ainda não guarda sozinha. Isso é próximo passo.

## IA

**4. Por que IA num sistema de 3 botões?**
Os botões OK e Atenção não usam IA. Ela entra no "Problema": quem viu escreve do jeito dele e não sabe se é Hidráulica ou Elétrica, nem se é urgente. A IA transforma a frase em categoria, prioridade e equipe. Esses dados viram a fila e o painel.

**5. Qual o acerto real?**
No teste cego (20 frases escritas e rotuladas à mão pela equipe, que o modelo nunca viu): 100% na categoria, 95% na prioridade e 6 de 6 casos P1 marcados como P1. Só regras de palavras-chave ficariam em 90% e 40%. **Mas** o teste é pequeno e foi escrito pela mesma equipe do treino. Com 16 frases reais do campo (rótulos ainda a revisar), cai para 81% e 62%. Esse é o número mais perto da realidade.

**6. E se a IA errar?**
Ela não decide. Mostra a confiança e, abaixo de 50%, pergunta "É mais X ou Y?" com dois botões quando ela fica entre duas categorias; sem segunda opção, avisa "IA em dúvida, confira". Quem registra pode mudar, e o gestor confirma ou corrige. A correção fica na linha do tempo. E a regra de risco fica acima dela.

**7. Por que não usaram ChatGPT ou outra IA pronta?**
Custaria por uso, precisaria de internet e mandaria texto do shopping para fora. O nosso modelo roda dentro do servidor, responde na hora, não custa nada por uso e tem acerto que conseguimos medir e mostrar. Usamos IAs prontas (Claude, Cursor, Gemini) só para **desenvolver**, tudo declarado em `docs/IA.md`.

**8. "Fumaça" na lanchonete não vira alarme falso?**
Pode virar, e é de propósito. Fumaça na praça de alimentação pode ser incêndio. O sistema só mostra "Avise a brigada pelo rádio" e marca P1; quem verifica e decide é a brigada. O sistema nunca chama ninguém sozinho.

## Testes

**9. Como vocês testaram?**
- **73 testes automáticos** (pytest), rodando no GitHub em todo pull request.
- **QA ponta a ponta** no computador e no celular: achamos 7 problemas e corrigimos em 8 commits `fix:` (`docs/evidencias/qa/`).
- **Responsividade** em 6 larguras de tela, de 375 px a 1920 px (`docs/evidencias/responsividade/`).
- **Avaliação da IA** com teste cego e teste de campo (`docs/evidencias/modelo/`).
- **Teste com 3 pessoas de fora:** roteiro em `docs/missao-2/teste-usabilidade.md` (resultado anotado pela equipe no sábado; só cite à banca depois de feito).

## Segurança e dados

**10. O QR prova que a pessoa esteve lá?**
Não totalmente: um QR fixo pode ser fotografado. Ele **registra** a conferência com hora e torna a ronda visível. QR com código que muda sozinho está no roadmap.

**11. Qualquer cliente pode ler o QR e registrar algo falso?**
Hoje, sim: o QR funciona sem entrar, para o aparelho compartilhado da equipe. O registro aparece como "Campo (sem crachá)" e o gestor confirma antes de tratar. Para produção, a API já tem celular autorizado + crachá (`/dispositivos` e `/crachas/entrar`); faltaria exigir isso na tela.

**12. O login não tem senha?**
No protótipo, não: os crachás OTTO, LIA, RITA e CAIO são fictícios, para a banca testar. O que existe de verdade é a separação de perfis: funcionário não abre o painel nem o editor, e só o gestor confirma a sugestão da IA. Em produção: senha ou crachá físico + celular autorizado.

**13. Vocês vigiam funcionários? E dados pessoais?**
Não. Os indicadores são só por **zona e equipe**, nunca por pessoa. Todos os nomes da demo são inventados. A planta do shopping não está no sistema nem no repositório: o mapa é um desenho nosso em blocos. O editor aceita uma imagem de fundo, mas ela fica só no servidor, fora do Git.

## Viabilidade e custo

**14. Quem garante que vão usar? Dá para implantar?**
O QR substitui a folha de papel que já existe, e não exige hardware novo: QR impresso (o sistema gera o PDF das etiquetas), o celular da equipe e um navegador. O plano é um piloto de 30 dias em sanitários e praça de alimentação. A adesão real só se mede nesse piloto.

**15. Quanto custa?**
O protótipo custou R$ 0 (bibliotecas gratuitas, hospedagem grátis). Em produção: hospedagem simples e impressão das etiquetas. Não há custo de IA por uso. Retorno financeiro não medimos; não prometemos número que não medimos.

## Bônus: o que é de verdade e o que é simulado?

| Funciona de verdade | Simulado ou ainda não feito |
|---|---|
| QR → OK / Atenção / Problema | Shopping, zonas, pessoas e frases: tudo fictício |
| IA sugerindo categoria e prioridade, com confiança | Crachás sem senha (protótipo) |
| Regra P1 + aviso da brigada; gestor não consegue rebaixar | Mapa em blocos desenhado pela equipe (não é a planta) |
| Fila, linha do tempo que não se apaga, dossiê | Rótulos do teste de campo ainda sugeridos por IA, a revisar |
| Mapa com zona cinza, atualizando a cada 5 s; painel; Sobre a IA | Guardar e reenviar sozinho quando a rede cai (só existe na API) |
| Editor de mapa, etiquetas QR em PDF, alertas por zona | QR com código que muda, retreino automático da IA |
| Easter Egg da sexta-feira 13 | No Render grátis, os dados voltam ao exemplo a cada reinício |
