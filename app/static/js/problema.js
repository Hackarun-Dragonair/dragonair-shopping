// Ações do supervisor na tela do problema. Depois de cada ação, recarrega a página
// para mostrar o novo passo na linha do tempo.
(function () {
  const tela = document.getElementById("tela-problema");
  const id = tela.dataset.id;
  document.querySelectorAll(".acao").forEach(function (botao) {
    botao.addEventListener("click", async function () {
      const acao = botao.dataset.acao;
      let dados = {};
      if (acao === "confirmar") {
        dados = {
          categoria: document.getElementById("categoria").value,
          prioridade: document.getElementById("prioridade").value,
          equipe_id: document.getElementById("equipe").value,
        };
      }
      botao.disabled = true;
      try {
        const r = await chamarApi(`/problemas/${id}/${acao}`, dados);
        if (r.aviso) { try { sessionStorage.setItem("aviso", r.aviso); } catch (e) { /* sem storage */ } }
        location.reload();
      } catch (erro) {
        document.getElementById("mensagem").innerHTML = `<div class="aviso aviso-problema">${seguro(erro.message)}</div>`;
        botao.disabled = false;
      }
    });
  });
  // Mostra o aviso da última ação (ex.: "prioridade mantida em P1")
  let aviso = null;
  try { aviso = sessionStorage.getItem("aviso"); sessionStorage.removeItem("aviso"); } catch (e) { /* sem storage */ }
  if (aviso) document.getElementById("mensagem").innerHTML = `<div class="aviso aviso-atencao">${seguro(aviso)}</div>`;
})();
