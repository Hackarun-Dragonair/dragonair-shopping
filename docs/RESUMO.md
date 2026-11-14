# Ronda Viva — resumo para os avaliadores
**Equipe Dragonair · HackaRun 2026 · Desafio 09: Eficiência operacional e infraestrutura**

**1. Nome do projeto**
Ronda Viva — *"Mostra o que ninguém conferiu. Registra que cuidou."*

**2. Problema identificado**
- A administração não sabe em que estado cada área do shopping está agora, nem quando foi conferida pela última vez.
- A ronda vive numa folha de papel que qualquer um assina depois; os problemas chegam soltos pelo rádio, sem prioridade nem dono, e se perdem na troca de turno.
- Quando algo dá errado, não há registro confiável do que foi feito.

**3. Público-alvo**
- **Equipe de campo** (limpeza, manutenção, segurança): registra a ronda pelo celular.
- **Supervisores e gestão de operações**: acompanham, priorizam e cobram por zona e equipe.
- **Frequentadores e lojistas**: ambientes conferidos e problemas resolvidos mais rápido.

**4. Solução proposta**
Cada zona do shopping tem um **QR**. O funcionário aponta o celular e toca **OK, Atenção ou Problema**. O problema, escrito do jeito dele, recebe uma **sugestão de categoria e prioridade** de uma IA própria; o gestor confirma. O **mapa fica cinza** onde ninguém conferiu no prazo, e cada ocorrência tem uma **linha do tempo que não se apaga**.

**5. Descrição do produto (MVP)**
- **Tela do QR (celular, sem instalar nada):** OK / Atenção / Problema em poucos toques; botões prontos ("vaso entupido", "quadro aberto").
- **IA local:** sugere categoria, prioridade e equipe; quando fica entre duas opções, pergunta "É mais X ou Y?".
- **Regra de segurança acima da IA:** fumaça, fogo, gás, choque ou pessoa presa → prioridade máxima (P1) e "Avise a brigada pelo rádio". Ninguém rebaixa.
- **Perfis:** funcionário (ronda, assumir, resolver) e gestor (confirmar, painel, editar mapa, imprimir etiquetas QR).
- **Fila** Aberto → Em atendimento → Resolvido, atualizando sozinha; **mapa** por piso com formas de shopping; **painel** com zonas no prazo, tempo de solução e reincidência — **por zona e equipe, nunca por pessoa**.
- **Demo online:** https://ronda-viva-0ek7.onrender.com (crachás fictícios: OTTO = gestor, RITA = funcionária).

**6. Tecnologias utilizadas**
Python, Flask, SQLite, HTML/CSS (Bootstrap local), JavaScript, scikit-learn (IA), segno (QR), pytest (78 testes automáticos), GitHub Actions, Render. Site responsivo: celular, tablet e computador.

**7. Diferencial e inovação**
- **Mostra o lugar, não só a tarefa:** a zona esquecida fica cinza no mapa antes de o cliente reclamar.
- **IA usada com senso crítico:** só sugere, mostra a dúvida, e a segurança fica numa regra fixa que ela não desfaz. Medida com honestidade: no teste cego (20 frases), palavras-chave pegavam 4 de 6 riscos; com a IA, 6 de 6. Com frases reais o acerto de categoria cai para 81% — por isso uma pessoa sempre confirma.
- **Registro que não se apaga:** o banco bloqueia alterar ou apagar a linha do tempo.

**8. Viabilidade e aplicação no shopping**
- Custo baixo: etiquetas impressas e o celular que a equipe já tem; sem API paga, sem aparelho novo.
- Piloto sugerido: **30 dias** nos sanitários e na praça de alimentação, medindo zonas no prazo e tempo de solução.
- Próximos passos: revisar as palavras de risco com a brigada, cadastro de aparelhos autorizado pelo gestor, testar a IA com relatos reais.

**Links:** repositório https://github.com/Hackarun-Dragonair/dragonair-shopping · como executar: `README.md` · uso de IA declarado: `docs/IA.md` · evidências: `docs/evidencias/`
