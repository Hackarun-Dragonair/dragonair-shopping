# Checklist de sábado 14/11

> Na dúvida entre dois prazos, vale o mais cedo. Textos prontos para colar e links: [`../ENTREGA.md`](../ENTREGA.md).

## O que levar
- [ ] Notebook **carregado** + carregador + extensão (tomada é disputada)
- [ ] Celular com bateria + cabo (é o celular da demo e o hotspot do plano B)
- [ ] Projeto **já instalado e testado** no notebook (`python -m pytest -q` passando) — não dependa do Wi-Fi do evento para instalar
- [ ] Etiqueta QR impressa da **Área técnica L2** (gerada pelo PDF de etiquetas aberto pelo IP do notebook; ver README, "Usar no celular")
- [ ] Papel e caneta para a folha do teste de usabilidade (ou o arquivo aberto)
- [ ] Fone com microfone ou um lugar silencioso para gravar a voz

## Horários

| Hora | O que fazer | Pronto quando… |
|---|---|---|
| **8h** | Chegar, ligar o notebook, abrir o site do Render para acordar, rodar `python -m pytest -q` | Testes passando e site respondendo |
| **8h15–9h15** | **Teste de usabilidade com 3 pessoas de fora**, seguindo [`../missao-2/teste-usabilidade.md`](../missao-2/teste-usabilidade.md): mesmo texto para todos, 4 tarefas, cronômetro, **sem anotar nome** | 3 folhas preenchidas + prints (sem rosto, sem nome) |
| **9h15–9h35** | Passar o resultado para a tabela "Resumo" do mesmo arquivo. Corrigir **1 coisa** que travou (commit `fix:`) ou anotar o que seria corrigido | Tabela preenchida com dados reais; prints em `docs/evidencias/` |
| **10h** | Lanche. Conferir se a organização mudou algo nas instruções (aviso de sexta à noite: **sábado não tem missão especial**; salas abertas das 8h às 13h; instruções finais e mentoria do vídeo e do pitch de 5 min) | Equipe sabe se mudou algo |
| **após o lanche (~10h30, 30 min)** | **Mentoria** do vídeo de 90 s e do pitch final de 5 min. Anotar o que pedirem e ajustar o vídeo. Em paralelo, alguém que **não** escreveu o código segue o README "Como executar" do zero | Anotações da mentoria |
| **11h** | **Código congelado.** Depois disso, nada de mudança no código; só texto | `main` com tudo e testes passando |
| **10h45–11h30** | **Gravar o vídeo de até 90 s** com um integrante falando para a câmera (sem IA): [`video-90s.md`](video-90s.md). Subir (YouTube não listado ou Drive aberto) | Link abrindo numa aba anônima |
| **até 11h45** | **Entrega final completa** (os 6 itens de [`../ENTREGA.md`](../ENTREGA.md), com vídeo e [`../RESUMO.pdf`](../RESUMO.pdf)). Prazo **12h sem prorrogação**: não deixar para o último minuto. Print do envio → `docs/evidencias/` | Print do comprovante salvo |
| **16h** | **Check-in no Capim Dourado Shopping** (todos, com o QR de identificação; recebe pulseira) | Todos com pulseira |
| **17h** | **Final no Capim Dourado (só as 7 melhores equipes): pitch de 5 min.** Demo ao vivo pelo notebook com `SEXTA13=1 python wsgi.py`; Render como reserva. Roteiro: [`pitch-5min.md`](pitch-5min.md) | Demo ensaiada uma vez antes |

## O que conferir antes de cada envio
- [ ] O site do Render abre (espere cerca de 1 min no 1º acesso)
- [ ] O `main` no GitHub tem a versão final e o selo dos testes está verde
- [ ] `docs/IA.md` tem uma linha para cada uso de IA, inclusive o de sábado
- [ ] Nenhuma planta do shopping, logo do shopping, nome de loja real, dado pessoal ou chave no repositório e no vídeo
- [ ] O teste de usabilidade tem **só** dados reais (ninguém inventa resultado)

## Antes da final (17h)
- [ ] Demo ensaiada com cronômetro (90 s) e com o plano B (rodar local + hotspot)
- [ ] Cada integrante leu [`cola-integrantes.md`](cola-integrantes.md) e treinou as 5 respostas
- [ ] Quem responde o quê na banca: técnica ______ · IA ______ · negócio/uso ______
- [ ] Ver [`faq-banca.md`](faq-banca.md) uma última vez
