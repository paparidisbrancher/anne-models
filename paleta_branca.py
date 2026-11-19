"""Paleta branca e dourada no site inteiro (pedido da Anne em 15/11/2026: "site branco com dourado igual ao cartão").

Fundo preto e creme -> branco; texto preto -> cinza-escuro (#3b3a37); dourado claro -> dourado escuro
(o claro some no branco); botões escuros -> dourado escuro com texto branco.
Roda sobre as páginas prontas (preserva o que foi editado à mão) e no fim do importar_fable.py.
Idempotente: depois de aplicado não sobra preto nem creme para trocar.
Uso: python paleta_branca.py
"""
import re
from pathlib import Path

RAIZ = Path(__file__).parent
CINZA, BRANCO, OURO, OURO_ESC = "#3b3a37", "#ffffff", "#b08d57", "#80622a"
ESCUROS = ("#0d0d0c", "#1b1a17", "#26241f")
CLAROS = ("#f7f5f0", "#f4eee3", "#f1eee7", "#f1eadc")
# troca de cor sem contexto (blocos <style>, JS dos componentes, gradientes)
TOKENS = [(r"#0d0d0c|#1b1a17|#26241f", CINZA), (r"#f7f5f0|#f4eee3|#f1eee7|#f1eadc", BRANCO),
          (r"rgba\(\s*247\s*,\s*245\s*,\s*240", "rgba(59,58,55"), (r"rgba\(\s*13\s*,\s*13\s*,\s*12", "rgba(255,255,255")]


def tokens(txt):
    for velho, novo in TOKENS:
        txt = re.sub(velho, novo, txt, flags=re.I)
    return txt


def declaracoes(css, interativo):
    """Troca as cores de uma lista de declarações CSS (style, style-hover, style-focus)."""
    botao = interativo or bool(re.search(r"cursor:\s*pointer|inline-flex", css))
    fundo_escuro = bool(re.search(r"background(?:-color)?:\s*(?:%s)\b" % "|".join(ESCUROS), css, re.I))
    fundo_colorido = bool(re.search(r"background(?:-color)?:\s*#(?:1a7f45|14663a|80622a|b08d57)", css, re.I))
    saida = []
    for d in re.split(r";(?![^(]*\))", css):
        if ":" not in d or "{{" in d:
            saida.append(d)
            continue
        prop, val = d.split(":", 1)
        p = prop.strip().lower()
        if p.startswith("background"):
            # véu creme: opaco vira branco; translúcido (cartão sobre fundo escuro) vira um toque de dourado
            val = re.sub(r"rgba\(\s*247\s*,\s*245\s*,\s*240\s*,\s*([\d.]+)\s*\)",
                         lambda m: f"rgba({'255,255,255' if float(m.group(1)) >= .5 else '176,141,87'},{m.group(1)})", val)
            val = re.sub(r"rgba\(\s*255\s*,\s*255\s*,\s*255\s*,\s*0?\.(?:1[468]|25?)\s*\)", "#dfd5c0", val)
            if botao and fundo_escuro:
                val = re.sub("|".join(ESCUROS), OURO_ESC, val, flags=re.I)
            val = re.sub("|".join(ESCUROS), BRANCO, val, flags=re.I)
        elif p == "color" or p.startswith("border") or p.startswith("outline") or p in ("fill", "stroke", "text-decoration-color"):
            if p == "color" and botao and fundo_escuro:
                val = re.sub("|".join(CLAROS), BRANCO, val, flags=re.I)
            elif p == "color" and not interativo and not fundo_colorido:
                # texto branco sobre foto escurecida ou fundo preto: o fundo agora é claro
                val = re.sub(r"#fff(?:fff)?\b|\bwhite\b", CINZA, val, flags=re.I)
            elif p.startswith("border") and botao and fundo_escuro:
                val = re.sub("|".join(ESCUROS), OURO_ESC, val, flags=re.I)
            if p.startswith("border"):
                val = re.sub(r"rgba\(\s*255\s*,\s*255\s*,\s*255\s*,\s*0?\.(?:1[468]|25?)\s*\)", "#dfd5c0", val)
            val = re.sub("#d9c29b", OURO_ESC if p == "color" else OURO, val, flags=re.I)
            val = re.sub("|".join(CLAROS), CINZA if p == "color" else "#dcd8cf", val, flags=re.I)
            val = re.sub("|".join(ESCUROS), CINZA, val, flags=re.I)
            val = re.sub(r"rgba\(\s*217\s*,\s*194\s*,\s*155", "rgba(128,98,42", val)
        saida.append(f"{prop}:{tokens(val)}")
    return ";".join(saida)


# véu da capa da home: no fundo claro o texto cinza precisa de mais branco por trás (no celular o texto ocupa a largura toda)
VEUS = [("linear-gradient(180deg,rgba(255,255,255,0) 45%,rgba(255,255,255,.7) 100%)",
         "linear-gradient(180deg,rgba(255,255,255,0) 28%,rgba(255,255,255,.9) 58%,rgba(255,255,255,.95) 100%)")]


def aplica(txt):
    for velho, novo in VEUS:
        txt = txt.replace(velho, novo)
    txt = re.sub(r'(style(-hover|-focus)?=")([^"]*)(")',
                 lambda m: m.group(1) + declaracoes(m.group(3), bool(m.group(2))) + m.group(4), txt)
    return tokens(txt)


def logo():
    """AN da logo oficial (aprovado em 15/11) no lugar do AN antigo do Fable: mesmos nomes de arquivo + favicon."""
    import re as _re, shutil
    png = RAIZ / "assets" / "an-oficial.png"
    for destino in ("img/logo-an.png", "assets/logo-an.png", "assets/dc/f7058975b634.png"):
        if (RAIZ / destino).exists():
            shutil.copyfile(png, RAIZ / destino)
    svg = (RAIZ / "assets" / "an-oficial.svg").read_text(encoding="utf-8")
    vb = _re.search(r'viewBox="([^"]+)"', svg).group(1)
    d = _re.search(r' d="([^"]+)"', svg).group(1)
    (RAIZ / "assets" / "favicon.svg").write_text(
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><rect width="100" height="100" rx="16" fill="#ffffff"/>'
        f'<svg x="9" y="14" width="82" height="72" viewBox="{vb}"><path fill="#b08d57" fill-rule="evenodd" d="{d}"/></svg></svg>',
        encoding="utf-8")


def main():
    logo()
    arquivos = [p for p in RAIZ.rglob("*.html") if "_fonte" not in p.parts]
    for p in arquivos:
        velho = p.read_text(encoding="utf-8")
        novo = aplica(velho)
        if novo != velho:
            p.write_text(novo, encoding="utf-8", newline="\n")
            print("paleta:", p.relative_to(RAIZ))


if __name__ == "__main__":
    assert "#ffffff" in declaracoes("background:#0d0d0c;color:#f7f5f0", False)                  # seção escura vira branca
    assert OURO_ESC in declaracoes("display:inline-flex;background:#0d0d0c;color:#f7f5f0", False)  # botão vira dourado
    assert CINZA in declaracoes("color:#0d0d0c", False) and aplica(aplica("a")) == "a"
    main()
