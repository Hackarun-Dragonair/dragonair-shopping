// JavaScript do Ronda Viva. Dono: TELAS (a parte da sugestão da IA é da tarefa #6).

// Sugestão da IA: ao digitar na tela da zona, pergunta ao servidor e mostra a sugestão.
(function () {
  const campo = document.getElementById("texto-ronda");
  const caixa = document.getElementById("sugestao-ia");
  if (!campo || !caixa) return;  // não estamos na tela da zona

  let espera;
  campo.addEventListener("input", function () {
    clearTimeout(espera);
    espera = setTimeout(buscar, 400);  // espera a pessoa parar de digitar
  });

  async function buscar() {
    const texto = campo.value.trim();
    if (texto.length < 4) { caixa.innerHTML = ""; return; }
    const resposta = await fetch("/api/sugestao?texto=" + encodeURIComponent(texto));
    const s = await resposta.json();

    let html = "";
    if (s.risco) {
      html += '<div class="alert alert-danger fw-bold mb-2">🚨 ' + s.aviso + "</div>";
    }
    const duvida = s.confianca < 0.5 ? " (IA em dúvida, confira)" : "";
    html += '<div class="border rounded p-2">🤖 Sugestão da IA' + duvida + ":<br>" +
      "Categoria: <strong>" + s.categoria + "</strong> · " +
      "Prioridade: <strong>" + s.prioridade + "</strong> · " +
      "Equipe: <strong>" + s.equipe + "</strong></div>";
    caixa.innerHTML = html;
  }
})();
