// Mapa interativo das zonas (SVG). Desenho FICTÍCIO feito pela equipe:
// não usa a planta do shopping (dado sensível) nem nomes de lojas reais.
// Lê GET /mapa a cada 15 s, pinta cada zona pelo estado e abre um painel ao tocar.
(function () {
  const W = 1000;
  let H = 620;          // muda quando o piso tem planta de fundo (proporção da imagem)
  let layouts = {};     // planta + bloquinhos desenhados pelo gestor (GET /mapa/layout)
  const caixa = document.getElementById("mapa-caixa");
  if (!caixa) return;
  const NS = "http://www.w3.org/2000/svg";
  const $ = (id) => document.getElementById(id);

  // ---------- Desenho de cada piso (coordenadas inventadas) ----------
  // Zonas que não estiverem aqui são posicionadas sozinhas numa grade.
  const PLANTA = {
    "Térreo": {
      casca: "M80,90 L920,90 L920,470 L620,470 L620,540 L380,540 L380,470 L80,470 Z",
      deco: [
        { x: 110, y: 120, w: 170, h: 110, t: "Lojas" }, { x: 300, y: 120, w: 170, h: 110, t: "Lojas" },
        { x: 490, y: 120, w: 170, h: 110, t: "Lojas" }, { x: 110, y: 330, w: 250, h: 110, t: "Loja âncora" },
        { x: 110, y: 250, w: 760, h: 60, t: "Corredor térreo" },
      ],
      zonas: { "entrada-principal": { x: 400, y: 440, w: 200, h: 90 }, "doca-1": { x: 700, y: 120, w: 190, h: 190 } },
    },
    "L1": {
      casca: "M60,80 L940,80 L940,540 L560,540 L520,580 L480,540 L60,540 Z",
      deco: [
        { x: 90, y: 310, w: 150, h: 90, t: "Lojas" }, { x: 255, y: 310, w: 150, h: 90, t: "Lojas" },
        { x: 420, y: 310, w: 150, h: 90, t: "Lojas" }, { x: 600, y: 420, w: 130, h: 100, t: "Lojas" },
        { x: 90, y: 420, w: 300, h: 100, t: "Loja âncora" },
      ],
      zonas: {
        "corredor-norte": { x: 90, y: 110, w: 610, h: 70 },
        "praca-a": { x: 90, y: 195, w: 300, h: 100 },
        "praca-b": { x: 400, y: 195, w: 300, h: 100 },
        "escada-norte": { x: 600, y: 310, w: 100, h: 90 },
        "sanitario-piso1": { x: 730, y: 110, w: 180, h: 150 },
        "banheiro-l1-sul": { x: 750, y: 380, w: 160, h: 140 },
      },
    },
    "L2": {
      casca: "M140,110 L860,110 L860,500 L140,500 Z",
      deco: [
        { x: 170, y: 290, w: 200, h: 180, t: "Lojas" }, { x: 390, y: 290, w: 200, h: 180, t: "Lojas" },
        { x: 170, y: 140, w: 420, h: 120, t: "Corredor L2" },
      ],
      zonas: { "banheiro-l2-norte": { x: 620, y: 140, w: 210, h: 150 }, "area-tecnica-l2": { x: 620, y: 310, w: 210, h: 160 } },
    },
    "Estacionamento": {
      casca: "M100,100 L900,100 L900,520 L100,520 Z",
      vagas: true,
      zonas: { "estacionamento-g1": { x: 300, y: 220, w: 400, h: 180 } },
    },
  };

  let zonas = [];
  let pisoAtual = null;
  let selecionada = null;
  let escala = 1, dx = 0, dy = 0;

  const svg = document.createElementNS(NS, "svg");
  svg.setAttribute("viewBox", `0 0 ${W} ${H}`);
  svg.setAttribute("class", "mapa-svg");
  svg.setAttribute("width", W);
  svg.setAttribute("height", H);
  caixa.appendChild(svg);

  function el(tag, attrs, texto) {
    const e = document.createElementNS(NS, tag);
    for (const [k, v] of Object.entries(attrs)) e.setAttribute(k, v);
    if (texto !== undefined) e.textContent = texto;
    return e;
  }

  function desenhoDoPiso(piso, daquele) {
    const base = PLANTA[piso] || { casca: `M60,80 L${W - 60},80 L${W - 60},${H - 60} L60,${H - 60} Z`, zonas: {} };
    const pos = Object.assign({}, base.zonas);
    // Zonas sem posição: grade automática
    const soltas = daquele.filter((z) => !pos[z.codigo]);
    soltas.forEach((z, i) => {
      const col = i % 4, lin = Math.floor(i / 4);
      pos[z.codigo] = { x: 100 + col * 205, y: 110 + lin * 150, w: 185, h: 125 };
    });
    return { base, pos };
  }

  function desenharPlanta(lay, daquele) {
    // Modo planta: imagem de fundo + bloquinhos de cada setor pintados pelo estado da zona
    H = Math.round(W * (lay.proporcao || 0.62));
    svg.setAttribute("viewBox", `0 0 ${W} ${H}`); svg.setAttribute("height", H);
    svg.appendChild(el("rect", { x: 0, y: 0, width: W, height: H, class: "fundo-planta" }));
    if (lay.imagem) svg.appendChild(el("image", { href: lay.imagem, x: 0, y: 0, width: W, height: H, preserveAspectRatio: "none", class: "imagem-planta" }));
    const cw = W / lay.colunas, ch = H / lay.linhas;
    const porZona = {};
    lay.celulas.forEach(([c, li, cod]) => (porZona[cod] = porZona[cod] || []).push([c, li]));
    daquele.forEach((z) => {
      const cels = porZona[z.codigo];
      if (!cels) return;
      const g = el("g", { class: `zona z-${z.estado}${selecionada === z.codigo ? " selecionada" : ""}`, tabindex: 0, role: "button", "aria-label": `${z.nome}: ${z.rotulo}` });
      let sx = 0, sy = 0, minY = Infinity, maxX = 0;
      cels.forEach(([c, li]) => {
        g.appendChild(el("rect", { x: c * cw, y: li * ch, width: cw + 0.6, height: ch + 0.6 }));
        sx += (c + 0.5) * cw; sy += (li + 0.5) * ch; minY = Math.min(minY, li * ch); maxX = Math.max(maxX, (c + 1) * cw);
      });
      g.addEventListener("click", (e) => { e.stopPropagation(); abrir(z.codigo); });
      g.addEventListener("keydown", (e) => { if (e.key === "Enter") abrir(z.codigo); });
      svg.appendChild(g);
      const cx = sx / cels.length, cy = sy / cels.length;
      svg.appendChild(el("text", { x: cx, y: cy - 8, class: "zona-texto" }, z.nome.replace("Praça de alimentação — ", "Praça ")));
      svg.appendChild(el("text", { x: cx, y: cy + 12, class: "zona-texto zona-sub" }, z.rotulo));
      if (z.gato) svg.appendChild(el("text", { x: maxX - 16, y: minY + 26, class: "gato-svg" }, "🐈‍⬛"));
    });
  }

  function desenhar() {
    svg.innerHTML = "";
    const daquele = zonas.filter((z) => z.piso === pisoAtual);
    const lay = layouts[pisoAtual];
    if (lay && (lay.imagem || (lay.celulas && lay.celulas.length))) return desenharPlanta(lay, daquele);
    H = 620;
    svg.setAttribute("viewBox", `0 0 ${W} ${H}`); svg.setAttribute("height", H);
    const { base, pos } = desenhoDoPiso(pisoAtual, daquele);
    svg.appendChild(el("path", { d: base.casca, class: "casca" }));
    if (base.vagas) {
      for (let x = 130; x < 880; x += 38) {
        svg.appendChild(el("line", { x1: x, y1: 120, x2: x, y2: 190, class: "vaga" }));
        svg.appendChild(el("line", { x1: x, y1: 430, x2: x, y2: 500, class: "vaga" }));
      }
    }
    (base.deco || []).forEach((d) => {
      svg.appendChild(el("rect", { x: d.x, y: d.y, width: d.w, height: d.h, rx: 8, class: "deco" }));
      svg.appendChild(el("text", { x: d.x + d.w / 2, y: d.y + d.h / 2, class: "deco-texto" }, d.t));
    });
    daquele.forEach((z) => {
      const p = pos[z.codigo];
      const r = el("rect", { x: p.x, y: p.y, width: p.w, height: p.h, rx: 10,
        class: `zona z-${z.estado}${selecionada === z.codigo ? " selecionada" : ""}`, tabindex: 0, role: "button",
        "aria-label": `${z.nome}: ${z.rotulo}` });
      r.addEventListener("click", (e) => { e.stopPropagation(); abrir(z.codigo); });
      r.addEventListener("keydown", (e) => { if (e.key === "Enter") abrir(z.codigo); });
      svg.appendChild(r);
      const cx = p.x + p.w / 2, cy = p.y + p.h / 2;
      svg.appendChild(el("text", { x: cx, y: cy - 9, class: "zona-texto" }, z.nome.replace("Praça de alimentação — ", "Praça ")));
      svg.appendChild(el("text", { x: cx, y: cy + 12, class: "zona-texto zona-sub" }, `${z.rotulo}${z.ha ? " · " + z.ha : ""}`));
      if (z.gato) svg.appendChild(el("text", { x: p.x + p.w - 18, y: p.y + 28, class: "gato-svg" }, "🐈‍⬛"));
    });
  }

  function botoesPisos() {
    const pisos = [...new Set(zonas.map((z) => z.piso))];
    $("pisos").innerHTML = pisos.map((p) => {
      const alerta = zonas.some((z) => z.piso === p && (z.estado === "problema" || z.gato));
      return `<button type="button" data-piso="${seguro(p)}" class="${p === pisoAtual ? "ativo" : ""}">${seguro(p)}${alerta ? '<span class="ponto"></span>' : ""}</button>`;
    }).join("");
    $("pisos").querySelectorAll("button").forEach((b) => b.addEventListener("click", () => {
      pisoAtual = b.dataset.piso; selecionada = null; fecharInspetor(); botoesPisos(); ajustar();
    }));
  }

  function contar() {
    const n = { ok: 0, atencao: 0, problema: 0, cinza: 0 };
    zonas.forEach((z) => { n[z.estado] = (n[z.estado] || 0) + 1; });
    for (const k of Object.keys(n)) { const c = $("n-" + k); if (c) c.textContent = n[k]; }
  }

  // ---------- Painel da zona ----------
  function abrir(codigo) {
    const z = zonas.find((x) => x.codigo === codigo);
    if (!z) return;
    selecionada = codigo;
    desenhar();
    const prob = z.problema_id
      ? `<a class="btn btn-sm btn-danger w-100 mb-2" href="/telas/problemas/${z.problema_id}">Ver problema aberto #${z.problema_id}</a>` : "";
    const gato = z.gato ? `<div class="alert alert-warning py-1 px-2 small mb-2">🐈‍⬛ O gato preto está aqui: é a zona esquecida há mais tempo.</div>` : "";
    const repete = (z.reincidencia || []).length ? `<div class="small text-warning mb-2">🔁 Problema repetido: ${seguro(z.reincidencia.join(", "))}</div>` : "";
    $("inspetor").innerHTML = `
      <div class="d-flex justify-content-between align-items-start mb-1">
        <span class="badge estado-${z.estado}">${seguro(z.rotulo)}</span>
        <button type="button" class="btn-close btn-sm" id="fechar-inspetor" aria-label="Fechar"></button>
      </div>
      <div class="fw-bold fs-6">${seguro(z.nome)}</div>
      <div class="small text-secondary mb-2">Piso ${seguro(z.piso)} · prazo ${z.prazo_minutos} min · QR: ${seguro(z.local_qr)}</div>
      <div class="small mb-2">Última conferência: <strong>${z.quando ? seguro(z.quando) + " (" + seguro(z.ha) + ")" : "nunca"}</strong></div>
      ${gato}${repete}${prob}
      <a class="btn btn-sm btn-primary w-100 mb-2" href="/z/${encodeURIComponent(z.codigo)}">Abrir tela da zona (QR)</a>
      <div class="small text-secondary mb-1">Conferir à distância:</div>
      <div class="d-flex gap-2">
        <button class="btn btn-sm btn-success flex-fill" data-res="ok">OK</button>
        <button class="btn btn-sm btn-warning flex-fill" data-res="atencao">Atenção</button>
      </div>
      <div id="msg-inspetor" class="small mt-2"></div>`;
    $("inspetor").classList.remove("d-none");
    $("fechar-inspetor").addEventListener("click", fecharInspetor);
    $("inspetor").querySelectorAll("[data-res]").forEach((b) => b.addEventListener("click", () => conferir(z.codigo, b.dataset.res)));
  }

  async function conferir(codigo, resultado) {
    try {
      const r = await chamarApi(`/z/${encodeURIComponent(codigo)}/conferir`, { resultado, origem: "lista" });
      await carregar();
      abrir(codigo);
      $("msg-inspetor").innerHTML = r.espantou_gato
        ? "🐈‍⬛ Gato preto espantado! Conferência registrada."
        : "✅ Conferência registrada (à distância).";
    } catch (e) {
      $("msg-inspetor").textContent = "Não deu certo: " + e.message;
    }
  }

  function fecharInspetor() {
    selecionada = null;
    $("inspetor").classList.add("d-none");
    desenhar();
  }

  // ---------- Arrastar e zoom ----------
  function aplicar() { svg.style.transform = `translate(${dx}px, ${dy}px) scale(${escala})`; }
  function ajustar() {
    const w = caixa.clientWidth, h = caixa.clientHeight;
    escala = Math.min(w / W, h / H) * 0.97;
    dx = (w - W * escala) / 2; dy = (h - H * escala) / 2;
    aplicar();
  }
  function zoom(f, cx, cy) {
    const nova = Math.min(5, Math.max(0.3, escala * f));
    cx = cx ?? caixa.clientWidth / 2; cy = cy ?? caixa.clientHeight / 2;
    dx = cx - (cx - dx) * (nova / escala); dy = cy - (cy - dy) * (nova / escala);
    escala = nova; aplicar();
  }
  let arrasto = null;
  caixa.addEventListener("pointerdown", (e) => {
    if (e.target.closest(".pisos, .controles-mapa, .inspetor, .legenda-mapa") || e.target.classList.contains("zona")) return;
    arrasto = { x: e.clientX - dx, y: e.clientY - dy };
    caixa.classList.add("arrastando");
  });
  window.addEventListener("pointermove", (e) => { if (arrasto) { dx = e.clientX - arrasto.x; dy = e.clientY - arrasto.y; aplicar(); } });
  window.addEventListener("pointerup", () => { arrasto = null; caixa.classList.remove("arrastando"); });
  caixa.addEventListener("wheel", (e) => {
    e.preventDefault();
    const r = caixa.getBoundingClientRect();
    zoom(e.deltaY > 0 ? 0.88 : 1.14, e.clientX - r.left, e.clientY - r.top);
  }, { passive: false });
  $("zoom-mais").addEventListener("click", () => zoom(1.25));
  $("zoom-menos").addEventListener("click", () => zoom(0.8));
  $("zoom-ajustar").addEventListener("click", ajustar);
  window.addEventListener("resize", ajustar);

  // ---------- Dados ----------
  async function carregar() {
    const [dados, lay] = await Promise.all([chamarApi("/mapa"), chamarApi("/mapa/layout").catch(() => ({ pisos: {} }))]);
    layouts = lay.pisos || {};
    zonas = dados.zonas.slice().sort((a, b) => (a.ordem_piso - b.ordem_piso) || a.nome.localeCompare(b.nome));
    if (!pisoAtual || !zonas.some((z) => z.piso === pisoAtual)) {
      // Começa no piso com mais coisa pedindo atenção
      const peso = (p) => zonas.filter((z) => z.piso === p && z.estado !== "ok").length;
      pisoAtual = [...new Set(zonas.map((z) => z.piso))].sort((a, b) => peso(b) - peso(a))[0];
    }
    contar(); botoesPisos(); desenhar();
  }

  carregar().then(ajustar).catch(() => { caixa.innerHTML = '<div class="p-3 text-secondary">Não consegui carregar o mapa. Use a lista abaixo.</div>'; });
  setInterval(() => { if (!document.hidden && !arrasto) carregar().then(() => { if (selecionada) abrir(selecionada); }); }, 5000);  // definição: ≤ 5 s
})();
