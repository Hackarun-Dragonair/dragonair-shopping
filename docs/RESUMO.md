# Equipe Dragonair · Desafio 09

**1. Nome do projeto**
Ronda Viva: mostra a área que ninguém conferiu.

**2. Problema identificado**
- A gestão não sabe como cada área está agora, nem quando foi vista.
- A ronda no papel não prova que alguém passou na hora.
- Problemas chegam pelo rádio, sem prioridade nem responsável, e se perdem na troca de turno.

**3. Público-alvo**
- Equipe de campo: limpeza, manutenção, segurança.
- Supervisores e gestão de operações.
- Beneficiados: clientes e lojistas.

**4. Solução proposta**
- Cada área tem uma etiqueta QR.
- O funcionário lê com o celular e marca OK, Atenção ou Problema.
- Área sem conferência no prazo fica cinza no mapa.
- Cada problema vira chamado com equipe responsável e histórico, visível até ser resolvido, mesmo na troca de turno.

**5. Descrição do produto (MVP)**
- Abre no celular, sem instalar aplicativo.
- IA treinada pela equipe sugere tipo e urgência; o gestor confirma. Na dúvida, oferece duas opções.
- Fumaça, fogo, gás, choque ou pessoa presa: urgência máxima e a tela pede para avisar a brigada. Ninguém rebaixa.
- Mapa por andar e etiquetas para imprimir.
- Painel por área e equipe, nunca por pessoa.

**6. Tecnologias utilizadas**
Python, Flask, SQLite, HTML, CSS, JavaScript e scikit-learn (IA). 78 testes automáticos.

**7. Diferencial e inovação**
- Acompanha o lugar, não só a tarefa.
- A regra fixa garante o mínimo, a IA pega o que ela deixa passar e a pessoa decide.
- Em 20 frases escritas pela equipe, só palavras-chave acharam 4 de 6 casos urgentes; com a IA, 6 de 6.
- O histórico fica registrado: o sistema não deixa apagar.

**8. Viabilidade e aplicação no shopping**
- Custo baixo: etiquetas, celulares que já existem e um computador do shopping ou servidor simples. IA sem custo por uso.
- Piloto de 30 dias em banheiros e praça de alimentação, medindo áreas em dia e tempo de solução.
- A brigada revisa as palavras de risco.

Repositório: Hackarun-Dragonair/dragonair-shopping
