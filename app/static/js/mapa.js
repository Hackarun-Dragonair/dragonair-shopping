// Mapa interativo das zonas (SVG). Desenho FICTÍCIO feito pela equipe:
// não usa a planta do shopping (dado sensível) nem nomes de lojas reais.
// Lê GET /mapa a cada 5 s, pinta cada zona pelo estado e abre um painel ao tocar.
(function () {
  const W = 1000;
  let H = 620;          // muda quando o piso tem planta de fundo (proporção da imagem)
  let layouts = {};     // planta + bloquinhos desenhados pelo gestor (GET /mapa/layout)
  const caixa = document.getElementById("mapa-caixa");
  if (!caixa) return;
  const NS = "http://www.w3.org/2000/svg";
  const $ = (id) => document.getElementById(id);

  // ---------- Desenho de cada piso (coordenadas inventadas) ----------
  // Desenho fictício feito do zero pela equipe; não copia a planta do shopping (dado sensível).
  // Shopping genérico e inventado: fachada curva, átrio redondo, âncoras nas pontas, praça em leque.
  // Cada forma pode ser retângulo {x,y,w,h}, polígono {pts} ou caminho SVG {d}.
  // lx/ly = onde fica o nome; gx/gy = onde o gato senta; curto = nome menor mostrado no celular.
  // Zonas que não estiverem aqui são posicionadas sozinhas numa grade.
  const PLANTA = {
    "Térreo": {
      casca: "M95,150 L160,85 L520,75 L700,92 L900,105 L945,170 L940,420 L880,480 Q500,615 120,480 L60,410 L58,215 Z",
      deco: [
        { pts: "72,222 106,163 168,100 285,108 312,250 262,395 75,402", t: "Âncora Oeste", lx: 185, ly: 250 },
        { pts: "752,262 848,278 928,262 925,412 872,465 768,448 735,352", t: "Âncora Leste", lx: 840, ly: 365 },
        { pts: "330,110 480,96 492,205 352,232", t: "Lojas" },
        { pts: "508,96 678,103 688,222 600,232 512,206", t: "Lojas" },
        { pts: "325,300 418,335 412,428 300,432 280,395", t: "Lojas" },
        { pts: "585,335 690,305 712,355 735,432 598,430", t: "Lojas" },
        { d: "M430,305 a70,70 0 1,0 140,0 a70,70 0 1,0 -140,0", t: "Átrio", lx: 500, ly: 305 },
        { pts: "445,388 555,388 548,428 452,428", t: "Elevadores" },
      ],
      zonas: {
        "entrada-principal": { pts: "362,440 638,440 668,518 590,533 500,538 410,533 332,518", lx: 500, ly: 488, curto: "Entrada" },
        "doca-1": { pts: "702,100 895,112 932,175 928,245 845,262 714,240", lx: 820, ly: 180 },
      },
    },
    "L1": {
      casca: "M70,150 L135,82 L700,72 L870,70 L935,130 L945,300 Q960,470 840,540 L600,560 L520,592 L440,560 L150,545 L62,470 Z",
      deco: [
        { pts: "85,232 190,222 158,300 122,362 80,378", t: "Lojas", lx: 128, ly: 295 },
        { d: "M330,520 A70,70 0 0,1 470,520 Z", t: "Átrio", lx: 400, ly: 500 },
        { pts: "740,480 868,474 848,506 812,526 748,524", t: "Lojas" },
      ],
      zonas: {
        "corredor-norte": { pts: "120,118 690,95 706,160 470,192 128,205", lx: 400, ly: 152, curto: "Corredor norte" },
        // praça de alimentação em leque, aberta em volta do átrio
        "praca-a": { pts: "118,480 133,420 161,365 200,317 249,278 305,251 365,237 390,441 373,445 358,452 344,463 333,476 325,492 321,509",
          lx: 272, ly: 388, curto: "Praça A" },
        "praca-b": { pts: "435,237 495,251 551,278 600,317 639,365 667,420 682,480 479,509 475,492 467,476 456,463 442,452 427,445 410,441",
          lx: 528, ly: 388, curto: "Praça B" },
        "sanitario-piso1": { pts: "716,90 858,80 925,135 930,208 815,222 728,205", lx: 822, ly: 160, gx: 870, gy: 128, curto: "Sanitário 1" },
        "escada-norte": { pts: "708,238 920,226 925,318 860,334 722,338 690,290", lx: 805, ly: 296, gx: 895, gy: 262, curto: "Escada norte" },
        "banheiro-l1-sul": { pts: "712,352 925,342 915,415 880,440 860,462 722,466 696,410", lx: 800, ly: 405, gx: 905, gy: 378, curto: "Banheiro sul" },
      },
    },
    "L2": {
      casca: "M150,125 L600,98 L815,118 Q905,240 875,420 L785,512 L300,528 L165,455 L118,265 Z",
      deco: [
        { pts: "172,148 420,130 440,300 330,350 175,328", t: "Cinema", lx: 300, ly: 240 },
        { pts: "450,122 582,110 588,232 470,240", t: "Lojas" },
        { pts: "195,358 335,372 400,470 300,510 180,450", t: "Lojas" },
        { d: "M460,330 a70,70 0 1,0 140,0 a70,70 0 1,0 -140,0", t: "Vão do átrio", lx: 530, ly: 330 },
        { pts: "430,425 580,420 570,478 440,482", t: "Elevadores" },
      ],
      zonas: {
        "banheiro-l2-norte": { pts: "598,112 798,130 850,215 772,272 622,252", lx: 724, ly: 205, gx: 785, gy: 172, curto: "Banheiro norte" },
        "area-tecnica-l2": { pts: "690,318 865,300 862,405 780,492 640,470 652,380", lx: 760, ly: 400, curto: "Área técnica" },
      },
    },
    "Estacionamento": {
      casca: "M100,135 L180,92 L880,100 L932,180 L912,500 L822,540 L140,532 L80,452 Z",
      vagas: true,
      deco: [
        { d: "M790,222 Q925,300 815,410 L775,392 Q840,305 762,248 Z", t: "Rampa", lx: 834, ly: 312 },
        { pts: "104,262 208,245 212,338 110,352", t: "Elevadores", lx: 158, ly: 300 },
      ],
      zonas: {
        "estacionamento-g1": { pts: "265,218 715,208 778,305 728,405 282,412 222,318", lx: 500, ly: 312 },
      },
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

  // ---------- Formas: retângulo {x,y,w,h}, polígono {pts:"x,y x,y ..."} ou caminho SVG {d:"M..."} ----------
  function pontos(pts) {
    // "10,20 30,40" vira [[10,20], [30,40]]
    return pts.trim().split(/\s+/).map((par) => par.split(",").map(Number));
  }
  function forma(f, attrs) {
    if (f.pts) return el("polygon", Object.assign({ points: f.pts }, attrs));
    if (f.d) return el("path", Object.assign({ d: f.d }, attrs));
    return el("rect", Object.assign({ x: f.x, y: f.y, width: f.w, height: f.h, rx: 10 }, attrs));
  }
  // Onde fica o nome: lx/ly se a forma disser; senão a média dos pontos (ou o meio do retângulo)
  function centro(f) {
    if (f.lx !== undefined) return [f.lx, f.ly];
    if (f.pts) {
      const ps = pontos(f.pts);
      return [ps.reduce((s, p) => s + p[0], 0) / ps.length, ps.reduce((s, p) => s + p[1], 0) / ps.length];
    }
    return [f.x + f.w / 2, f.y + f.h / 2];
  }
  // Canto de cima à direita, onde o gato senta
  function canto(f) {
    if (f.gx !== undefined) return [f.gx, f.gy];
    if (f.pts) {
      const ps = pontos(f.pts);
      const [x, y] = ps.reduce((a, b) => (b[0] - b[1] > a[0] - a[1] ? b : a));
      return [x - 24, y + 30];
    }
    if (f.d) { const [x, y] = centro(f); return [x + 40, y - 40]; }
    return [f.x + f.w - 18, f.y + 28];
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
    semLugar(daquele.filter((z) => !porZona[z.codigo]));
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

  // Zona que o gestor ainda não pintou na planta não pode sumir: aparece como botão abaixo do mapa
  function semLugar(lista) {
    const div = $("sem-lugar");
    if (!div) return;
    div.classList.toggle("d-none", !lista.length);
    div.innerHTML = lista.length ? '<span class="text-secondary me-1">Ainda sem lugar na planta:</span>' + lista.map((z) =>
      `<button type="button" class="chip estado-${seguro(z.estado)} border-0 me-1 mb-1" data-zona="${seguro(z.codigo)}">${seguro(z.nome)} · ${seguro(z.rotulo)}</button>`).join("") : "";
    div.querySelectorAll("button").forEach((b) => b.addEventListener("click", () => abrir(b.dataset.zona)));
  }

  function desenhar() {
    svg.innerHTML = "";
    svg.setAttribute("class", "mapa-svg");
    semLugar([]);
    const daquele = zonas.filter((z) => z.piso === pisoAtual);
    const lay = layouts[pisoAtual];
    if (lay && (lay.imagem || (lay.celulas && lay.celulas.length))) return desenharPlanta(lay, daquele);
    H = 620;
    svg.setAttribute("viewBox", `0 0 ${W} ${H}`); svg.setAttribute("height", H);
    // Tela estreita (celular): letras maiores e nome curto, para continuar legível com o mapa inteiro na tela
    const pequeno = caixa.clientWidth < 600;
    if (pequeno) svg.classList.add("mapa-pequeno");
    const { base, pos } = desenhoDoPiso(pisoAtual, daquele);
    svg.appendChild(el("path", { d: base.casca, class: "casca" }));
    if (base.vagas) {
      // vagas inclinadas, como num estacionamento de verdade
      for (let x = 140; x < 860; x += 38) {
        svg.appendChild(el("line", { x1: x, y1: 125, x2: x + 18, y2: 190, class: "vaga" }));
        svg.appendChild(el("line", { x1: x + 18, y1: 430, x2: x, y2: 495, class: "vaga" }));
      }
    }
    (base.deco || []).forEach((d) => {
      svg.appendChild(forma(d, { class: "deco" }));
      const [tx, ty] = centro(d);
      svg.appendChild(el("text", { x: tx, y: ty, class: "deco-texto" }, d.t));
    });
    daquele.forEach((z) => {
      const p = pos[z.codigo];
      const r = forma(p, {
        class: `zona z-${z.estado}${selecionada === z.codigo ? " selecionada" : ""}`, tabindex: 0, role: "button",
        "aria-label": `${z.nome}: ${z.rotulo}` });
      r.addEventListener("click", (e) => { e.stopPropagation(); abrir(z.codigo); });
      r.addEventListener("keydown", (e) => { if (e.key === "Enter") abrir(z.codigo); });
      svg.appendChild(r);
      const [cx, cy] = centro(p);
      const nome = pequeno && p.curto ? p.curto : z.nome.replace("Praça de alimentação — ", "Praça ");
      const sub = pequeno ? z.rotulo : `${z.rotulo}${z.ha ? " · " + z.ha : ""}`;
      svg.appendChild(el("text", { x: cx, y: cy - (pequeno ? 14 : 9), class: "zona-texto" }, nome));
      svg.appendChild(el("text", { x: cx, y: cy + (pequeno ? 16 : 12), class: "zona-texto zona-sub" }, sub));
      if (z.gato) {
        const [gx, gy] = canto(p);
        svg.appendChild(el("text", { x: gx, y: gy, class: "gato-svg" }, "🐈‍⬛"));
      }
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
    const repete = (z.reincidencia || []).length ? `<div class="small text-warning mb-2">Problema repetido: ${seguro(z.reincidencia.join(", "))}</div>` : "";
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
        : "Conferência registrada (à distância).";
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
  window.addEventListener("resize", () => { desenhar(); ajustar(); });  // redesenha: no celular o texto muda de tamanho

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
  // Quadro ao lado do mapa (computador grande): busca a mesma página e troca só esse pedaço
  async function atualizarLateral() {
    const lateral = document.querySelector(".lateral-mapa");
    if (!lateral || getComputedStyle(lateral).display === "none") return;
    try {
      const resposta = await fetch(location.pathname, { headers: { Accept: "text/html" } });
      const nova = new DOMParser().parseFromString(await resposta.text(), "text/html").querySelector(".lateral-mapa");
      if (nova) lateral.innerHTML = nova.innerHTML;
    } catch (e) { /* sem rede: mantém o que já está na tela */ }
  }
  setInterval(() => {
    if (document.hidden || arrasto) return;
    carregar().then(() => { if (selecionada) abrir(selecionada); });
    atualizarLateral();
  }, 5000);  // definição: ≤ 5 s
})();
