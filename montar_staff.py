"""Gera staff/index.html (equipe e filiados) usando castings/index.html como molde.

Editar a lista STAFF e rodar: python montar_staff.py
- instagram: só o @ (sem link); vazio = o botão vira "Instagram em breve".
- site: opcional, tupla (rótulo, url) para link público adicional (ex.: rádio/TV web).
- ativo=False: a pessoa fica fora da página até a Anne liberar.
"""
import html
import re
from pathlib import Path

RAIZ = Path(__file__).parent

STAFF = [
    # nome, função, instagram, site, ativo
    (
        "Glee Vinicius Produções",
        "Filiado terceirizado: fotógrafo, cinegrafista, composite e produtor de cinema, TV e teatro.",
        "gleeproducoes",
        None,
        True,
    ),
    (
        "Edição Fofoca dos Famosos · Vadú Braga (Edvaldo)",
        "Mídia e cobertura ao vivo de eventos, filiado à agência com contrato 2026 atualizado.",
        "tvnoticiasvadubraga",
        None,
        True,
    ),
    (
        "Paulo Maisfm",
        "Filiado em TV e rádio web internacional (Mais FM), com transmissões ao vivo e divulgação de serviços da agência.",
        "radiomaisfmbh",
        ("Site maisfm.top", "https://maisfm.top/"),
        True,
    ),
    (
        "Karina Silva",
        "Jornalista, assessora do Vadú Braga e filiada em mídia de eventos.",
        "",
        None,
        True,
    ),
    (
        "Clarice Grigati",
        "Scouter e filiada em Recife (PE), atua na divulgação e venda de cursos online da agência.",
        "",
        None,
        True,
    ),
]

DOCUMENTOS = [
    ("Credencial de filiação (PDF)", "arquivos/credencial-filiacao.pdf", True),
    ("Cartilha do scouter filiado (PDF)", "arquivos/cartilha-scouter-filiado.pdf", False),
    ("Área de documentos da equipe (com senha)", "documentos/", False),
]

TITULO = "Staff e filiados · Anne Models Management"
DESCRICAO = "Equipe e profissionais filiados à Anne Models Management: fotografia, mídia, imprensa e eventos."
URL = "https://annemodels.com.br/staff/"

E = html.escape


def cartao(nome, funcao, insta, site=None):
    acoes = []
    if insta:
        acoes.append(
            f'<a href="https://www.instagram.com/{E(insta)}/" target="_blank" rel="noopener" '
            f'style="display:inline-flex;align-items:center;min-height:48px;padding:12px 18px;'
            f'border:1px solid #3b3a37;color:#3b3a37;text-decoration:none;font:500 12px/1.2 Jost,sans-serif;'
            f'letter-spacing:.14em;text-transform:uppercase" style-hover="background:#80622a;border-color:#80622a;color:#fff">'
            f'Instagram @{E(insta)}</a>'
        )
    if site:
        rotulo, href = site
        acoes.append(
            f'<a href="{E(href)}" target="_blank" rel="noopener" '
            f'style="display:inline-flex;align-items:center;min-height:48px;padding:12px 18px;'
            f'border:1px solid #b08d57;color:#80622a;text-decoration:none;font:500 12px/1.2 Jost,sans-serif;'
            f'letter-spacing:.14em;text-transform:uppercase" style-hover="background:#80622a;border-color:#80622a;color:#fff">'
            f'{E(rotulo)}</a>'
        )
    if acoes:
        rodape = f'<div style="margin-top:auto;padding-top:8px;display:flex;flex-wrap:wrap;gap:10px">{"".join(acoes)}</div>'
    else:
        rodape = '<div style="margin-top:auto;padding-top:8px"><span style="font:500 12px/1.2 Jost,sans-serif;letter-spacing:.14em;text-transform:uppercase;color:#80622a">Instagram em breve</span></div>'
    return (f'<li style="display:flex;flex-direction:column;gap:10px;background:#fff;border:1px solid #dfd5c0;'
            f'border-top:3px solid #b08d57;padding:24px">'
            f'<h3 style="font:400 clamp(24px,2.4vw,30px)/1.12 \'Bodoni Moda\',serif;text-wrap:balance;color:#3b3a37">{E(nome)}</h3>'
            f'<p style="font-size:15px;color:#4a4740;line-height:1.5">{E(funcao)}</p>{rodape}</li>')


def botao_doc(rotulo, href, principal):
    cor = ("background:#80622a;color:#fff;border:1px solid #80622a" if principal
           else "background:transparent;color:#3b3a37;border:1px solid #3b3a37")
    extra = ' download' if href.endswith('.pdf') else ''
    return (f'<a href="{E(href)}"{extra} style="display:inline-flex;align-items:center;justify-content:center;min-height:52px;'
            f'padding:14px 24px;font:500 13px/1.2 Jost,sans-serif;letter-spacing:.14em;text-transform:uppercase;'
            f'text-decoration:none;{cor}">{E(rotulo)}</a>')


def main_html():
    pessoas = "".join(cartao(n, f, i, s) for n, f, i, s, ativo in STAFF if ativo)
    docs = "".join(botao_doc(*d) for d in DOCUMENTOS)
    largura = "width:min(1240px, calc(100% - 40px));margin:0 auto"
    return f"""<main>
<section style="background:#faf8f3;border-bottom:1px solid #e6decb;padding:clamp(56px,7vw,104px) 0">
  <div style="{largura};display:grid;gap:24px;justify-items:start">
    <p style="display:inline-flex;align-items:center;gap:12px;font:500 12px/1.4 Jost,sans-serif;letter-spacing:.22em;text-transform:uppercase;color:#80622a"><span style="width:28px;height:1px;background:#b08d57;display:inline-block"></span>Equipe · Staff e filiados</p>
    <h1 style="font:400 clamp(48px,7vw,104px)/.96 'Bodoni Moda',Didot,serif;letter-spacing:-.025em;text-wrap:balance;color:#2c2b28">Quem faz a agência <em style="font-style:italic;color:#80622a">acontecer.</em></h1>
    <p style="font-size:clamp(17px,1.4vw,20px);line-height:1.65;color:#3a3833;max-width:56ch;text-wrap:pretty">Profissionais filiados à Anne Models Management atuam com suas próprias empresas: fotografia, mídia, imprensa e eventos. Fale direto com cada um pelo Instagram.</p>
  </div>
</section>
<section style="background:#ffffff;padding:clamp(56px,7vw,96px) 0">
  <div style="{largura}">
    <ul style="list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,340px),1fr));gap:20px">{pessoas}</ul>
  </div>
</section>
<section style="background:#faf8f3;border-top:1px solid #e6decb;padding:clamp(56px,7vw,96px) 0">
  <div style="{largura};display:grid;gap:20px;justify-items:start">
    <p style="font:500 12px/1.4 Jost,sans-serif;letter-spacing:.22em;text-transform:uppercase;color:#80622a">Para filiados e equipe</p>
    <h2 style="font:400 clamp(36px,4.8vw,68px)/1.02 'Bodoni Moda',Didot,serif;letter-spacing:-.015em;text-wrap:balance;color:#2c2b28">Documentos</h2>
    <p style="font-size:clamp(17px,1.4vw,20px);line-height:1.65;color:#3a3833;max-width:56ch;text-wrap:pretty">Baixe a credencial para imprimir e assinar. A área da equipe, com senha, guarda os contratos e recebe as versões revisadas.</p>
    <div style="display:flex;flex-wrap:wrap;gap:12px">{docs}</div>
  </div>
</section>
</main>"""


SCRIPT = """<script type="text/x-dc" data-dc-script="" data-props="{}">
class Component extends DCLogic {
  renderVals() { return {}; }
}
</script>"""


def montar():
    base = (RAIZ / "castings" / "index.html").read_text(encoding="utf-8")
    out = base.replace("<title>Castings · Anne Models Management</title>", f"<title>{E(TITULO)}</title>")
    out = re.sub(r'(<meta name="description" content=")[^"]*', lambda m: m.group(1) + E(DESCRICAO), out, count=1)
    out = re.sub(r'(<meta property="og:description" content=")[^"]*', lambda m: m.group(1) + E(DESCRICAO), out, count=1)
    out = re.sub(r'(<meta property="og:title" content=")[^"]*', lambda m: m.group(1) + "Staff e filiados", out, count=1)
    out = out.replace("https://annemodels.com.br/castings/", URL)
    out = out.replace('atual="castings"', 'atual="staff"')
    out, n = re.subn(r"<main>.*?</main>", lambda m: main_html(), out, count=1, flags=re.S)
    assert n == 1, "molde sem <main>"
    out, n = re.subn(r'<script type="text/x-dc".*?</script>', lambda m: SCRIPT, out, count=1, flags=re.S)
    assert n == 1, "molde sem script do componente"
    assert "castings" not in out.split("<x-dc>")[0].replace("cast-", ""), "sobrou castings no head"
    destino = RAIZ / "staff" / "index.html"
    destino.parent.mkdir(exist_ok=True)
    destino.write_text(out, encoding="utf-8")
    print("ok:", destino)


if __name__ == "__main__":
    montar()
