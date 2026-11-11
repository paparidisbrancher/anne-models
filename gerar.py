"""Gera as páginas do site Anne Models.

Uso: python gerar.py
Edite os textos aqui (ou em assets/servicos.json) e rode de novo.
Em cada página, {P} vira o caminho relativo até a raiz.
"""
import json
from pathlib import Path
from urllib.parse import quote

RAIZ = Path(__file__).parent

# Contatos e links. None = ainda não recebido (ver PENDENCIAS.md).
CONFIG = {
    "wa_agencia": "5531973023077",
    "wa_catalogo": "5531996589729",  # número que aparece nos cartazes do catálogo
    "wa_jane": None,
    "email_ceo": "annemacphersonceomodels@gmail.com",  # e-mail que consta no contrato de filiação
    "email_cursos": "annypraddocursos@gmail.com",
    "email_assessoria": "annymodelsassessoria@gmail.com",
    "form_cadastro": "https://forms.gle/VuQUWbzRoZpm6ykv9",
    "contrato_agenciamento": None,
    "comunidade_cristal": None,
    "youtube_eventos": "https://www.youtube.com/@TVANNYPRADDOEVENTOS",
    "youtube_fashion_trade": "https://www.youtube.com/@ANNYTVFashiontrade",
    "youtube_lifestyle": "https://www.youtube.com/@ANNYTVFashiontrade",  # a confirmar: canal "Lifestyle with Anne Mac Pherson"
    "instagram": "https://www.instagram.com/anny_praddo_modeling_career",
    "site_url": "https://paparidisbrancher.github.io/anne-models/",
}


def wa(msg, num=None):
    return f"https://wa.me/{num or CONFIG['wa_agencia']}?text={quote(msg)}"


def ext(href, txt, cls="btn btn-solid"):
    return f'<a class="{cls}" href="{href}" target="_blank" rel="noopener">{txt}</a>'


# ---------------------------------------------------------------- layout

NAV = [
    ("a-agencia/", "Agência"),
    ("servicos/", "Serviços"),
    ("cursos/", "Cursos"),
    ("castings/", "Castings"),
    ("fashion-trade/", "Fashion Trade"),
    ("contato/", "Contatos"),
]

ICONES = """<svg width="0" height="0" style="position:absolute" aria-hidden="true">
  <symbol id="logo-a" viewBox="0 0 100 100"><path fill="currentColor" d="M50 4 L53 4 L96 96 L84 96 Z M50 4 L47.5 4 L6 96 L9 96 Z M30 84 L50 74 L70 84 L66 86 L50 79 L34 86 Z"/></symbol>
  <!-- provisório: monograma A+N até a Anne enviar a logo oficial -->
  <symbol id="logo-an" viewBox="0 0 140 100"><path fill="currentColor" d="M50 4 L53 4 L96 96 L84 96 Z M50 4 L47.5 4 L6 96 L9 96 Z M30 84 L50 74 L70 84 L66 86 L50 79 L34 86 Z M89 4 L101 4 L130 78 L130 4 L134 4 L134 96 L129 96 L93 7 L93 96 L89 96 Z"/></symbol>
  <symbol id="i-wa" viewBox="0 0 24 24"><path fill="currentColor" d="M12 2a10 10 0 0 0-8.66 15l-1.3 4.76 4.88-1.28A10 10 0 1 0 12 2Zm0 18.2a8.2 8.2 0 0 1-4.18-1.15l-.3-.18-2.9.76.78-2.83-.2-.3A8.2 8.2 0 1 1 12 20.2Zm4.5-6.14c-.25-.12-1.46-.72-1.69-.8-.23-.08-.39-.12-.56.12-.16.25-.64.8-.78.97-.14.16-.29.18-.53.06a6.7 6.7 0 0 1-3.32-2.9c-.25-.43.25-.4.72-1.33.08-.16.04-.3-.02-.43l-.76-1.83c-.2-.48-.4-.41-.56-.42h-.47a.9.9 0 0 0-.66.31 2.76 2.76 0 0 0-.86 2.05 4.8 4.8 0 0 0 1 2.54 11 11 0 0 0 4.2 3.7c1.56.68 2.18.73 2.96.62.48-.07 1.46-.6 1.67-1.18.2-.58.2-1.08.14-1.18-.06-.1-.22-.16-.47-.28Z"/></symbol>
  <symbol id="i-grid" viewBox="0 0 24 24"><path fill="none" stroke="currentColor" stroke-width="1.5" d="M4 4h7v7H4zM13 4h7v7h-7zM4 13h7v7H4zM13 13h7v7h-7z"/></symbol>
  <symbol id="i-book" viewBox="0 0 24 24"><path fill="none" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round" d="M4 5.5C6.5 4 9.5 4 12 5.5v14c-2.5-1.5-5.5-1.5-8 0zM20 5.5C17.5 4 14.5 4 12 5.5v14c2.5-1.5 5.5-1.5 8 0z"/></symbol>
  <symbol id="i-pen" viewBox="0 0 24 24"><path fill="none" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round" d="M4 20h4L19 9l-4-4L4 16zM13 7l4 4"/></symbol>
</svg>"""


def layout(rota, titulo, descricao, corpo, *, hero=False, extra=""):
    nivel = rota.count("/")
    p = "../" * nivel
    nav_links = "".join(
        f'<a href="{p}{h}"{" aria-current=\"page\"" if h == rota else ""}>{t}</a>'
        for h, t in NAV
    )
    wa_geral = wa("Olá! Vim pelo site da Anne Models.")
    pagina_titulo = "Anne Models Management" if not rota else f"{titulo} | Anne Models"
    html = f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{pagina_titulo}</title>
<meta name="description" content="{descricao}">
<meta name="robots" content="noindex, nofollow">
<meta name="theme-color" content="#0d0d0c">
<meta property="og:type" content="website">
<meta property="og:locale" content="pt_BR">
<meta property="og:title" content="{pagina_titulo}">
<meta property="og:description" content="{descricao}">
<meta property="og:url" content="{CONFIG['site_url']}{rota}">
<meta property="og:image" content="{CONFIG['site_url']}img/hero.jpg">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{p}assets/favicon.svg" type="image/svg+xml">
<script>document.documentElement.classList.add('js')</script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bodoni+Moda:ital,opsz,wght@0,6..96,400;0,6..96,500;1,6..96,400&family=Jost:wght@300;400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{p}assets/site.css">
</head>
<body data-wa="{CONFIG['wa_agencia']}"{' class="interna"' if not hero else ''}>
{ICONES}
<a class="skip" href="#conteudo">Pular para o conteúdo</a>
<header class="top" id="topo">
  <div class="wrap">
    <a class="brand" href="{p or './'}" aria-label="Anne Models, página inicial"><svg class="logo-an" aria-hidden="true"><use href="#logo-an"/></svg><span>ANNE MODELS</span></a>
    <nav class="menu" id="menuNav" aria-label="Principal">
      {nav_links}
      <a class="menu-util" href="{p}area-do-aluno/">Área do aluno</a>
    </nav>
    <div class="top-actions">
      <a class="btn btn-ghost top-cta" href="{p}#cadastro">Cadastre-se grátis</a>
      <button class="menu-btn" id="menuBtn" type="button" aria-expanded="false" aria-controls="menuNav"><span></span><span class="sr">Menu</span></button>
    </div>
  </div>
</header>
<main id="conteudo">
{corpo}
</main>
<footer class="foot">
  <div class="wrap">
    <p class="foot-copy"><span>Anne Models Management</span><span>CNPJ 49.330.189/0001-70</span><span>Direitos autorais reservados de acordo com a Lei 9.610</span></p>
  </div>
</footer>
<nav class="dock" aria-label="Atalhos">
  <a href="{p}cursos/"><svg aria-hidden="true"><use href="#i-book"/></svg>Cursos</a>
  <a href="{p}servicos/"><svg aria-hidden="true"><use href="#i-grid"/></svg>Serviços</a>
  <a href="{p}#cadastro"><svg aria-hidden="true"><use href="#i-pen"/></svg>Cadastro</a>
  <a class="wa" href="{wa_geral}" target="_blank" rel="noopener"><svg aria-hidden="true"><use href="#i-wa"/></svg>WhatsApp</a>
</nav>
<a class="wa-fab" href="{wa_geral}" target="_blank" rel="noopener" aria-label="Falar no WhatsApp"><svg aria-hidden="true"><use href="#i-wa"/></svg></a>
{extra}
<script src="{p}assets/site.js" defer></script>
</body>
</html>
"""
    return html.replace("{P}", p)


def cabeca(eyebrow, titulo, lead, acoes=""):
    return f"""<section class="page-head"><div class="wrap">
  <p class="eyebrow">{eyebrow}</p>
  <h1>{titulo}</h1>
  <p class="lead">{lead}</p>
  {f'<div class="ctas">{acoes}</div>' if acoes else ''}
</div></section>"""


# ---------------------------------------------------------------- conteúdo

CURSOS = [
    {
        "slug": "metodo-anne-mac-pherson",
        "nome": "Método Anne Mac <em>Pherson</em>",
        "nome_txt": "Método Anne Mac Pherson",
        "tag": "Modelos, manequins e atores",
        "resumo": "Formação profissional completa de modelo, manequim e ator, com todos os módulos para obter o Certificado de Capacitação Técnica (CCT).",
        "publico": "Quem quer trabalhar como modelo, manequim ou ator, de crianças a adultos. Menores de 16 anos participam com autorização do responsável.",
        "objetivo": "Preparar para o mercado da moda e da publicidade e chegar ao CCT, documento usado para tirar o registro profissional (RPMT) e assinar contratos dentro da lei.",
        "inclui": ["Formação completa", "Desfiles de moda", "Book profissional", "Certificado de capacitação"],
        "modulos": [
            ("Auto maquiagem", None), ("Etiqueta social e profissional", None), ("Cuidados físicos e postura", None),
            ("Passarela", None), ("Expressões faciais e corporais", None), ("História da moda", None),
            ("A carreira do modelo", None), ("Preparação psicológica", None), ("Dicionário do modelo", None),
            ("Prova teórica e tarefas de cada módulo", None), ("Certificado do Método Anne Mac Pherson", None),
        ],
    },
    {
        "slug": "integracao-profissional",
        "nome": "Integração <em>Profissional</em>",
        "nome_txt": "Integração Profissional",
        "tag": "Lojistas, empresas e profissionais",
        "resumo": "Posicionamento de vida e transformação de imagem: integração profissional, social e familiar para quem quer se destacar no mercado.",
        "publico": "Lojistas, empresários, equipes e profissionais que atendem clientes e querem melhorar a própria imagem e a da empresa.",
        "objetivo": "Desenvolver imagem, comportamento, ética e colaboração na equipe, para conquistar e manter clientes.",
        "inclui": ["Aulas virtuais e presenciais", "Plano de ação personalizado", "Prova de avaliação", "Certificado de capacitação técnica"],
        "milao": True,
        "modulos": [
            ("Mente e vida", ["Autoconhecimento", "Saúde física e mental", "Ansiedade e equilíbrio emocional", "Vida pessoal e familiar", "Propósito e motivação"]),
            ("Estética e imagem pessoal", ["Corte de cabelo, cor e estilo", "Paleta de cores e looks", "Maquiagem e cuidados pessoais", "Saúde e bem-estar", "Personalidade e hobbies"]),
            ("Mídia e presença digital", ["Redes sociais e posicionamento", "Dicção, voz e comunicação", "Linguagem corporal", "Gravações e vídeos", "Atrair e manter clientes"]),
            ("Etiqueta e comportamento", ["Etiqueta social e profissional", "Relacionamento com clientes", "Atendimento e equipe", "Família e vida pessoal", "Viagens e eventos"]),
            ("Expansão profissional", ["Cursos e certificações", "Tendências internacionais", "Passaporte fashionista (Milão)", "Networking e oportunidades", "Projetos de crescimento"]),
            ("Consultoria de estilo", ["Looks para cada ocasião", "Curadoria de produtos", "Bijuterias, bolsas e calçados", "Como orientar seus clientes", "Montar looks e aumentar vendas"]),
            ("Clientes e fidelização", ["Cadastro e perfil de clientes", "Atendimento personalizado", "Programas de fidelidade", "Comunicação e pós-venda"]),
            ("Eventos e calendário comercial", ["Projetos de eventos na loja", "Datas sazonais no Brasil e no exterior", "Halloween, Dia das Mulheres, Natal", "Réveillon e ações especiais", "Marketing e divulgação"]),
            ("Imagem da boutique", ["Decoração e ambientação", "Experiência do cliente", "Design e identidade visual", "Imagem da loja e da proprietária", "Upgrade e diferenciais"]),
            ("Liderança e equipe", ["Gestão de pessoas", "Comunicação interna", "Padrões de atendimento", "Ética e profissionalismo", "Cultura de equipe"]),
            ("Plano de ação e avaliação", ["Revisão dos módulos", "Prova de avaliação", "Plano de ação personalizado", "Acompanhamento da evolução", "Certificado de capacitação técnica"]),
        ],
    },
    {
        "slug": "recepcionistas-de-eventos",
        "nome": "Recepcionistas de <em>eventos</em>",
        "nome_txt": "Recepcionistas de eventos",
        "tag": "Feiras e eventos",
        "resumo": "Treinamento especializado para trabalhar em eventos de moda, feiras e grandes eventos corporativos.",
        "publico": "Quem quer trabalhar como recepcionista em feiras, eventos de moda e eventos corporativos.",
        "objetivo": "Preparar para receber o público com postura, etiqueta e comunicação profissionais.",
        "inclui": ["Funções e atendimento profissional em eventos de moda", "Aplicação em festas, casamentos, aniversários e exposições", "Etiqueta, comunicação e imagem"],
        "modulos": [],
    },
]

# Categorias de avaliação e premiação (não são concursos)
CATEGORIAS = [
    ("Top Model of the Year", "jovens de 16 a 30 anos"),
    ("Sósias do Brasil", "covers e youtubers"),
    ("ABC do Amanhã", "baby, kids, pré-teen e teen"),
    ("Mulher Total", "plus size e 40+"),
]

# Agrupamento do catálogo
GRUPOS = {
    "Capa e mídia": ("capa", "cv-dark"),
    "Material profissional": ("material", "cv-light"),
    "Avaliação e agenciamento": ("carreira", "cv-dark"),
    "Formação": ("formacao", "cv-light"),
    "Eventos": ("eventos", "cv-dark"),
}
SERVICOS = json.loads((RAIZ / "assets" / "servicos.json").read_text(encoding="utf-8"))


def titulo_em(t):
    partes = t.rsplit(" ", 1)
    return t if len(partes) == 1 else f"{partes[0]} <em>{partes[1]}</em>"


def capa_servico(n, slug, s, tag="button"):
    cat, estilo = GRUPOS[s["tag"]]
    attrs = f'type="button" data-open="{slug}"' if tag == "button" else f'href="{{P}}servicos/#{slug}"'
    return (f'<{tag} class="cat-img cv {estilo}" {attrs} aria-label="Ver detalhes: {s["t"]}">'
            f'<span class="cv-top"><span>Nº {n:02d}</span><svg aria-hidden="true"><use href="#logo-a"/></svg></span>'
            f'<span class="cv-title">{titulo_em(s["t"])}</span>'
            f'<span class="cv-foot"><span>{s["tag"]}</span><b>{s["p"]}</b></span></{tag}>')


def cards_servicos(slugs=None, link=False):
    itens = []
    for n, (slug, s) in enumerate(SERVICOS.items(), 1):
        if slugs and slug not in slugs:
            continue
        cat = GRUPOS[s["tag"]][0]
        mais = (f'<a class="cat-more" href="{{P}}servicos/#{slug}">Ver detalhes</a>' if link
                else f'<button class="cat-more" type="button" data-open="{slug}">Ver detalhes</button>')
        itens.append(f'<li class="cat-card" data-cat="{cat}">{capa_servico(n, slug, s, "a" if link else "button")}'
                     f'<div class="cat-meta"><h3 class="sr">{s["t"]}</h3><p class="cat-sum">{s["d"][0]}</p>{mais}</div></li>')
    return '<ul class="cat-grid">' + "".join(itens) + "</ul>"


def card_curso(c, extra_cls=""):
    return f"""<li><a class="curso-card {extra_cls}" href="{{P}}cursos/{c['slug']}/">
  <span class="cv-top"><span>{c['tag']}</span><svg aria-hidden="true"><use href="#logo-a"/></svg></span>
  <span class="curso-nome">{c['nome']}</span>
  <span class="curso-resumo">{c['resumo']}</span>
  <span class="curso-link">Conhecer o curso</span>
</a></li>"""


def lista_cursos():
    estilos = ["cv-dark", "cv-light", "cv-dark"]
    return '<ul class="cursos-grid">' + "".join(card_curso(c, e) for c, e in zip(CURSOS, estilos)) + "</ul>"


FORM_CADASTRO = f"""<section class="insc" id="cadastro">
  <div class="wrap">
    <div class="insc-head reveal">
      <div><p class="eyebrow">Cadastro gratuito</p><h2>Comece pelo <em>celular</em></h2></div>
      <p class="lead">São três passos rápidos. No final, seus dados chegam ao WhatsApp da agência e você manda as fotos na mesma conversa.</p>
    </div>
    <div class="insc-grid">
      <div class="reveal">
        <div class="guide">
          <h3>Como fazer as fotos</h3>
          <ol>
            <li><b>Foto 1</b>Corpo inteiro, de frente</li>
            <li><b>Foto 2</b>Meio corpo</li>
            <li><b>Foto 3</b>De perfil</li>
            <li><b>Foto 4</b>Rosto, sério e sorrindo</li>
          </ol>
          <p>Fotografe de dia, perto de uma janela e diante de uma parede lisa. Sem filtro e sem óculos escuros. Prefira roupa simples, como camiseta preta ou branca.</p>
        </div>
        <div class="qa">
          <details><summary>O cadastro é pago?</summary><p>Não. O cadastro é gratuito.</p></details>
          <details><summary>Tem limite de idade?</summary><p>Não. Agenciamos de 6 meses a 80 anos. Quem tem menos de 16 anos se cadastra com o nome de um responsável.</p></details>
          <details><summary>Preciso ter book profissional?</summary><p>Não. Nesta etapa, fotos de celular bastam.</p></details>
        </div>
      </div>
      <form class="form reveal" id="formInsc">
        <div class="steps-nav" aria-hidden="true"><span data-s="0" class="on">1 Você</span><span data-s="1">2 Perfil</span><span data-s="2">3 Origem</span></div>
        <fieldset class="step on" data-step="0">
          <legend>Sobre você</legend>
          <label class="field"><span>Nome completo</span><input name="nome" autocomplete="name" required></label>
          <div class="row2">
            <label class="field"><span>Idade</span><input name="idade" type="number" inputmode="numeric" min="0" max="99" required></label>
            <label class="field"><span>Cidade e estado</span><input name="cidade" autocomplete="address-level2" placeholder="Ex.: Belo Horizonte, MG" required></label>
          </div>
          <label class="field" id="campoResp" hidden><span>Nome do responsável</span><input name="responsavel" autocomplete="off"></label>
        </fieldset>
        <fieldset class="step" data-step="1">
          <legend>Seu perfil</legend>
          <div class="field"><span>Quero ser</span><div class="chips">
            <label><input type="checkbox" name="interesse" value="Modelo ou manequim"><span>Modelo ou manequim</span></label>
            <label><input type="checkbox" name="interesse" value="Ator ou atriz"><span>Ator ou atriz</span></label>
            <label><input type="checkbox" name="interesse" value="Recepcionista de eventos"><span>Recepcionista</span></label>
            <label><input type="checkbox" name="interesse" value="Influenciador"><span>Influenciador</span></label>
            <label><input type="checkbox" name="interesse" value="Cantor ou dançarino"><span>Cantor ou dançarino</span></label>
            <label><input type="checkbox" name="interesse" value="Sósia"><span>Sósia</span></label>
          </div></div>
          <label class="field"><span>Formação de interesse</span><select name="curso">
            <option>Ainda não sei</option>{''.join(f'<option value="{c["slug"]}">{c["nome_txt"]}</option>' for c in CURSOS)}
          </select></label>
          <div class="field"><span>Categoria de avaliação e premiação</span><div class="chips">
            {''.join(f'<label><input type="checkbox" name="categoria" value="{n}"><span>{n} <small>({t})</small></span></label>' for n, t in CATEGORIAS)}
          </div></div>
          <div class="row2">
            <label class="field"><span>Altura (cm)</span><input name="altura" type="number" inputmode="numeric" min="40" max="230" placeholder="Ex.: 172"></label>
            <label class="field"><span>Instagram ou TikTok</span><input name="redes" placeholder="@seuperfil" autocapitalize="off"></label>
          </div>
        </fieldset>
        <fieldset class="step" data-step="2">
          <legend>Como você conheceu a Anne?</legend>
          <div class="chips">
            <label><input type="radio" name="origem" value="Entrevista na TV" required><span>Entrevista na TV</span></label>
            <label><input type="radio" name="origem" value="Instagram"><span>Instagram</span></label>
            <label><input type="radio" name="origem" value="YouTube"><span>YouTube</span></label>
            <label><input type="radio" name="origem" value="Indicação"><span>Indicação</span></label>
            <label><input type="radio" name="origem" value="Outro"><span>Outro</span></label>
          </div>
          <p class="note">Ao enviar, o WhatsApp abre com seus dados preenchidos. Depois é só mandar as 4 fotos na mesma conversa.</p>
        </fieldset>
        <div class="form-actions">
          <button type="button" class="btn btn-ghost" id="btnVoltar" hidden>Voltar</button>
          <button type="button" class="btn btn-solid" id="btnSeguir">Continuar</button>
          <button type="submit" class="btn btn-solid" id="btnEnviar">Enviar pelo WhatsApp</button>
        </div>
        <p class="note">Prefere outro caminho? Use o <a href="{CONFIG['form_cadastro']}" target="_blank" rel="noopener">formulário do Google</a>.</p>
      </form>
    </div>
  </div>
</section>"""


# ---------------------------------------------------------------- páginas

PILARES = [
    ("servicos/#formacao", "Formação", "Formação profissional", "As três formações da agência e o acesso à área do aluno."),
    ("castings/", "Casting", "Banco de talentos", "Modelos, atores, dançarinos e cantores para contratantes."),
    ("servicos/#working", "Working", "Trabalhos divulgados", "Oportunidades de trabalho para modelos e agenciados."),
    ("trade-sales/", "Trade Sales", "Loja virtual", "Produtos e convites."),
]


def pilares():
    return '<ul class="proj-links cols4">' + "".join(
        f'<li class="reveal"><a href="{{P}}{h}"><small>{s}</small><b>{t}</b><span>{d}</span></a></li>' for h, s, t, d in PILARES) + "</ul>"


def home():
    return f"""
<section class="hero" aria-label="Apresentação">
  <img src="img/hero.jpg" alt="Modelo e modelo masculino em retrato preto e branco" fetchpriority="high">
  <div class="wrap">
    <h1>ANNE MODELS</h1>
    <p class="sub">Management</p>
    <p class="sub sub2"><span>National</span><span>International</span></p>
    <p class="intro">Formação profissional técnica artística.<br>Projeções de profissionais artistas nacionais e internacionais.</p>
    <div class="ctas"><a class="btn btn-solid" href="#cadastro">Cadastre-se grátis</a></div>
  </div>
</section>

<section class="facts" aria-label="A agência em números">
  <div class="wrap">
    <div><b>33 anos</b><span>De experiência</span></div>
    <div><b>6 meses a 80 anos</b><span>Perfis agenciados</span></div>
    <div><b>SP e capitais</b><span>Eventos</span></div>
  </div>
</section>

<section class="sec-tight sec-white" id="servicos">
  <div class="wrap">
    <div class="sec-head reveal"><div><h2>Serviços e <em>projetos</em></h2></div></div>
    {pilares()}
  </div>
</section>

<section class="trade">
  <div class="wrap">
    <div class="trade-top reveal">
      <div>
        <p class="eyebrow">Evento</p>
        <h2>Fashion <em>Trade</em></h2>
        <p class="lead">Um fim de semana de imersão: books, composites, vídeos, treino de passarela e um desfile final com as categorias de avaliação e premiação, troféus e atrações artísticas.</p>
      </div>
      <aside><b>Próxima edição</b><span>Data e local a anunciar.</span></aside>
    </div>
    <div class="triptych reveal">
      <figure><img src="img/trade-passarela.jpg" alt="Desfile com look prateado" loading="lazy"></figure>
      <figure><img src="img/trade-salao.jpg" alt="Desfile em salão clássico com plateia" loading="lazy"></figure>
      <figure><img src="img/trade-dourado.jpg" alt="Modelo com vestido dourado na passarela" loading="lazy"></figure>
    </div>
  </div>
</section>

{FORM_CADASTRO}
"""


def agencia():
    return cabeca("A agência", "Anne Models <em>Management</em>",
                  "Agência de modelos, manequins e atores fundada em 1995. Formação, agenciamento e eventos de moda em São Paulo e outras capitais.") + """
<section class="sec-tight">
  <div class="wrap founder-grid">
    <figure class="founder-photo reveal"><img src="{P}img/anne-fundadora.jpg" alt="Retrato de Anne Mac Pherson, fundadora e CEO da Anne Models" loading="lazy" width="360" height="480"></figure>
    <div class="reveal">
      <p class="eyebrow">Fundadora e CEO</p>
      <h2>Anne Mac <em>Pherson</em></h2>
      <p class="lead">33 anos de experiência na moda. Fundou a agência em 1995 e atende perfis de 6 meses a 80 anos.</p>
      <p>É a criadora do Método Anne Mac Pherson. Como colunista social, faz a cobertura de eventos no canal Lifestyle with Anne Mac Pherson.</p>
      <div class="roles"><span>Agenciadora</span><span>Produtora de eventos de moda</span><span>Ministrante de cursos</span><span>Fotógrafa</span><span>Apresentadora</span><span>Palestrante</span><span>Personal stylist</span></div>
    </div>
  </div>
</section>

<section class="sec-tight sec-white" id="staff">
  <div class="wrap">
    <div class="sec-head reveal"><div><p class="eyebrow">Staff</p><h2>Nossa <em>equipe</em></h2></div></div>
    <div class="duo">
      <article class="bloco reveal">
        <p class="eyebrow">Jornalismo e mídia</p><h3 class="h3">Vadú Braga</h3>
        <p>Jornalista à frente dos portais TV Notícias e Edição Fofoca dos Famosos e Celebridades, e da revista Fashion Modus.</p>
        <a class="btn btn-ghost btn-dark" href="https://www.instagram.com/tvnoticiasvadubraga?utm_source=qr&amp;mdxt=MXZibDc5bmYybmdiYg%3D%3D" target="_blank" rel="noopener">TV Notícias - Vadú Braga</a>
      </article>
    </div>
  </div>
</section>

<section class="sec-tight">
  <div class="wrap faq">
    <h2 class="h3 reveal">Dúvidas sobre a <em>carreira</em></h2>
    <div class="reveal">
      <details><summary>Como entro para a carreira de modelo ou manequim?</summary><p>Você passa por avaliação de medidas, teste fotogênico, de passarela e de vídeo comercial. Aprovada, faz a formação profissional, recebe o CCT e é convidada a se agenciar para ser apresentada aos contratantes.</p></details>
      <details><summary>O que é o DRT e como consigo?</summary><p>No caso de modelos e manequins, o nome correto é RPMT, o registro profissional emitido pelo Ministério do Trabalho. Você leva o CCT do curso com RG, CPF, comprovante de residência e os demais documentos pedidos.</p></details>
      <details><summary>Tem limite de idade?</summary><p>Não. Agenciamos de 6 meses a 80 anos, de qualquer etnia. A partir de 16 anos é exigido o RPMT; abaixo disso, é preciso autorização do responsável legal.</p></details>
      <details><summary>Por que estar em uma agência?</summary><p>A agência cuida do contrato assinado, do piso salarial e do apoio jurídico junto ao SATED, e apresenta seu perfil às agências de publicidade, produtores e diretores.</p></details>
    </div>
  </div>
</section>"""


def castings():
    return cabeca("Para contratantes e publicitários", "<em>Castings</em>",
                  "A Anne Models faz a ponte entre o talento e o contratante, com contrato e segurança jurídica em cada trabalho. Marque os perfis que procura e envie o pedido pelo WhatsApp.") + """
<section class="cast" id="contratantes">
  <div class="wrap">
    <div class="cast-grid">
      <article class="cast-card reveal"><img src="{P}img/cast-modelo.jpg" alt="Modelo sentada em cadeira, vestido preto" loading="lazy"><div class="cap"><h3>Modelos e manequins</h3><p>Perfis comerciais e de passarela.</p><button class="pick" type="button" data-pick="Modelos e manequins" aria-pressed="false">Selecionar</button></div></article>
      <article class="cast-card reveal"><img src="{P}img/cast-ator.jpg" alt="Artista em cena no palco" loading="lazy"><div class="cap"><h3>Atores e atrizes</h3><p>TV, cinema e publicidade.</p><button class="pick" type="button" data-pick="Atores e atrizes" aria-pressed="false">Selecionar</button></div></article>
      <article class="cast-card reveal"><img src="{P}img/cast-danca.jpg" alt="Dançarino em movimento no estúdio" loading="lazy"><div class="cap"><h3>Dançarinos</h3><p>Coreógrafos e intérpretes.</p><button class="pick" type="button" data-pick="Dançarinos" aria-pressed="false">Selecionar</button></div></article>
      <article class="cast-card text reveal"><svg aria-hidden="true"><use href="#logo-a"/></svg><h3>Cantores e bandas</h3><p>Artistas de vários estilos, adultos e infantis.</p><button class="pick" type="button" data-pick="Cantores e bandas" aria-pressed="false">Selecionar</button></article>
    </div>
    <div class="ctas reveal">
      <a class="btn btn-solid" id="ctaTalentos" href="WA_TALENTOS" target="_blank" rel="noopener">Solicitar talentos</a>
    </div>
  </div>
</section>""".replace("WA_TALENTOS", wa("Olá! Gostaria de solicitar talentos da Anne Models."))


EXTRA_TALENTOS = '<div class="selbar" id="selbar" hidden role="status" aria-live="polite"><p><b id="selCount">0</b> na seleção: <span id="selList"></span></p><a class="btn" id="selSend" href="#" target="_blank" rel="noopener">Pedir orçamento</a></div>'


def cursos_idx():
    return cabeca("Cursos", "Escolha o seu <em>curso</em>",
                  "Três formações com a fundadora Anne Mac Pherson. Compare e escolha a que combina com o seu objetivo.") + f"""
<section class="sec-tight"><div class="wrap">
  {lista_cursos()}
  <div class="tabela reveal" role="region" aria-label="Comparação dos cursos" tabindex="0">
    <table>
      <thead><tr><th scope="col">Curso</th><th scope="col">Para quem</th><th scope="col">Você sai com</th></tr></thead>
      <tbody>{''.join(f'<tr><th scope="row"><a href="{c["slug"]}/">{c["nome_txt"]}</a></th><td>{c["publico"]}</td><td>{c["inclui"][-1]}</td></tr>' for c in CURSOS)}</tbody>
    </table>
  </div>
  <p class="note center">Já é aluno? Acesse a <a href="../area-do-aluno/">área do aluno</a>.</p>
</div></section>"""


def curso(c):
    msg = f"Olá! Quero me inscrever no curso {c['nome_txt']} da Anne Models."
    acoes = ext(wa(msg), "Quero me inscrever") + f'<a class="btn btn-ghost btn-dark" href="../../?curso={c["slug"]}#cadastro">Cadastro gratuito</a>'
    if c["modulos"]:
        itens = []
        for i, (nome, topicos) in enumerate(c["modulos"], 1):
            if topicos:
                lis = "".join(f"<li>{t}</li>" for t in topicos)
                itens.append(f'<details><summary><span class="mod-n">Módulo {i}</span>{nome}</summary><ul>{lis}</ul></details>')
            else:
                itens.append(f'<div class="mod-item"><span class="mod-n">Módulo {i}</span>{nome}</div>')
        modulos = f'<div class="modulos reveal"><h2 class="h3">Programa</h2>{"".join(itens)}</div>'
    else:
        modulos = '<div class="modulos reveal"><h2 class="h3">Programa</h2><p>O programa completo é enviado na inscrição. Fale com a agência para receber.</p></div>'
    inclui = "".join(f"<li>{x}</li>" for x in c["inclui"])
    return cabeca(c["tag"], c["nome"], c["resumo"], acoes) + f"""
<section class="sec-tight"><div class="wrap curso-grid">
  <div class="curso-info reveal">
    <h2 class="h3">Para quem é</h2><p>{c['publico']}</p>
    <h2 class="h3">Objetivo</h2><p>{c['objetivo']}</p>
    <h2 class="h3">O que inclui</h2><ul class="check">{inclui}</ul>
    <p class="note">Datas, formato, carga horária e valores são informados na inscrição.</p>
  </div>
  {modulos}
</div></section>
{milao_modulo() if c.get("milao") else ""}
<section class="cta-band"><div class="wrap">
  <h2>Pronto para começar?</h2>
  <div class="ctas">{ext(wa(msg), "Falar sobre a inscrição")}<a class="btn btn-ghost" href="../">Ver os outros cursos</a></div>
</div></section>"""


def servicos():
    data = json.dumps(SERVICOS, ensure_ascii=False)
    filtros = '<button type="button" data-f="todos" aria-pressed="true">Todos</button>' + "".join(
        f'<button type="button" data-f="{v[0]}" aria-pressed="false">{k}</button>' for k, v in GRUPOS.items())
    return cabeca("Serviços", "Serviços e <em>projetos</em>",
                  "Formação profissional, casting, trabalhos e loja virtual da Anne Models.") + f"""
<section class="sec-tight sec-white"><div class="wrap">{pilares()}</div></section>
<section class="sec-tight" id="formacao"><div class="wrap">
  <div class="sec-head reveal"><div><p class="eyebrow">Formação profissional</p><h2>Três <em>formações</em></h2></div></div>
  {lista_cursos()}
  <div class="ctas center"><a class="btn btn-ghost btn-dark" href="../area-do-aluno/">Área do aluno</a></div>
</div></section>
<section class="sec-tight sec-white" id="working"><div class="wrap">
  <div class="sec-head reveal"><div><p class="eyebrow">Working</p><h2>Trabalhos <em>divulgados</em></h2></div>
    <p class="lead">Os trabalhos abertos para modelos e agenciados serão publicados aqui.</p></div>
  <div class="ctas">{ext(wa("Olá! Sou modelo/agenciado(a) e quero receber os trabalhos divulgados pela Anne Models."), "Quero receber os trabalhos", "btn btn-ghost btn-dark")}</div>
</div></section>
<section class="catalogo sec-tight" id="catalogo"><div class="wrap">
  <div class="sec-head reveal"><div><p class="eyebrow">Catálogo do WhatsApp Business</p><h2>Catálogo de <em>serviços</em></h2></div>
    <p class="lead">Toque em um serviço para ver o que está incluído e falar com a agência.</p></div>
  <div class="cat-filtros" role="group" aria-label="Filtrar serviços">{filtros}</div>
  {cards_servicos()}
</div></section>
<section class="sec-tight sec-white" id="documentos"><div class="wrap">
  <div class="sec-head reveal"><div><p class="eyebrow">Contratação</p><h2>Documentos de <em>contratação</em></h2></div>
    <p class="lead">Os documentos de contratação serão publicados aqui. Enquanto isso, peça pelo WhatsApp.</p></div>
  <div class="ctas">{ext(wa("Olá! Gostaria de receber os documentos de contratação da Anne Models."), "Pedir os documentos", "btn btn-ghost btn-dark")}</div>
</div></section>
<script type="application/json" id="catData" data-base="../" data-wa="{CONFIG['wa_catalogo']}">{data}</script>"""


EXTRA_SERVICOS = f"""<dialog class="cat-dlg" id="catDlg" aria-labelledby="catDlgTitle">
  <button class="cat-close" type="button" aria-label="Fechar"></button>
  <div class="cat-dlg-in">
    <div class="cat-media"><div class="cv cv-dark cat-big" id="catBig"></div></div>
    <div class="cat-txt"><p class="cat-tag" id="catDlgTag"></p><h3 id="catDlgTitle"></h3><p class="cat-price" id="catDlgPrice"></p><ul id="catDlgList"></ul><a class="btn btn-solid" id="catDlgCta" href="#" target="_blank" rel="noopener">Quero este serviço</a><p class="note">Atendimento pelo WhatsApp (31) 99658-9729. <a id="catDlgArt" href="#" target="_blank" rel="noopener">Ver a arte original</a></p></div>
  </div>
</dialog>"""


def fashion_trade():
    prog = [
        ("Sexta", "18h às 22h", "Abertura", "Entrega das camisetas da agência, coquetel de integração, palestra e abertura oficial."),
        ("Sábado", "8h às 14h", "Material profissional", "Books, composites e vídeos de comerciais de TV."),
        ("Sábado", "15h às 21h", "Treinamento", "Passarela e coreografias."),
        ("Domingo", "Manhã", "Produção", "Cabelo, maquiagem e camarim."),
        ("Domingo", "A partir das 14h", "O desfile", "Desfiles, categorias de avaliação e premiação, troféus e leilão de looks."),
    ]
    linhas = "".join(f'<li><span class="dia">{d}<small>{h}</small></span><div><b>{t}</b><p>{x}</p></div></li>' for d, h, t, x in prog)
    modos = [
        ("Modelos e participantes", "Desfile, book, composite, vídeo e certificado.", "Quero participar do Fashion Trade como modelo."),
        ("Atrações artísticas", "Cantores, dançarinos e performances nos intervalos.", "Quero me inscrever como atração artística no Fashion Trade."),
        ("Imprensa", "Jornalistas, influenciadores e youtubers para cobertura e transmissão ao vivo.", "Quero fazer o credenciamento de imprensa no Fashion Trade."),
        ("Patrocinadores", "Cotas Master, Ouro, Prata e Bronze.", "Quero patrocinar o Fashion Trade. Gostaria de conhecer as cotas."),
        ("Apoiadores", "Prestadores de serviço em troca de divulgação.", "Quero apoiar o Fashion Trade como prestador de serviço."),
        ("Convidados especiais", "Autoridades e celebridades convidadas.", "Gostaria de falar sobre convite especial para o Fashion Trade."),
        ("Convites para o público", "Convites limitados para assistir aos desfiles.", "Quero ser avisado(a) quando abrir a venda de convites do Fashion Trade."),
    ]
    cards = "".join(f'<li><h3>{t}</h3><p>{d}</p>{ext(wa("Olá! " + m), "Quero este", "btn btn-ghost")}</li>' for t, d, m in modos)
    atracoes = ["Desfile Luxo no Lixo, com looks de materiais reciclados", "Desfile oficial da agência, com jeans e escarpim",
                "Categorias de avaliação e premiação: ABC do Amanhã, Top Model of the Year, Sósias do Brasil e Mulher Total 40+",
                "Troféus para os alunos que mais se destacaram", "Leilão de looks ao vivo no palco",
                "Espaço para cantores, dançarinos e artistas nos intervalos"]
    return f"""<section class="trade page-dark">
  <div class="wrap">
    <div class="trade-top">
      <div><p class="eyebrow">Evento anual</p><h1>Fashion <em>Trade</em></h1>
        <p class="lead">Um fim de semana completo de formação e desfile, de sexta a domingo. Edições previstas em Belo Horizonte, São Paulo, Rio de Janeiro, Pernambuco e Salvador.</p></div>
      <aside><b>Próxima edição</b><span>Data e local a anunciar.</span></aside>
    </div>
    <div class="triptych">
      <figure><img src="../img/trade-passarela.jpg" alt="Desfile com look prateado"></figure>
      <figure><img src="../img/trade-salao.jpg" alt="Desfile em salão clássico com plateia"></figure>
      <figure><img src="../img/trade-dourado.jpg" alt="Modelo com vestido dourado na passarela"></figure>
    </div>
    <h2 class="h3">Programação</h2>
    <ul class="agenda">{linhas}</ul>
  </div>
</section>
<section class="sec-tight"><div class="wrap">
  <div class="sec-head reveal"><div><p class="eyebrow">No palco</p><h2>Destaques do <em>evento</em></h2></div></div>
  <ul class="check cols2 reveal">{''.join(f'<li>{a}</li>' for a in atracoes)}</ul>
</div></section>
<section class="sec-tight sec-white" id="participar"><div class="wrap">
  <div class="sec-head reveal"><div><p class="eyebrow">Participe</p><h2>Escolha como <em>participar</em></h2></div>
    <p class="lead">Cada opção abre uma conversa no WhatsApp com a mensagem certa para a equipe.</p></div>
  <ul class="modos">{cards}</ul>
</div></section>"""


def trade_sales():
    cats = [
        ("Calçados", "Escarpim para desfiles e books."),
        ("Alfaiataria", "Terninho feminino e masculino e chemise."),
        ("Básicos para book", "T-shirts branca e preta e calça jeans tradicional."),
        ("Moda praia", "Biquíni, maiô e sunga."),
        ("Infantil", "Moda infantil para os books das crianças."),
        ("Maquiagem", "Maletas e acessórios de maquiagem."),
    ]
    itens = "".join(f'<li class="reveal"><h3>{t}</h3><p>{d}</p></li>' for t, d in cats)
    return cabeca("Loja virtual", "Trade <em>Sales</em>",
                  "Loja virtual da agência: produtos para o book, os desfiles e o dia a dia de trabalho, e convites para os eventos. A loja está em preparação; enquanto isso, peça pelo WhatsApp.",
                  ext(wa("Olá! Quero indicações de compra da Trade Sales."), "Pedir pelo WhatsApp")) + f"""
<section class="sec-tight"><div class="wrap">
  <ul class="cats">{itens}</ul>
  <p class="note center">Os links dos fornecedores serão publicados aqui. Enquanto isso, peça a lista pelo WhatsApp.</p>
</div></section>"""


def area_aluno():
    return cabeca("Área do aluno", "Área do <em>aluno</em>",
                  "Aqui os alunos matriculados vão assistir às aulas, baixar as apostilas, enviar as tarefas e receber os certificados. O acesso está sendo preparado.",
                  ext(wa("Olá! Sou aluno(a) e preciso de ajuda com o acesso às aulas."), "Sou aluno e preciso de ajuda") + '<a class="btn btn-ghost btn-dark" href="../cursos/">Conhecer os cursos</a>') + """
<section class="sec-tight"><div class="wrap">
  <ul class="cats">
    <li class="reveal"><h3>Aulas</h3><p>Vídeos de cada módulo, liberados conforme a matrícula.</p></li>
    <li class="reveal"><h3>Apostilas</h3><p>Material em PDF para estudar.</p></li>
    <li class="reveal"><h3>Tarefas</h3><p>Envio dos trabalhos de cada módulo.</p></li>
    <li class="reveal"><h3>Certificado</h3><p>Emitido ao concluir o curso.</p></li>
  </ul>
</div></section>"""


def contato():
    end = "Av. Governador Valadares, 443, Centro, Alpinópolis/MG"
    return cabeca("Contatos", "Fale com a <em>agência</em>",
                  "Endereço, WhatsApp, e-mails e redes sociais da Anne Models Management.") + f"""
<section class="sec-tight"><div class="wrap">
  <div class="channels reveal">
    <a href="https://wa.me/{CONFIG['wa_agencia']}" target="_blank" rel="noopener"><small>WhatsApp</small><span>(31) 97302-3077</span></a>
    <a href="https://wa.me/{CONFIG['wa_catalogo']}" target="_blank" rel="noopener"><small>WhatsApp do catálogo</small><span>(31) 99658-9729</span></a>
    <a href="mailto:{CONFIG['email_ceo']}"><small>E-mail da CEO</small><span>{CONFIG['email_ceo']}</span></a>
    <a href="mailto:{CONFIG['email_cursos']}"><small>E-mail dos cursos</small><span>{CONFIG['email_cursos']}</span></a>
    <a href="mailto:{CONFIG['email_assessoria']}"><small>E-mail da assessoria</small><span>{CONFIG['email_assessoria']}</span></a>
    <a href="{CONFIG['youtube_lifestyle']}" target="_blank" rel="noopener"><small>YouTube</small><span>Lifestyle with Anne Mac Pherson</span></a>
    <a href="{CONFIG['youtube_eventos']}" target="_blank" rel="noopener"><small>YouTube</small><span>TV Anny Praddo Eventos</span></a>
    <a href="{CONFIG['instagram']}" target="_blank" rel="noopener"><small>Instagram</small><span>@anny_praddo_modeling_career</span></a>
  </div>
</div></section>
<section class="sec-tight sec-white"><div class="wrap duo">
  <div class="reveal">
    <h2 class="h3">Endereço</h2>
    <p>{end}</p>
    <iframe class="mapa" title="Mapa: {end}" src="https://www.google.com/maps?q={quote(end)}&amp;output=embed" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>
  </div>
  <form class="form reveal" id="formMsg">
    <h2 class="h3">Envie sua mensagem</h2>
    <label class="field"><span>Nome ou apelido artístico</span><input name="nome" autocomplete="name" required></label>
    <div class="row2">
      <label class="field"><span>Idade</span><input name="idade" type="number" inputmode="numeric" min="0" max="120" required></label>
      <label class="field"><span>Cidade e estado</span><input name="cidade" autocomplete="address-level2" required></label>
    </div>
    <div class="row2">
      <label class="field"><span>E-mail</span><input name="email" type="email" autocomplete="email" required></label>
      <label class="field"><span>WhatsApp</span><input name="whats" type="tel" inputmode="tel" autocomplete="tel" required></label>
    </div>
    <label class="field"><span>O que mais gostou no nosso site?</span><textarea name="gostou" rows="3" required></textarea></label>
    <label class="field"><span>Despertou interesse em algum de nossos serviços ou produtos?</span><textarea name="interesse" rows="3" required></textarea></label>
    <div class="form-actions"><button type="submit" class="btn btn-solid">Enviar pelo WhatsApp</button></div>
    <p class="note">Ao enviar, o WhatsApp abre com a sua mensagem preenchida.</p>
  </form>
</div></section>"""


def milao_modulo():
    itens = ["Viagem organizada", "Convites em até 3 agências de modelos", "Visita a um Salão de Retiro e a uma boutique ou desfile de grife",
             "Participação em até 3 eventos de moda em Milão", "Visitas a desfiles de moda", "Acesso a eventos culturais gratuitos ou de baixo custo",
             "Aulas de italiano na prática", "Networking com profissionais do mercado"]
    return f"""<section class="sec-tight sec-white" id="milao"><div class="wrap curso-grid">
  <figure class="milao-foto reveal"><img src="../../img/milao-2027.jpg" alt="Anne Mac Pherson diante da Catedral de Milão, em cartaz da Imersão e Intercâmbio de Modelos 2027" loading="lazy"></figure>
  <div class="curso-info reveal">
    <p class="eyebrow">Módulo Expansão profissional</p>
    <h2 class="h3">Imersão em Milão</h2>
    <p>Parte do curso de Integração Profissional: um fim de semana de moda, cultura, networking e desenvolvimento profissional na Itália, com coordenação de Anne Mac Pherson.</p>
    <ul class="fatos"><li><b>Outubro de 2027</b><span>Milão, Itália</span></li><li><b>15 vagas</b><span>Feminino e masculino</span></li><li><b>A partir de 21 anos</b><span>Idade mínima</span></li><li><b>30/01/2027</b><span>Prazo para inscrição e pagamento</span></li></ul>
    <h3 class="h3">O que está previsto</h3>
    <ul class="check">{''.join(f'<li>{i}</li>' for i in itens)}</ul>
    <p class="note">Programa preliminar: datas, custos, reservas, convites e visitas estão sujeitos a confirmação.</p>
  </div>
</div></section>"""


def nao_encontrada():
    return cabeca("Erro 404", "Página não <em>encontrada</em>",
                  "O endereço pode ter mudado. Volte para a página inicial ou fale com a agência.",
                  '<a class="btn btn-solid" href="/anne-models/">Página inicial</a>')


# ---------------------------------------------------------------- saída

PAGINAS = [
    ("", "Início", "Agência de modelos, manequins e atores há 33 anos. Formação profissional, castings, serviços e o Fashion Trade.", home, True, ""),
    ("a-agencia/", "A agência", "História da Anne Models Management e da fundadora Anne Mac Pherson.", agencia, False, ""),
    ("castings/", "Castings", "Modelos, atores, dançarinos e cantores para contratantes e publicitários.", castings, False, EXTRA_TALENTOS),
    ("cursos/", "Cursos", "Método Anne Mac Pherson, Integração Profissional e Recepcionistas de eventos.", cursos_idx, False, ""),
    ("servicos/", "Serviços", "Formação profissional, casting, trabalhos, loja virtual e catálogo de serviços da Anne Models.", servicos, False, EXTRA_SERVICOS),
    ("fashion-trade/", "Fashion Trade", "Programação e formas de participar do Fashion Trade, evento anual da Anne Models.", fashion_trade, True, ""),
    ("trade-sales/", "Trade Sales", "Curadoria de produtos para book, desfiles e trabalho de modelos e artistas.", trade_sales, False, ""),
    ("area-do-aluno/", "Área do aluno", "Acesso às aulas, apostilas, tarefas e certificados dos cursos da Anne Models.", area_aluno, False, ""),
    ("contato/", "Contato", "WhatsApp, e-mails e redes da Anne Models Management.", contato, False, ""),
]
for c in CURSOS:
    PAGINAS.append((f"cursos/{c['slug']}/", c["nome_txt"], c["resumo"], lambda c=c: curso(c), False, ""))


def main():
    for rota, titulo, desc, fn, hero, extra in PAGINAS:
        destino = RAIZ / rota / "index.html"
        destino.parent.mkdir(parents=True, exist_ok=True)
        destino.write_text(layout(rota, titulo, desc, fn(), hero=hero, extra=extra), encoding="utf-8", newline="\n")
    (RAIZ / "404.html").write_text(
        layout("404/", "Página não encontrada", "Página não encontrada.", nao_encontrada()).replace('"../', '"/anne-models/'),
        encoding="utf-8", newline="\n")
    urls = "".join(f"<url><loc>{CONFIG['site_url']}{r}</loc></url>" for r, *_ in PAGINAS)
    (RAIZ / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n', encoding="utf-8")
    print(len(PAGINAS), "páginas geradas")


if __name__ == "__main__":
    main()
