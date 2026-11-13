// Funções comuns das telas: conversar com a API do backend em JSON.
async function chamarApi(url, dados) {
  const opcoes = { headers: { "Accept": "application/json" } };
  if (dados !== undefined) {
    opcoes.method = "POST";
    opcoes.headers["Content-Type"] = "application/json";
    opcoes.body = JSON.stringify(dados);
  }
  const resposta = await fetch(url, opcoes);
  const json = await resposta.json();
  if (!resposta.ok) throw new Error(json.erro || "erro");
  return json;
}

// Evita que texto digitado vire HTML na tela.
function seguro(texto) {
  const div = document.createElement("div");
  div.textContent = texto == null ? "" : String(texto);
  return div.innerHTML;
}

const NOME_PRIORIDADE = { P1: "P1 · Urgente", P2: "P2 · Alta", P3: "P3 · Média", P4: "P4 · Baixa" };
