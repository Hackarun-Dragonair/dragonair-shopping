# Ronda Viva — Pitch e perguntas difíceis
**Equipe Dragonair · HackaRun 2026** · Use este texto para todos defenderem o projeto do mesmo jeito.

> Regra de ouro: **no pitch, só prometemos o que vamos mostrar funcionando.** O resto é "próximo passo".

## Pitch (cerca de 2 minutos)
**A cena.** Sábado, 12h40, praça de alimentação lotada. Alguém conferiu o banheiro do 2º piso na última hora? Hoje a resposta é uma folha de papel que qualquer um assina depois — ou a reclamação do cliente. E se alguém escorrega no piso molhado, é o shopping que precisa demonstrar que sinalizou.

**O problema.** A administração não sabe em que condição cada ambiente está agora nem quando foi conferido pela última vez. Os problemas viram texto solto no rádio e se perdem na troca de turno.

**A solução — Ronda Viva: "Mostra o que ninguém conferiu. Registra que cuidou."**

1. **Um QR por zona**, numa placa de aviso, sempre no mesmo tipo de lugar. O encarregado aponta a câmera do celular da equipe e toca **OK, Atenção ou Problema**.
2. **Uma IA que traduz a frase de quem viu em quem deve ir olhar.** "Tá pingando do teto" → Hidráulica, prioridade 2, equipe de manutenção. Ela roda **sem internet**, foi treinada por nós e o acerto foi medido num teste cego. **O supervisor confirma.**
3. **Segurança em primeiro lugar.** Palavra de risco — fumaça, fogo, choque, pessoa presa — **sempre** mostra "avise a brigada pelo rádio". O sistema nunca rebaixa um risco e nunca aciona ninguém sozinho.
4. **Mapa vivo.** As zonas ficam **cinza quando ninguém conferiu no prazo** — mostramos o que **não** aconteceu, coisa que a folha de papel e os apps de checklist não mostram.
5. **Linha do tempo que não se apaga.** Cada passo de cada problema fica registrado com hora e vira um resumo para imprimir.

**Responsividade:** celular na ronda, tablet na sala de controle, computador na gestão — um site, sem instalar nada.

**Fechamento:** *"Hoje, a ronda registra só que alguém assinou uma folha. A Ronda Viva mostra o que ninguém conferiu, manda a pessoa certa com uma IA que funciona sem internet e registra cada passo do cuidado. O shopping deixa de reagir à reclamação e passa a prevenir."*

## O que mostramos na demo × próximos passos
| Mostramos funcionando | Próximos passos (dizer que é roadmap) |
|---|---|
| QR → OK / Atenção / Problema | Celular autorizado + código do crachá |
| IA sugere categoria, prioridade e equipe (sem internet) | Modo totalmente offline (sem sinal) |
| Alerta de brigada para palavras de risco | QR com código rotativo |
| Mapa com zona cinza (3 telas responsivas) | Editor de mapa por blocos com planta de fundo |
| Fila de problemas com linha do tempo | Retreino da IA com as correções do supervisor |
| Painel + acerto da IA medido | Alertas de "OK divergente" e piloto real de 30 dias |

## Perguntas difíceis e respostas
**Uso e adoção**

- **Quem garante que vão usar?** O QR substitui a folha de papel que já existe. No início, quem usa é o encarregado (1 pessoa por turno). A adesão real só se mede num piloto — é o próximo passo.
- **E pessoas leigas?** 3 botões grandes, botões prontos para os problemas comuns e ditado pelo teclado. Fizemos teste cronometrado com pessoas de fora (resultado nas evidências).
- **Funcionário novo não sabe onde está o QR.** O QR fica sempre no mesmo tipo de lugar por tipo de zona, e a lista de zonas mostra onde ele está.
- **E se ele marcar OK sem olhar?** Nenhum sistema elimina isso, nem a folha. O registro com hora e a zona cinza tornam a ronda visível para o supervisor; alertas de "OK divergente" estão no roadmap.

**QR e segurança**

- **O QR prova que a pessoa esteve lá?** Não totalmente — um QR fixo pode ser fotografado. Ele **registra a conferência** e torna a ronda auditável; QR com código rotativo está no roadmap.
- **Cliente pode registrar algo?** Na versão de produção, só celulares autorizados pelo supervisor registram. Na demo usamos um usuário fictício.
- **E se arrancarem o QR?** A zona fica cinza (ninguém consegue conferir) e o supervisor vê; dá para registrar pela lista de zonas.
- **Vocês monitoram pessoas?** Não. Indicadores são por **zona e equipe**, nunca por pessoa.

**IA**

- **Por que IA num sistema de 3 botões?** Os botões não usam IA. Ela entra quando alguém descreve um problema: quem viu não sabe se é hidráulica ou ar-condicionado, nem se é urgente. A IA transforma a frase em categoria, prioridade e equipe — e esses dados viram os indicadores.
- **E se ela errar?** Ela não decide: sugere, mostra as 2 opções mais prováveis quando está em dúvida, e o supervisor confirma. Para qual equipe vai é definido por uma tabela do gestor.
- **Fumaça da lanchonete vira alarme falso?** Pode virar — e isso é de propósito. Fumaça na praça de alimentação pode ser incêndio. O sistema nunca rebaixa um risco; a brigada verifica e decide.
- **Qual o acerto?** Medido num teste cego, com frases escritas à mão pela equipe e por pessoas de fora, guardadas antes do treino, e comparado com regras de palavra-chave. O número real está na tela "Sobre o modelo". Os dados são sintéticos; o ajuste fino viria no piloto.

**Conexão e tecnologia**

- **Sem internet?** A IA roda no nosso servidor, sem depender de serviço externo. A demonstração roda no notebook, sem depender do Wi-Fi. Modo totalmente offline no celular é roadmap.
- **É aplicativo?** É um site que vira ícone na tela inicial. Funciona em qualquer celular, sem loja.

**Negócio e implantação**

- **O que o gestor ganha?** Ver onde ninguém olhou, encaminhamento certo sem depender do rádio, problema resolvido antes do pico e um registro com hora de cada passo.
- **É difícil implantar?** Não exige hardware novo: QR impresso, o celular da equipe e um navegador. O plano é um piloto em sanitários e praça de alimentação.
- **Vale o investimento?** Não há custo de IA por uso. O retorno real só se mede no piloto — não prometemos número que não medimos.
