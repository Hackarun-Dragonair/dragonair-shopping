// Funções comuns das telas: conversar com a API do backend em JSON.
async function chamarApi(url, dados) {
  const opcoes = { headers: { "Accept": "application/json" } };
  if (dados !== undefined) {
    opcoes.method = "POST";
    opcoes.headers["Content-Type"] = "application/json";
    opcoes.body = JSON.stringify(dados);
  }
  let resposta;
  try {
    resposta = await fetch(url, opcoes);
  } catch (erro) {
    // Sem rede: falha alto, nunca finge que enviou.
    throw new Error("Não enviado: sem conexão. Verifique a internet e tente de novo.");
  }
  const json = await resposta.json().catch(() => ({}));
  if (!resposta.ok) throw new Error(json.mensagem || json.erro || "Não deu certo (erro " + resposta.status + ").");
  return json;
}

// Evita que texto digitado vire HTML na tela.
function seguro(texto) {
  const div = document.createElement("div");
  div.textContent = texto == null ? "" : String(texto);
  return div.innerHTML;
}

const NOME_PRIORIDADE = { P1: "P1 · Urgente", P2: "P2 · Alta", P3: "P3 · Média", P4: "P4 · Baixa" };
