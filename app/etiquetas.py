"""PDF das etiquetas de QR. Uma zona por página: nome, onde colar e o código."""

from __future__ import annotations

import segno


def _literal(texto: str) -> bytes:
    codificado = texto.encode("cp1252", errors="replace")
    codificado = (
        codificado.replace(b"\\", b"\\\\").replace(b"(", b"\\(").replace(b")", b"\\)")
    )
    return b"(" + codificado + b")"


def _pagina(zona: dict) -> bytes:
    url = zona["url"]
    matriz = segno.make(url, error="m").matrix
    lado = len(matriz)
    modulo = 4
    origem_x = 40
    origem_y = 520
    comandos = [b"0.5 w"]
    for linha, celulas in enumerate(matriz):
        y = origem_y + (lado - 1 - linha) * modulo
        for coluna, escuro in enumerate(celulas):
            if not escuro:
                continue
            x = origem_x + coluna * modulo
            comandos.append(f"{x} {y} {modulo} {modulo} re f".encode())
    texto_x = origem_x + lado * modulo + 24
    linhas = [
        (texto_x, 760, 16, zona["nome"]),
        (texto_x, 730, 12, zona["piso"]),
        (texto_x, 700, 11, "Onde colar:"),
        (texto_x, 680, 11, zona["local_qr"]),
        (40, 80, 9, url),
    ]
    bloco = [b"BT"]
    for x, y, tamanho, texto in linhas:
        bloco.append(f"/F1 {tamanho} Tf".encode())
        bloco.append(f"1 0 0 1 {x} {y} Tm".encode())
        bloco.append(_literal(texto) + b" Tj")
    bloco.append(b"ET")
    return b"\n".join(comandos + bloco)


def pdf_etiquetas(zonas: list[dict]) -> bytes:
    if not zonas:
        zonas = [{"nome": "Sem zonas", "piso": "", "local_qr": "", "url": "sem-zona"}]
    paginas = [_pagina(zona) for zona in zonas]
    quantidade = len(paginas)
    # 1 catálogo, 2 páginas, 3 fonte, depois conteúdo e página de cada etiqueta.
    ids_pagina = [5 + (indice * 2) for indice in range(quantidade)]
    kids = " ".join(f"{numero} 0 R" for numero in ids_pagina)
    objetos = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        f"<< /Type /Pages /Kids [{kids}] /Count {quantidade} >>".encode(),
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>",
    ]
    for indice, conteudo in enumerate(paginas):
        objetos.append(
            f"<< /Length {len(conteudo)} >>\nstream\n".encode()
            + conteudo
            + b"\nendstream"
        )
        objetos.append(
            (
                f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] "
                f"/Contents {4 + indice * 2} 0 R "
                f"/Resources << /Font << /F1 3 0 R >> >> >>"
            ).encode()
        )
    saida = bytearray(b"%PDF-1.4\n")
    offsets = []
    for numero, corpo in enumerate(objetos, start=1):
        offsets.append(len(saida))
        saida += f"{numero} 0 obj\n".encode() + corpo + b"\nendobj\n"
    xref = len(saida)
    saida += f"xref\n0 {len(objetos) + 1}\n".encode()
    saida += b"0000000000 65535 f \n"
    for offset in offsets:
        saida += f"{offset:010d} 00000 n \n".encode()
    saida += (
        f"trailer << /Size {len(objetos) + 1} /Root 1 0 R >>\n"
        f"startxref\n{xref}\n%%EOF"
    ).encode()
    return bytes(saida)
