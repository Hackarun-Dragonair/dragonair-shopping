// Tela da zona: fluxo do botão "Problema".
// 1) abre o formulário  2) pede a sugestão da IA  3) a pessoa confere e registra.
(function () {
  const painel = document.getElementById("painel-problema");
  const codigo = painel.dataset.zona;
  const $ = (id) => document.getElementById(id);
  let sugestaoIA = null;   // o que a IA sugeriu (para saber se a pessoa mudou)

  // 1) Problema: em vez de enviar o formulário, abre o painel
  $("botao-problema").addEventListener("click", async function (evento) {
    evento.preventDefault();
    painel.classList.remove("d-none");
    const dados = await chamarApi(`/z/${codigo}/problema`);
    $("atalhos").innerHTML = dados.botoes.map((b) =>
      `<button type="button" class="btn btn-outline-light btn-sm atalho">${seguro(b)}</button>`).join("");
    document.querySelectorAll(".atalho").forEach((b) =>
      b.addEventListener("click", () => { $("descricao").value = b.textContent; }));
    $("perto").innerHTML = '<option value="">—</option>' + dados.perto_de.map((p) =>
      `<option value="${seguro(p.codigo)}">${seguro(p.nome)}</option>`).join("");
    $("descricao").focus();
  });

  // 2) Sugestão da IA
  $("botao-sugestao").addEventListener("click", async function () {
    const descricao = $("descricao").value.trim();
    if (!descricao) { $("descricao").focus(); return; }
    const r = await chamarApi(`/z/${codigo}/triagem`, { descricao, perto_de: $("perto").value, origem: "qr" });
    const s = r.sugestao;
    sugestaoIA = { categoria: s.categoria, prioridade: s.prioridade, equipe_id: String(r.equipe_id) };

    $("categoria").innerHTML = r.categorias.map((c) => `<option value="${c.codigo}">${seguro(c.nome)}</option>`).join("");
    $("prioridade").innerHTML = ["P1", "P2", "P3", "P4"].map((p) => `<option value="${p}">${NOME_PRIORIDADE[p]}</option>`).join("");
    $("equipe").innerHTML = r.equipes.map((e) => `<option value="${e.id}">${seguro(e.nome)}</option>`).join("");
    $("categoria").value = s.categoria;
    $("prioridade").value = s.prioridade;
    $("equipe").value = String(r.equipe_id);

    const pct = Math.round(s.confianca * 100);
    $("confianca").textContent = `🤖 Sugestão da IA (confiança ${pct}%)` + (pct < 50 ? " · IA em dúvida, confira" : "") + ". Você pode mudar.";
    const alerta = $("alerta-risco");
    if (s.risco) { alerta.textContent = "🚨 " + s.aviso; alerta.classList.remove("d-none"); }
    else { alerta.classList.add("d-none"); }
    $("sugestao").classList.remove("d-none");
  });

  // 3) Registrar
  $("botao-registrar").addEventListener("click", async function () {
    const escolha = { categoria: $("categoria").value, prioridade: $("prioridade").value, equipe_id: $("equipe").value };
    const mudou = Object.keys(escolha).some((k) => escolha[k] !== sugestaoIA[k]);
    const r = await chamarApi(`/z/${codigo}/problema`, {
      descricao: $("descricao").value.trim(), perto_de: $("perto").value, origem: "qr",
      ...escolha, editado: mudou ? "1" : "0",
      sugestao_categoria: sugestaoIA.categoria, sugestao_prioridade: sugestaoIA.prioridade,
    });
    const aviso = r.aviso ? `<div class="alert alert-danger fw-bold">${seguro(r.aviso)}</div>` : "";
    $("sugestao").classList.add("d-none");
    $("resultado").innerHTML = aviso +
      `<div class="alert alert-success">✅ Problema registrado e enviado para ${seguro(r.problema.equipe_nome)}.
       <a href="/telas/problemas/${r.problema.id}">Ver linha do tempo</a></div>`;
  });
})();
