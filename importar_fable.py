"""Importa as páginas do Fable (.dc.html empacotadas) para o site estático.

Cada .dc.html do Fable traz tudo dentro: o HTML (template), e fontes, imagens,
React, support.js, cabeçalho e rodapé num "manifest" em base64. Este script
desempacota isso em arquivos normais (assets/dc/), grava cada página na rota
que ela já tinha no site e corrige links e o <head> (SEO, noindex).

Uso: python importar_fable.py <pasta com os .dc.html>
Depois: python gerar.py (só refaz a apostila e o 404).
"""
import base64, gzip, hashlib, html, json, re, sys
from pathlib import Path

RAIZ = Path(__file__).parent
SAIDA = RAIZ / "assets" / "dc"
SITE_URL = "https://annemodels.com.br/"

# arquivo do Fable -> (rota no site, título, descrição)
PAGINAS = {
    "Home Anne Models": ("", "Anne Models Management", "Agência de modelos, manequins e atores desde 1995. Formação profissional, castings, serviços e o Fashion Trade."),
    "Agencia": ("a-agencia/", "A agência", "História da Anne Models Management e da fundadora Anne Mac Pherson."),
    "Castings": ("castings/", "Castings", "Modelos, atores, dançarinos e cantores para marcas, produtoras e eventos."),
    "Cursos": ("cursos/", "Cursos", "Método Anne Mac Pherson, Integração Profissional e Recepcionistas de eventos."),
    "Metodo": ("cursos/metodo-anne-mac-pherson/", "Método Anne Mac Pherson", "Formação profissional completa de modelo, manequim e ator, com certificado de capacitação técnica."),
    "Integracao": ("cursos/integracao-profissional/", "Integração Profissional", "Imagem, atendimento e liderança para lojistas e profissionais."),
    "Recepcionistas": ("cursos/recepcionistas-de-eventos/", "Recepcionistas de eventos", "Postura, etiqueta e comunicação para trabalhar em grandes eventos."),
    "Servicos": ("servicos/", "Serviços", "Catálogo de serviços e preços da Anne Models Management."),
    "Lifestyle": ("servicos/lifestyle/", "Portal Lifestyle", "Programa Lifestyle da Anne Models no YouTube."),
    "RevistaFashionModels": ("servicos/revista-fashion-models/", "Revista Fashion Models", "Revista Fashion Models, filiada à Anne Models Management."),
    "RevistaKrystal": ("servicos/revista-krystal/", "Revista Krystal", "Revista Krystal, filiada à Anne Models Management."),
    "FashionTrade": ("fashion-trade/", "Fashion Trade", "Programação e formas de participar do Fashion Trade, evento anual da Anne Models."),
    "TradeSales": ("trade-sales/", "Trade Sales", "Curadoria de produtos para book, desfiles e trabalho de modelos e artistas."),
    "AreaDoAluno": ("area-do-aluno/", "Área do aluno", "Acesso às aulas, apostilas, tarefas e certificados dos cursos da Anne Models."),
    "Contato": ("contato/", "Contato", "WhatsApp, e-mails e redes da Anne Models Management."),
}
ROTA = {f"{k}.dc.html": v[0] for k, v in PAGINAS.items()}
ROTA["Home%20Anne%20Models.dc.html"] = ""

# Ajustes sobre o que veio do Fable (texto exato -> substituto), reaplicados a cada importação.
AJUSTES = {
    # a apostila de leitura + PDF já existe (gerar.py); o botão do Fable só pedia por WhatsApp
    "Metodo": [
        ('href="https://wa.me/5531996589729?text=Ol%C3%A1!%20Quero%20receber%20a%20apostila%20do%20M%C3%A9todo%20Anne%20Mac%20Pherson." target="_blank" rel="noopener"',
         'href="cursos/metodo-anne-mac-pherson/apostila/"'),
        ("Pedir a apostila em PDF", "Ler a apostila"),
        # respostas da Anne em 15/11: menor de 18 vai com o responsável; sexta das 19h às 22h
        ("Menores de 16 anos participam com autorização do responsável.",
         "Menores de 18 anos participam com um responsável, que acompanha todas as etapas."),
        ("Sexta-feira</span>", "Sexta-feira, 19h às 22h</span>"),
    ],
    "Cursos": [("Menores de 16 anos com autorização do responsável.", "Menores de 18 anos com um responsável presente.")],
    # Anne em 15/11: só SP (outubro) e Salvador (novembro); dia e local saem para quem concluir o curso
    "FashionTrade": [
        (r"(?s)<li[^>]*>(?:Belo Horizonte|Rio de Janeiro|Pernambuco)</li>", ""),
        ("Próxima edição", "Próximas edições"),
        ("Data e local a anunciar", "São Paulo, outubro<br>Salvador, novembro"),
        ("Deixe seu WhatsApp e avisamos assim que a data sair.",
         "Dia, local e programação completa são enviados a quem concluir o curso online. Hotel, alimentação e transporte ficam à parte."),
        ("Sexta · 18h às 22h", "Sexta · 19h às 22h"),
        ("Mulher Total 40+", "Plenitude 40+"),  # nome unissex sugerido; falta a Anne aprovar
    ],
    # depoimentos ainda são caixas vazias: escondidos até a Anne mandar fotos e falas autorizadas
    "Home Anne Models": [
        (r"(?s)<section[^>]*>(?:(?!</section>).)*?Quem passou(?:(?!</section>).)*</section>", ""),
        ("Menores de 16 anos se cadastram com um responsável", "Menores de 18 anos se cadastram com um responsável"),
        # cartão do Fashion Trade na home: mesmas cidades e meses da página do evento (Anne, 15/11)
        (r"(?s)\n\s*<span[^>]*>(?:Belo Horizonte|Rio de Janeiro|Pernambuco)</span>", ""),
        (">Próxima edição<", ">Próximas edições<"),
        (">Data a anunciar<", ">São Paulo, outubro<br>Salvador, novembro<"),
    ],
    # a Anne ainda não informou plataforma de aulas; o link era um exemplo
    "AreaDoAluno": [(r'(?s)<a href="https://hotmart\.com"[^>]*>Entrar na Hotmart</a>', "")],
}

# cabeçalho: no celular (< 440 px) "Cadastre-se grátis" vira "Cadastro" para o botão Menu caber na tela
AJUSTES_COMPONENTES = [
    ("state = { wide: window.innerWidth >= 1080, aberto: false };",
     "state = { wide: window.innerWidth >= 1080, curto: window.innerWidth < 440, aberto: false };"),
    ("this.setState({ wide: window.innerWidth >= 1080 })",
     "this.setState({ wide: window.innerWidth >= 1080, curto: window.innerWidth < 440 })"),
    ("return { links, wide,", "return { cta: this.state.curto ? 'Cadastro' : 'Cadastre-se grátis', links, wide,"),
    (">Cadastre-se grátis</a>", ">{{ cta }}</a>"),
]

EXT = {"image/png": "png", "image/jpeg": "jpg", "image/webp": "webp", "image/svg+xml": "svg",
       "font/woff2": "woff2", "font/woff": "woff", "text/html": "html", "text/css": "css",
       "application/javascript": "js", "text/javascript": "js"}


def blocos(s):
    pega = lambda t: re.search(rf'<script type="__bundler/{t}">(.*?)</script>', s, re.S).group(1)
    return json.loads(pega("manifest")), json.loads(pega("template")), json.loads(pega("ext_resources"))


def link(href, rota):
    """Link do Fable -> link relativo à raiz do site (a página tem <base> apontando para a raiz)."""
    if href.startswith("#"):
        return rota + href
    nome, _, ancora = href.partition("#")
    if nome in ROTA:
        return ROTA[nome] + ("#" + ancora if ancora else "")
    return href


def arruma_links(txt, rota):
    txt = re.sub(r'href="([^"{]*)"', lambda m: f'href="{html.escape(link(html.unescape(m.group(1)), rota), quote=True)}"', txt)
    # links montados no JavaScript dos componentes ('Agencia.dc.html', 'Integracao.dc.html#milao')
    nomes = "|".join(re.escape(n) for n in sorted(ROTA, key=len, reverse=True))
    return re.sub(rf"(?<![\w./])({nomes})", lambda m: ROTA[m.group(1)], txt)


def grava(dados, mime):
    nome = hashlib.sha256(dados).hexdigest()[:12] + "." + EXT.get(mime.split(";")[0], "bin")
    (SAIDA / nome).write_bytes(dados)
    return "assets/dc/" + nome


def importa(arq, rota, titulo, desc):
    manifest, tpl, ext = blocos(arq.read_text(encoding="utf-8"))
    caminhos = {}
    for uuid, e in manifest.items():
        dados = base64.b64decode(e["data"])
        if e.get("compressed"):
            dados = gzip.decompress(dados)
        caminhos[uuid] = (dados, e["mime"])
    # cabeçalho/rodapé (.dc.html) e React vêm por window.__resources; o support.js busca por esses nomes
    recursos = {}
    for r in ext:
        dados, mime = caminhos.pop(r["uuid"])
        if r["id"].endswith(".dc.html"):
            txt = arruma_links(dados.decode("utf-8"), "")
            for velho, novo in AJUSTES_COMPONENTES:
                txt = txt.replace(velho, novo)
            dados = txt.encode("utf-8")
        recursos[r["id"]] = grava(dados, mime)
    for uuid, (dados, mime) in caminhos.items():
        tpl = tpl.replace(uuid, grava(dados, mime))
    tpl = arruma_links(tpl, rota)
    for velho, novo in AJUSTES.get(arq.name.removesuffix(".dc.html"), []):
        tpl, n = re.subn(velho if velho.startswith("(?") else re.escape(velho), novo, tpl)
        assert n >= 1, (arq.name, velho[:60])

    base = "../" * rota.count("/") or "./"
    canon = SITE_URL + rota
    head = f"""<base href="{base}">
<title>{html.escape(titulo + ("" if not rota else " · Anne Models Management"))}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{canon}">
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Anne Models Management">
<meta property="og:title" content="{html.escape(titulo)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{canon}">
<meta property="og:image" content="{SITE_URL}img/anne-fundadora.jpg">
<meta property="og:locale" content="pt_BR">
<script>window.__resources = {json.dumps(recursos)};</script>
"""
    tpl, n = re.subn(r'(<meta name="viewport"[^>]*>)', lambda m: m.group(1) + "\n" + head, tpl, count=1)
    assert n == 1, arq.name
    destino = RAIZ / rota / "index.html"
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text(tpl, encoding="utf-8", newline="\n")
    print(f"{arq.name:32} -> /{rota}")


def main(pasta):
    pasta = Path(pasta)
    SAIDA.mkdir(parents=True, exist_ok=True)
    for velho in SAIDA.iterdir():
        velho.unlink()
    for nome, (rota, titulo, desc) in PAGINAS.items():
        importa(pasta / f"{nome}.dc.html", rota, titulo, desc)
    imgs = pasta / "img"
    if imgs.is_dir():
        for f in imgs.rglob("*"):
            if f.is_file():
                alvo = RAIZ / "img" / f.relative_to(imgs)
                alvo.parent.mkdir(parents=True, exist_ok=True)
                alvo.write_bytes(f.read_bytes())
    import paleta_branca
    paleta_branca.main()  # site branco e dourado (Anne, 15/11)


if __name__ == "__main__":
    main(sys.argv[1])
