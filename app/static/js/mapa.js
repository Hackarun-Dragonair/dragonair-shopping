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
  // Shopping genérico e inventado: corredores, dezenas de lojas sem nome, átrio redondo,
  // âncoras nas pontas, praça de alimentação em leque, cinema e garagem com vagas.
  // As lojas NÃO são desenhadas uma a uma: pequenas funções repetem blocos em fila, em anel ou em leque.
  // Cada forma pode ser retângulo {x,y,w,h}, polígono {pts} ou caminho SVG {d}.
  // lx/ly = onde fica o nome; gx/gy = onde o gato senta; curto = nome menor mostrado no celular.
  // Zonas que não estiverem aqui são posicionadas sozinhas numa grade.
  const rad = (g) => (g * Math.PI) / 180;
  const um = (n) => Math.round(n * 10) / 10;           // 1 casa decimal: SVG mais leve
  const pt = (x, y) => `${um(x)},${um(y)}`;

  // n lojas iguais em fila a partir de (x0,y0); "angulo" gira a fila (0 = para a direita)
  function fileira(x0, y0, n, larg, alt, passo, angulo = 0) {
    const c = Math.cos(rad(angulo)), s = Math.sin(rad(angulo)), lista = [];
    for (let i = 0; i < n; i++) {
      const ox = x0 + i * passo * c, oy = y0 + i * passo * s;
      const cantos = [[0, 0], [larg, 0], [larg, alt], [0, alt]].map(([a, b]) => pt(ox + a * c - b * s, oy + a * s + b * c));
      lista.push({ pts: cantos.join(" ") });
    }
    return lista;
  }
  // Corredor reto [x0,y0,x1,y1,largura] vira uma faixa clara
  function rua([x0, y0, x1, y1, w]) {
    const a = Math.atan2(y1 - y0, x1 - x0), nx = (-Math.sin(a) * w) / 2, ny = (Math.cos(a) * w) / 2;
    return { pts: [pt(x0 + nx, y0 + ny), pt(x1 + nx, y1 + ny), pt(x1 - nx, y1 - ny), pt(x0 - nx, y0 - ny)].join(" ") };
  }
  // Lojas de um lado do corredor (lado 1 ou -1), de "ini" até "fim" (distâncias das pontas)
  function margem([x0, y0, x1, y1, w], lado, alt, ini = 0, fim = 0, larg = 26, passo = 30) {
    const a = Math.atan2(y1 - y0, x1 - x0), c = Math.cos(a), s = Math.sin(a);
    const n = Math.floor((Math.hypot(x1 - x0, y1 - y0) - ini - fim - larg) / passo) + 1;
    const d = lado > 0 ? w / 2 + 3 : -(w / 2 + 3 + alt);
    return fileira(x0 + c * ini - s * d, y0 + s * ini + c * d, n, larg, alt, passo, (a * 180) / Math.PI);
  }
  // Fatia de anel entre os raios ri e re, do ângulo a0 ao a1 (0° = direita, 90° = para baixo)
  function setor(cx, cy, ri, re, a0, a1) {
    const p = (r, g) => pt(cx + r * Math.cos(rad(g)), cy + r * Math.sin(rad(g)));
    const grande = a1 - a0 > 180 ? 1 : 0;
    const fora = `M${p(re, a0)} A${re},${re} 0 ${grande},1 ${p(re, a1)}`;
    return ri > 0 ? `${fora} L${p(ri, a1)} A${ri},${ri} 0 ${grande},0 ${p(ri, a0)} Z` : `${fora} L${pt(cx, cy)} Z`;
  }
  // n boxes lado a lado num anel ou leque (átrio redondo, praça de alimentação)
  function leque(cx, cy, ri, re, n, a0, a1, folga = 1.6) {
    const passo = (a1 - a0) / n;
    return Array.from({ length: n }, (_, i) => ({ d: setor(cx, cy, ri, re, a0 + i * passo + folga / 2, a0 + (i + 1) * passo - folga / 2) }));
  }
  // Vagas de garagem: n riscos inclinados a partir de (x0,y0)
  function vagas(x0, y0, n, passo, alt, incl) {
    return Array.from({ length: n }, (_, i) => [x0 + i * passo, y0, x0 + i * passo + incl, y0 + alt]);
  }

  // Térreo: corredor principal leste-oeste, corredor norte, dois corredores em diagonal até a entrada
  const T = {
    principal: [210, 280, 790, 280, 34], norte: [215, 170, 700, 170, 20], entrada: [500, 297, 500, 442, 34],
    diagOeste: [235, 297, 440, 442, 24], diagLeste: [765, 297, 560, 442, 24], ligacao: [500, 178, 500, 264, 22],
  };
  // L1: faixa do corredor norte, corredor da praça e corredor leste
  const L1 = { norte: [122, 149, 690, 139, 60], praca: [128, 236, 690, 228, 16], leste: [676, 236, 676, 470, 22] };
  // L2: corredor principal, corredor das lojas e a borda oeste (só para alinhar lojas)
  const L2 = { principal: [128, 300, 640, 300, 28], lojas: [415, 200, 600, 192, 18], borda: [148, 322, 190, 470, 0] };

  const PLANTA = {
    "Térreo": {
      casca: "M95,150 L160,85 L520,75 L700,92 L900,105 L945,170 L940,420 L880,480 Q500,615 120,480 L60,410 L58,215 Z",
      ruas: Object.values(T),
      lojas: [
        ...margem(T.norte, -1, 44),                       // fachada norte
        ...margem(T.norte, 1, 74, 0, 335), ...margem(T.norte, 1, 74, 425),
        ...leque(500, 280, 64, 92, 4, 18, 72), ...leque(500, 280, 64, 92, 4, 108, 162),   // anel do átrio
        ...leque(500, 280, 64, 92, 4, 198, 252), ...leque(500, 280, 64, 92, 4, 288, 342),
        ...margem(T.diagOeste, -1, 40, 34, 8), ...margem(T.diagOeste, 1, 40, 22, 70),          // diagonais
        ...margem(T.diagLeste, 1, 40, 34, 8), ...margem(T.diagLeste, -1, 40, 22, 70),
        ...fileira(150, 440, 4, 26, 34, 30, 14), ...fileira(712, 474, 3, 26, 34, 30, -14),        // perto da fachada sul
      ],
      deco: [
        { pts: "70,222 104,160 165,100 205,100 205,400 75,404", t: "Âncora Oeste", lx: 140, ly: 260 },
        { pts: "800,270 930,270 928,412 872,466 800,452", t: "Âncora Leste", lx: 862, ly: 360 },
        { d: setor(500, 280, 0, 56, 0, 359.9), t: "Eventos", lx: 500, ly: 280 },
      ],
      icones: [
        { x: 368, y: 190, w: 24, h: 24, t: "WC" }, { x: 368, y: 222, w: 24, h: 24, t: "ESC" },
        { x: 610, y: 190, w: 24, h: 24, t: "WC" }, { x: 610, y: 222, w: 24, h: 24, t: "ESC" },
      ],
      zonas: {
        "entrada-principal": { pts: "362,440 638,440 668,518 590,533 500,538 410,533 332,518", lx: 500, ly: 488, curto: "Entrada" },
        "doca-1": { pts: "712,104 895,112 932,175 928,245 845,258 712,240", lx: 820, ly: 180 },
      },
    },
    "L1": {
      casca: "M70,150 L135,82 L700,72 L870,70 L935,130 L945,300 Q960,470 840,540 L600,560 L520,592 L440,560 L150,545 L62,470 Z",
      ruas: [L1.praca, L1.leste],
      lojas: [
        ...margem(L1.norte, -1, 24, 30), ...margem(L1.norte, 1, 40, 10),
        ...leque(420, 486, 204, 240, 20, 180, 360),       // boxes da praça de alimentação, em leque
        ...fileira(190, 494, 6, 26, 36, 30), ...fileira(476, 494, 6, 26, 36, 30),
      ],
      deco: [
        { pts: "72,236 172,236 176,476 66,476", t: "Âncora Oeste", lx: 122, ly: 356 },
        { pts: "706,480 878,472 846,512 806,534 706,540", t: "Âncora Leste", lx: 784, ly: 506 },
        { d: setor(420, 486, 0, 52, 180, 360), t: "Átrio", lx: 420, ly: 466 },
      ],
      icones: [{ x: 398, y: 496, w: 22, h: 22, t: "ESC" }, { x: 424, y: 496, w: 22, h: 22, t: "WC" }],
      zonas: {
        "corredor-norte": { pts: "120,119 690,109 692,169 122,179", lx: 405, ly: 144, curto: "Corredor norte" },
        // praça de alimentação: as mesas em leque, cercadas pelos boxes
        "praca-a": { d: setor(420, 486, 60, 196, 180, 270), lx: 322, ly: 398, gx: 300, gy: 330, curto: "Praça A" },
        "praca-b": { d: setor(420, 486, 60, 196, 270, 360), lx: 510, ly: 398, gx: 560, gy: 340, curto: "Praça B" },
        "sanitario-piso1": { pts: "716,90 858,80 925,135 930,208 815,222 728,205", lx: 822, ly: 160, gx: 870, gy: 128, curto: "Sanitário 1" },
        "escada-norte": { pts: "708,238 920,226 925,318 860,334 722,338 692,290", lx: 805, ly: 296, gx: 895, gy: 262, curto: "Escada norte" },
        "banheiro-l1-sul": { pts: "712,352 925,342 915,415 880,440 860,462 722,466 696,410", lx: 800, ly: 405, gx: 905, gy: 378, curto: "Banheiro sul" },
      },
    },
    "L2": {
      casca: "M150,125 L600,98 L815,118 Q905,240 875,420 L785,512 L300,528 L165,455 L118,265 Z",
      ruas: [L2.principal, L2.lojas],
      lojas: [
        ...fileira(175, 150, 6, 34, 52, 38),               // salas do cinema
        ...margem(L2.lojas, -1, 60), ...margem(L2.lojas, 1, 62),
        ...leque(390, 515, 150, 188, 18, 196, 344),        // restaurantes do espaço gourmet, em leque
        ...margem(L2.borda, -1, 40, 0, 30), ...fileira(640, 330, 4, 26, 40, 32, 90),
      ],
      deco: [
        { pts: "150,142 405,126 405,276 125,276", t: "Cinema", lx: 265, ly: 244 },
        { d: setor(390, 515, 40, 140, 196, 344), t: "Espaço gourmet", lx: 390, ly: 440 },
      ],
      icones: [{ x: 368, y: 486, w: 22, h: 22, t: "ESC" }, { x: 394, y: 486, w: 22, h: 22, t: "WC" }],
      zonas: {
        "banheiro-l2-norte": { pts: "608,112 798,130 850,215 772,272 622,252", lx: 724, ly: 205, gx: 785, gy: 172, curto: "Banheiro norte" },
        "area-tecnica-l2": { pts: "690,318 865,300 862,405 780,492 676,470 682,380", lx: 770, ly: 400, curto: "Área técnica" },
      },
    },
    "Estacionamento": {
      casca: "M100,135 L180,92 L880,100 L932,180 L912,500 L822,540 L140,532 L80,452 Z",
      ruas: [[200, 197, 790, 197, 20], [200, 418, 790, 418, 20], [215, 197, 215, 418, 20]],
      linhas: [
        ...vagas(200, 116, 21, 28, 34, 10), ...vagas(200, 152, 21, 28, 34, 10),    // duas fileiras em cima
        ...vagas(190, 430, 21, 28, 34, -10), ...vagas(190, 466, 21, 28, 34, -10),  // duas fileiras embaixo
        [200, 151, 788, 151], [190, 465, 778, 465],                               // meio-fio entre as fileiras
      ],
      deco: [
        { d: "M790,222 Q925,300 815,410 L775,392 Q840,305 762,248 Z", t: "Rampa", lx: 834, ly: 312 },
        { pts: "104,262 196,250 198,338 110,352", t: "Elevadores", lx: 152, ly: 300 },
      ],
      icones: [{ x: 822, y: 130, w: 34, h: 22, t: "Saída" }, { x: 806, y: 448, w: 40, h: 22, t: "Entrada" },
        ...[0, 1, 2, 3, 4, 5].flatMap((i) => [{ x: 222 + i * 112, y: 147, w: 8, h: 8, t: "" }, { x: 212 + i * 112, y: 461, w: 8, h: 8, t: "" }])],  // pilares
      zonas: {
        "estacionamento-g1": { pts: "265,218 715,208 760,305 728,398 282,398 232,318", lx: 500, ly: 306 },
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
    // Fundo (só enfeite, não reage ao toque): corredores claros, lojas bege, vagas, áreas grandes e ícones
    const fundo = el("g", { class: "fundo-desenho" });
    (base.ruas || []).forEach((r) => fundo.appendChild(forma(rua(r), { class: "corredor" })));
    (base.lojas || []).forEach((l) => fundo.appendChild(forma(l, { class: "loja" })));
    (base.linhas || []).forEach(([x1, y1, x2, y2]) => fundo.appendChild(el("line", { x1, y1, x2, y2, class: "vaga" })));
    (base.deco || []).forEach((d) => {
      fundo.appendChild(forma(d, { class: "deco" }));
      const [tx, ty] = centro(d);
      fundo.appendChild(el("text", { x: tx, y: ty, class: "deco-texto" }, d.t));
    });
    (base.icones || []).forEach((i) => {
      fundo.appendChild(forma(i, { class: "icone" }));
      fundo.appendChild(el("text", { x: i.x + i.w / 2, y: i.y + i.h / 2 + 0.5, class: "icone-texto" }, i.t));
    });
    svg.appendChild(fundo);
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
