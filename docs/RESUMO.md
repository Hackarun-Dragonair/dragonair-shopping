# Ronda Viva · Equipe Dragonair · Desafio 09

**1. Nome do projeto**
Ronda Viva: mostra a área que ninguém conferiu.

**2. Problema identificado**
- A gestão não sabe como cada área está agora, nem quando foi vista.
- A ronda fica no papel, que pode ser assinado depois.
- Problemas chegam pelo rádio, sem prioridade nem dono, e se perdem na troca de turno.

**3. Público-alvo**
- Equipe de campo: limpeza, manutenção, segurança.
- Supervisores e gestão de operações.
- Beneficiados: clientes e lojistas.

**4. Solução proposta**
- Cada área tem uma etiqueta QR.
- O funcionário lê com o celular e marca OK, Atenção ou Problema.
- Área sem conferência no prazo fica cinza no mapa.
- Cada problema vira chamado com dono e histórico, que passa de um turno para o outro sem se perder.

**5. Descrição do produto (MVP)**
- Abre no celular, sem instalar aplicativo.
- IA própria sugere tipo e urgência; o gestor confirma. Na dúvida, mostra duas opções.
- Fumaça, fogo, gás, choque ou pessoa presa: urgência máxima e a tela pede para avisar a brigada. Ninguém rebaixa.
- Chamados: aberto, em atendimento, resolvido.
- Mapa por andar e etiquetas para imprimir.
- Painel por área e equipe, nunca por pessoa.

**6. Tecnologias utilizadas**
Python, Flask, SQLite, HTML, CSS, JavaScript e scikit-learn (IA). 78 testes automáticos.

**7. Diferencial e inovação**
- Acompanha o lugar, não só a tarefa.
- A IA só sugere; a pessoa decide e a regra de segurança vem antes.
- Em 20 frases de teste, palavras-chave acharam 4 de 6 casos graves; com a IA, 6 de 6.
- O histórico fica registrado: o sistema não deixa apagar.

**8. Viabilidade e aplicação no shopping**
- Custo baixo: etiquetas de papel e celulares que já existem. Sem pagar por uso de IA.
- Piloto de 30 dias em banheiros e praça de alimentação, medindo áreas em dia e tempo de solução.
- Depois: revisar palavras de risco com a brigada.

Repositório: Hackarun-Dragonair/dragonair-shopping
