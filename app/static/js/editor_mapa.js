// Editor do mapa (gestor): planta de fundo + grade de bloquinhos.
// Arraste para selecionar um grupo de bloquinhos e atribua a um setor (zona).
(function () {
  const $ = (id) => document.getElementById(id);
  const dados = JSON.parse($("ed-dados").textContent);
  const NS = "http://www.w3.org/2000/svg";
  const W = 1000;
  const CORES = ["#c9a227", "#2f80ed", "#27ae60", "#eb5757", "#9b51e0", "#f2994a", "#00a8a8", "#d35d9b", "#6d8a2f", "#8a6d3b", "#4f6bed", "#b8860b"];
  const svg = $("ed-svg");

  let layouts = {};
  let piso = dados.pisos[0];
  let estado = null;          // {imagem, proporcao, colunas, linhas, celulas: Map("c,l" -> codigo)}
  let selecao = new Set();    // "c,l"
  let alterado = false;

  const corDaZona = (codigo) => {
    const i = dados.zonas.findIndex((z) => z.codigo === codigo);
    return CORES[(i < 0 ? 0 : i) % CORES.length];
  };
  const nomeDaZona = (codigo) => (dados.zonas.find((z) => z.codigo === codigo) || {}).nome || codigo;

  function carregarEstado() {
    const l = layouts[piso] || {};
    estado = {
      imagem: l.imagem || null,
      proporcao: l.proporcao || 0.62,
      colunas: l.colunas || 40,
      linhas: l.linhas || 25,
      celulas: new Map((l.celulas || []).map(([c, li, z]) => [`${c},${li}`, z])),
    };
    selecao = new Set();
    alterado = false;
    $("ed-colunas").value = estado.colunas;
    $("ed-linhas").value = estado.linhas;
    $("ed-zona").innerHTML = dados.zonas.filter((z) => z.piso === piso)
      .map((z) => `<option value="${seguro(z.codigo)}">${seguro(z.nome)}</option>`).join("");
    desenhar();
  }

  function H() { return Math.round(W * estado.proporcao); }

  function el(tag, attrs, texto) {
    const e = document.createElementNS(NS, tag);
    for (const [k, v] of Object.entries(attrs)) e.setAttribute(k, v);
    if (texto !== undefined) e.textContent = texto;
    return e;
  }

  function desenhar() {
    const h = H();
    svg.setAttribute("viewBox", `0 0 ${W} ${h}`);
    svg.innerHTML = "";
    svg.appendChild(el("rect", { x: 0, y: 0, width: W, height: h, fill: "#f4f2ec" }));
    if (estado.imagem) {
      svg.appendChild(el("image", { href: estado.imagem + "?v=" + Date.now(), x: 0, y: 0, width: W, height: h, preserveAspectRatio: "none", opacity: 0.9 }));
    } else {
      svg.appendChild(el("text", { x: W / 2, y: h / 2, "text-anchor": "middle", fill: "#8a8578", "font-size": 22 }, "Sem planta: envie uma imagem ou desenhe direto na grade"));
    }
    const cw = W / estado.colunas, ch = h / estado.linhas;
    const grupo = el("g", {});
    for (let li = 0; li < estado.linhas; li++) {
      for (let c = 0; c < estado.colunas; c++) {
        const k = `${c},${li}`;
        const z = estado.celulas.get(k);
        const sel = selecao.has(k);
        grupo.appendChild(el("rect", {
          x: c * cw, y: li * ch, width: cw, height: ch,
          fill: z ? corDaZona(z) : "transparent", "fill-opacity": z ? 0.55 : 0,
          stroke: sel ? "#111" : "#00000022", "stroke-width": sel ? 2 : 0.5,
          "data-k": k,
        }));
      }
    }
    svg.appendChild(grupo);
    // Nome de cada setor no centro dos seus bloquinhos
    const somas = {};
    estado.celulas.forEach((z, k) => {
      const [c, li] = k.split(",").map(Number);
      const s = (somas[z] = somas[z] || { x: 0, y: 0, n: 0 });
      s.x += (c + 0.5) * cw; s.y += (li + 0.5) * ch; s.n++;
    });
    Object.entries(somas).forEach(([z, s]) => {
      svg.appendChild(el("text", { x: s.x / s.n, y: s.y / s.n, "text-anchor": "middle", "dominant-baseline": "middle",
        "font-size": 15, "font-weight": 700, fill: "#1b1b1b", stroke: "#fff", "stroke-width": 3, "paint-order": "stroke",
        "pointer-events": "none" }, nomeDaZona(z)));
    });
    $("ed-selecao").textContent = selecao.size ? `${selecao.size} bloquinho(s) selecionado(s).` : "Nenhum bloquinho selecionado.";
    legenda();
  }

  function legenda() {
    const usados = {};
    estado.celulas.forEach((z) => { usados[z] = (usados[z] || 0) + 1; });
    const zonasPiso = dados.zonas.filter((z) => z.piso === piso);
    $("ed-legenda").innerHTML = "<div class='fw-semibold mb-1'>Setores deste piso</div>" + zonasPiso.map((z) =>
      `<div class="d-flex align-items-center gap-2 mb-1"><i style="width:12px;height:12px;border-radius:3px;background:${corDaZona(z.codigo)}"></i>
       <span class="flex-fill">${seguro(z.nome)}</span><span class="${usados[z.codigo] ? "" : "text-danger"}">${usados[z.codigo] || "sem bloco"}</span></div>`).join("");
  }

  // ---------- Seleção por arrasto ----------
  function celulaDoPonto(evento) {
    const pt = svg.createSVGPoint();
    pt.x = evento.clientX; pt.y = evento.clientY;
    const p = pt.matrixTransform(svg.getScreenCTM().inverse());
    const c = Math.floor(p.x / (W / estado.colunas)), li = Math.floor(p.y / (H() / estado.linhas));
    return [Math.max(0, Math.min(estado.colunas - 1, c)), Math.max(0, Math.min(estado.linhas - 1, li))];
  }
  let inicio = null, somar = false, base = null;
  svg.addEventListener("pointerdown", (e) => {
    e.preventDefault();
    svg.setPointerCapture(e.pointerId);
    inicio = celulaDoPonto(e);
    somar = e.ctrlKey || e.metaKey;
    base = somar ? new Set(selecao) : new Set();
  });
  svg.addEventListener("pointermove", (e) => {
    if (!inicio) return;
    const fim = celulaDoPonto(e);
    selecao = new Set(base);
    for (let c = Math.min(inicio[0], fim[0]); c <= Math.max(inicio[0], fim[0]); c++)
      for (let li = Math.min(inicio[1], fim[1]); li <= Math.max(inicio[1], fim[1]); li++) selecao.add(`${c},${li}`);
    desenhar();
  });
  svg.addEventListener("pointerup", (e) => {
    if (!inicio) return;
    const fim = celulaDoPonto(e);
    if (fim[0] === inicio[0] && fim[1] === inicio[1]) {
      const k = `${fim[0]},${fim[1]}`;
      const z = estado.celulas.get(k);
      selecao = new Set(base);
      if (z) { // clique num setor: seleciona o setor inteiro e já escolhe ele na lista
        estado.celulas.forEach((zz, kk) => { if (zz === z) selecao.add(kk); });
        $("ed-zona").value = z;
      } else selecao.add(k);
      desenhar();
    }
    inicio = null;
  });

  // ---------- Ações ----------
  function msg(texto, tipo = "secondary") { $("ed-msg").innerHTML = `<span class="text-${tipo}">${seguro(texto)}</span>`; }

  $("ed-atribuir").addEventListener("click", () => {
    if (!selecao.size) return msg("Selecione bloquinhos primeiro.", "danger");
    const z = $("ed-zona").value;
    selecao.forEach((k) => estado.celulas.set(k, z));
    selecao = new Set(); alterado = true; desenhar();
    msg(`Atribuído a ${nomeDaZona(z)}. Não esqueça de salvar.`);
  });
  $("ed-apagar").addEventListener("click", () => {
    selecao.forEach((k) => estado.celulas.delete(k));
    selecao = new Set(); alterado = true; desenhar();
  });
  $("ed-grade").addEventListener("click", () => {
    const c = parseInt($("ed-colunas").value, 10), l = parseInt($("ed-linhas").value, 10);
    if (!(c >= 10 && c <= 80 && l >= 10 && l <= 80)) return msg("Use de 10 a 80 colunas e linhas.", "danger");
    if (estado.celulas.size) {
      // Mudar a grade reescala os bloquinhos já pintados para a nova grade
      const novas = new Map();
      estado.celulas.forEach((z, k) => {
        const [cc, ll] = k.split(",").map(Number);
        const x0 = Math.floor(cc * c / estado.colunas), x1 = Math.floor((cc + 1) * c / estado.colunas);
        const y0 = Math.floor(ll * l / estado.linhas), y1 = Math.floor((ll + 1) * l / estado.linhas);
        for (let x = x0; x <= Math.max(x0, x1 - 1); x++) for (let y = y0; y <= Math.max(y0, y1 - 1); y++) novas.set(`${x},${y}`, z);
      });
      estado.celulas = novas;
    }
    estado.colunas = c; estado.linhas = l; selecao = new Set(); alterado = true; desenhar();
  });
  $("ed-salvar").addEventListener("click", async () => {
    const celulas = [...estado.celulas].map(([k, z]) => { const [c, l] = k.split(",").map(Number); return [c, l, z]; });
    try {
      const r = await chamarApi(`/plantas/${encodeURIComponent(piso)}/layout`,
        { colunas: estado.colunas, linhas: estado.linhas, proporcao: estado.proporcao, celulas });
      layouts = r.pisos; alterado = false;
      msg(`Mapa do piso ${piso} salvo (${r.celulas} bloquinhos).`, "success");
    } catch (e) { msg("Não salvou: " + e.message, "danger"); }
  });
  $("ed-enviar").addEventListener("click", async () => {
    const arquivo = $("ed-arquivo").files[0];
    if (!arquivo) return msg("Escolha uma imagem.", "danger");
    const form = new FormData(); form.append("arquivo", arquivo);
    msg("Enviando…");
    const resp = await fetch(`/plantas/${encodeURIComponent(piso)}/imagem`, { method: "POST", body: form, headers: { Accept: "application/json" } });
    const json = await resp.json().catch(() => ({}));
    if (!resp.ok) return msg(json.mensagem || "Não deu certo.", "danger");
    layouts = json.pisos;
    // Usa a proporção real da imagem para os bloquinhos não ficarem tortos
    const img = new Image();
    img.onload = () => {
      estado.imagem = layouts[piso].imagem;
      estado.proporcao = img.naturalHeight / img.naturalWidth;
      alterado = true; desenhar();
      msg("Imagem enviada. Agora pinte os setores e salve.", "success");
    };
    img.src = URL.createObjectURL(arquivo);
  });
  $("ed-tirar").addEventListener("click", async () => {
    const r = await chamarApi(`/plantas/${encodeURIComponent(piso)}/imagem/remover`, {});
    layouts = r.pisos; estado.imagem = null; desenhar(); msg("Imagem removida.");
  });
  $("ed-piso").addEventListener("change", (e) => {
    if (alterado && !window.confirm("Há mudanças não salvas neste piso. Trocar mesmo assim?")) { e.target.value = piso; return; }
    piso = e.target.value; carregarEstado();
  });

  chamarApi("/mapa/layout").then((r) => { layouts = r.pisos; carregarEstado(); });
})();
