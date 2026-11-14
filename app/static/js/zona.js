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
    let r;
    try {
      r = await chamarApi(`/z/${codigo}/triagem`, { descricao, perto_de: $("perto").value, origem: "qr" });
    } catch (erro) {
      $("resultado").innerHTML = `<div class="aviso aviso-problema">${seguro(erro.message)}</div>`;
      return;
    }
    const s = r.sugestao;
    sugestaoIA = { categoria: s.categoria, prioridade: s.prioridade, equipe_id: String(r.equipe_id) };

    $("categoria").innerHTML = r.categorias.map((c) => `<option value="${c.codigo}">${seguro(c.nome)}</option>`).join("");
    $("prioridade").innerHTML = ["P1", "P2", "P3", "P4"].map((p) => `<option value="${p}">${NOME_PRIORIDADE[p]}</option>`).join("");
    $("equipe").innerHTML = r.equipes.map((e) => `<option value="${e.id}">${seguro(e.nome)}</option>`).join("");
    $("categoria").value = s.categoria;
    $("prioridade").value = s.prioridade;
    $("equipe").value = String(r.equipe_id);

    const pct = Math.round(s.confianca * 100);
    const emDuvida = pct < 50 && !s.alternativa;   // com alternativa, a pergunta abaixo já avisa
    $("confianca").textContent = `Sugestão da IA local · confiança ${pct}%` + (emDuvida ? " · IA em dúvida, confira" : "") + ". Você pode mudar.";
    mostrarDesempate(s, r);
    const alerta = $("alerta-risco");
    if (s.risco) { alerta.textContent = s.aviso; alerta.classList.remove("d-none"); }
    else { alerta.classList.add("d-none"); }
    // Nova sugestão = novo registro: libera o botão e limpa o recado do registro anterior
    $("botao-registrar").disabled = false;
    $("botao-registrar").textContent = "Registrar problema";
    $("resultado").innerHTML = "";
    $("sugestao").classList.remove("d-none");
  });

  // 2b) Pergunta de desempate: a IA ficou entre duas categorias.
  // Os botões só preenchem Categoria e Equipe; a pessoa ainda pode mudar tudo nos campos.
  let opcoes = [];   // [{categoria, equipe_id}, {categoria, equipe_id}]
  function mostrarDesempate(s, r) {
    if (!s.alternativa || !r.alternativa_equipe) {
      $("desempate").classList.add("d-none");
      return;
    }
    opcoes = [
      { categoria: s.categoria, equipe_id: String(r.equipe_id) },
      { categoria: s.alternativa, equipe_id: String(r.alternativa_equipe.equipe_id) },
    ];
    $("pergunta-desempate").innerHTML =
      `A IA ficou em dúvida. É mais <strong>${seguro(s.categoria_nome)}</strong> ou <strong>${seguro(s.alternativa_nome)}</strong>?`;
    $("opcao-1").textContent = s.categoria_nome;
    $("opcao-2").textContent = s.alternativa_nome;
    marcarOpcao();
    $("desempate").classList.remove("d-none");
  }

  // Deixa dourado o botão que bate com a categoria escolhida agora.
  function marcarOpcao() {
    ["opcao-1", "opcao-2"].forEach((id, i) => {
      const escolhido = opcoes[i] && $("categoria").value === opcoes[i].categoria;
      $(id).classList.toggle("btn-primary", escolhido);
      $(id).classList.toggle("btn-outline-light", !escolhido);
    });
  }

  ["opcao-1", "opcao-2"].forEach((id, i) => {
    $(id).addEventListener("click", function () {
      $("categoria").value = opcoes[i].categoria;
      $("equipe").value = opcoes[i].equipe_id;
      marcarOpcao();
    });
  });
  $("categoria").addEventListener("change", marcarOpcao);

  // 3) Registrar
  $("botao-registrar").addEventListener("click", async function () {
    const botao = this;
    if (botao.disabled) return;           // evita registrar duas vezes
    botao.disabled = true;
    botao.textContent = "Enviando…";
    try {
    const escolha = { categoria: $("categoria").value, prioridade: $("prioridade").value, equipe_id: $("equipe").value };
    const mudou = Object.keys(escolha).some((k) => escolha[k] !== sugestaoIA[k]);
    const r = await chamarApi(`/z/${codigo}/problema`, {
      descricao: $("descricao").value.trim(), perto_de: $("perto").value, origem: "qr",
      ...escolha, editado: mudou ? "1" : "0",
      sugestao_categoria: sugestaoIA.categoria, sugestao_prioridade: sugestaoIA.prioridade,
    });
    const aviso = r.aviso ? `<div class="alert alert-danger fw-bold">${seguro(r.aviso)}</div>` : "";
    $("sugestao").classList.add("d-none");
    $("descricao").value = "";            // pronto para o próximo relato
    $("resultado").innerHTML = aviso +
      `<div class="aviso aviso-ok">Ocorrência #${r.problema.id} registrada e enviada para ${seguro(r.problema.equipe_nome)}.
       <a href="/telas/problemas/${r.problema.id}">Ver linha do tempo</a></div>`;
    } catch (erro) {
      $("resultado").innerHTML = `<div class="aviso aviso-problema">${seguro(erro.message)}</div>`;
      botao.disabled = false;
      botao.textContent = "Tentar de novo";
    }
  });
})();
