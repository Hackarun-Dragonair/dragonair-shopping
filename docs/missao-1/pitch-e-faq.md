# Ronda Viva — Pitch e perguntas difíceis
**Equipe Dragonair · HackaRun 2026** · Use este texto para todos defenderem o projeto do mesmo jeito.

## Pitch (cerca de 2 minutos)
**A cena.** Sábado, 12h40, praça de alimentação lotada. Alguém conferiu o banheiro do 2º piso na última hora? Hoje a resposta é uma folha de papel que qualquer um assina depois — ou a reclamação do cliente. E se alguém escorrega no piso molhado, o shopping precisa **provar** que sinalizou: há casos públicos de condenação de R$ 5 mil a R$ 30 mil por falta dessa prova.

**O problema.** A administração não sabe em que condição cada ambiente está agora nem quando foi realmente conferido. Os problemas viram texto solto no rádio e se perdem na troca de turno.

**A solução — a folha de papel vira prova.**

1. **Um QR por zona**, numa placa de aviso, sempre no mesmo tipo de lugar. O encarregado aponta a câmera do celular da equipe e toca **OK, Atenção ou Problema**. Só o QR, no local, marca "OK".
2. **Uma IA que traduz a frase de quem viu em quem deve ir olhar.** "Tá pingando do teto" → Hidráulica, prioridade 2, equipe de manutenção. Ela roda sem internet, foi treinada e medida por nós; em dúvida, pergunta; o supervisor confirma.
3. **Segurança sem alarme falso.** "Fumaça"? O sistema pergunta de onde vem. Equipamento elétrico → "avise a brigada pelo rádio". Quem decide chamar os bombeiros é a brigada.
4. **Prova de que cuidou.** Cada passo fica registrado com hora e vira o dossiê do incidente.
5. **Mapa vivo.** As zonas ficam **cinza quando ninguém conferiu no prazo** — mostramos o que **não** aconteceu. O mapa é feito de blocos e muda quando o shopping muda.

**Responsividade:** celular na ronda, tablet na sala de controle, computador na gestão — um site, sem instalar nada.

**Fechamento:** *"Hoje, a ronda prova só que alguém assinou uma folha. A Ronda Viva mostra o que ninguém conferiu, manda a pessoa certa com uma IA que funciona até sem internet e guarda a prova de que o shopping cuidou. O shopping deixa de reagir à reclamação e passa a prevenir."*

---
## Perguntas difíceis e respostas
**Uso e adoção**

- **Quem garante que vão usar?** O QR substitui a folha de papel que já existe — não é tarefa nova. No início, quem usa é o encarregado (1 pessoa por turno). O registro protege o funcionário ("eu passei às 12h10"). A adesão é medida no piloto de 30 dias.
- **E pessoas leigas?** 3 botões grandes, botões prontos para os problemas comuns, ditado pelo teclado, cartaz de 3 figuras e primeira ronda acompanhada.
- **Funcionário novo não sabe onde está o QR.** O QR fica sempre no mesmo tipo de lugar por tipo de zona, e "Minha ronda" mostra a próxima zona com foto do local do QR.
- **E se ele marcar OK sem olhar?** O sistema não elimina isso, mas mostra: "OK divergente" (supervisor achou problema logo depois) e "semana sem achados". Apontar problema não gera trabalho para quem apontou — vai para a equipe certa — e conta como mérito da equipe.

**QR e segurança**

- **Cliente pode registrar algo?** Não. Só celulares autorizados pelo supervisor registram; para os outros aparece "Este código é da equipe".
- **E se trocarem ou arrancarem o QR?** A página verdadeira mostra o nome da zona; QR arrancado faz a zona ficar cinza; a ronda continua pela lista de zonas e o sistema avisa para repor, com foto do local.
- **Registro à distância?** Só o QR marca "OK". Problema pode ser relatado de qualquer lugar, com o selo "relatado à distância".
- **Quem fez cada registro?** Cada registro tem dono (código do crachá) para auditoria. Os indicadores são por zona e equipe, nunca ranking de pessoas.
- **Demitido / PIN emprestado / esquecido?** Aparelho e pessoa são separados: o supervisor desativa o código em 1 clique; a sessão expira quando o celular fica parado; inconsistências são sinalizadas; a identificação é o número do crachá.

**IA**

- **Por que IA num sistema de 3 botões?** Os botões não usam IA. Ela entra quando alguém descreve um problema: quem viu não sabe se é hidráulica ou ar-condicionado, nem se é urgente. A IA traduz a frase em categoria, prioridade e equipe — e esses dados alimentam os indicadores.
- **Quem treina?** Nós entregamos o modelo treinado com o vocabulário de operação de shopping. Cada correção do supervisor vira treino; uma versão nova só entra se acertar mais que a atual.
- **E se ela errar?** Ela não decide: sugere, pergunta quando está em dúvida, e o supervisor confirma. Para qual equipe vai é definido por uma tabela do gestor.
- **Fumaça da lanchonete vira incêndio?** Não. O sistema pergunta de onde vem antes de qualquer alerta, e nunca aciona ninguém sozinho.
- **Qual o acerto?** Medido num teste separado, escrito à mão pela equipe e por pessoas de fora, comparado com regras de palavra-chave. Mostramos o número real na tela "Sobre o modelo".

**Conexão e tecnologia**

- **Sem internet no subsolo?** O registro fica salvo no celular com a hora certa e sobe sozinho depois. O alerta de risco funciona offline. A IA não depende de internet.
- **É aplicativo?** É um site que vira ícone na tela inicial. Funciona em qualquer celular, sem loja e sem instalação.
- **E o mapa quando a planta muda?** As zonas são feitas de blocos: dividir ou juntar é reagrupar blocos, e o histórico da zona antiga fica guardado.

**Negócio e implantação**

- **O que o gestor ganha?** Ver onde ninguém olhou, encaminhamento certo sem depender do rádio, problema resolvido antes do pico, relatório por contrato e registro que ajuda a demonstrar diligência.
- **É difícil implantar?** O piloto roda em 1 dia: modelos prontos de zona, etiquetas em PDF, equipe por planilha, celular ativado por QR, e a instalação das etiquetas já é a primeira ronda.
- **Vale o investimento?** Não exige hardware novo nem custo de IA por uso. Uma única indenização evitada paga meses de sistema. O piloto de 30 dias mede o retorno real.
