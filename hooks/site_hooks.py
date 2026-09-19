"""Build hooks voor 2 Minuten IT-Architectuur.

Verzorgt vier dingen, zonder extra afhankelijkheden:

1. metaregel onder de artikeltitel: publicatiedatum, onderwerp en leestijd;
2. de artikellijst op de overzichtspagina's via {{ artikellijst }};
3. lazy loading en async decoding voor afbeeldingen in de artikelen;
4. cache busting: aan extra_css en extra_javascript wordt een content hash
   gehangen, zodat een nieuwe deployment nooit oude CSS bij nieuwe HTML serveert.
"""

import hashlib
import os
import re
from urllib.parse import urlparse

WORDS_PER_MINUTE = 200

MAANDEN = [
    "januari", "februari", "maart", "april", "mei", "juni",
    "juli", "augustus", "september", "oktober", "november", "december",
]
MONTHS = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December",
]
MAAND_KORT = ["jan", "feb", "mrt", "apr", "mei", "jun", "jul", "aug", "sep", "okt", "nov", "dec"]
MONTH_SHORT = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

_ARTICLE = re.compile(r"^1\d\d-")
_FRONTMATTER = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.S)
_TITLE = re.compile(r"^#\s+(.+)$", re.M)
_IMG = re.compile(r"<img(?![^>]*\bloading=)")
_LIST = re.compile(r"\{\{\s*artikellijst(?::(nl|en))?(?::(\d+))?\s*\}\}")
_CARDS = re.compile(r"\{\{\s*artikelraster(?::(nl|en))?(?::(\d+))?(?::(\d+))?\s*\}\}")
_FEATURED = re.compile(r"\{\{\s*uitgelicht(?::(nl|en))?\s*\}\}")
_DOMAINS = re.compile(r"\{\{\s*domeinen(?::(nl|en))?\s*\}\}")
_BYDOMAIN = re.compile(r"\{\{\s*perdomein(?::(nl|en))?\s*\}\}")


def _lang(page):
    src = page.file.src_uri
    return "en" if src.startswith("en/") else "nl"


def _parse_date(value):
    value = str(value).strip()
    m = re.match(r"(\d{4})-(\d{1,2})-(\d{1,2})", value)
    if not m:
        return None
    return tuple(int(g) for g in m.groups())


def _format_date(value, lang, short=False):
    parts = _parse_date(value)
    if not parts:
        return str(value)
    year, month, day = parts
    if short:
        names = MONTH_SHORT if lang == "en" else MAAND_KORT
        return "%s %d" % (names[month - 1], year)
    names = MONTHS if lang == "en" else MAANDEN
    if lang == "en":
        return "%s %d, %d" % (names[month - 1], day, year)
    return "%d %s %d" % (day, names[month - 1], year)


def _reading_time(markdown, lang):
    text = re.sub(r"```.*?```", " ", markdown, flags=re.S)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)
    minutes = max(1, int(round(len(text.split()) / float(WORDS_PER_MINUTE))))
    unit = "min read" if lang == "en" else "min lezen"
    return "%d %s" % (minutes, unit)


def _read_article(path):
    with open(path, encoding="utf-8") as handle:
        raw = handle.read()
    meta = {}
    match = _FRONTMATTER.match(raw)
    body = raw
    if match:
        body = raw[match.end():]
        for line in match.group(1).split("\n"):
            if ":" in line:
                key, _, value = line.partition(":")
                meta[key.strip()] = value.strip().strip('"')
    title = _TITLE.search(body)
    meta["title"] = title.group(1).strip() if title else os.path.basename(path)
    meta["body"] = body
    return meta


def _articles(docs_dir, lang, limit=None, prefix=""):
    directory = os.path.join(docs_dir, lang)
    articles = []
    for name in os.listdir(directory):
        if not name.endswith(".md") or not _ARTICLE.match(name):
            continue
        meta = _read_article(os.path.join(directory, name))
        meta["href"] = prefix + name[:-3] + "/"
        articles.append(meta)
    articles.sort(key=lambda a: _parse_date(a.get("date", "")) or (0, 0, 0), reverse=True)
    if limit:
        articles = articles[:limit]
    return articles


def _post_list(docs_dir, lang, limit=None, prefix=""):
    """Verticale lijst: links de datum, rechts titel, samenvatting en meta."""
    out = ['<ol class="post-list">']
    for article in _articles(docs_dir, lang, limit, prefix):
        date = article.get("date", "")
        out.append('<li class="post">')
        out.append(
            '<div class="post__date"><time datetime="%s">%s</time></div>'
            % (date, _format_date(date, lang, short=True))
        )
        out.append('<div class="post__body">')
        out.append(
            '<h3 class="post__title"><a href="%s">%s</a></h3>'
            % (article["href"], article["title"])
        )
        if article.get("description"):
            out.append('<p class="post__text">%s</p>' % article["description"])
        meta = []
        if article.get("topic"):
            meta.append('<span class="post__topic">%s</span>' % article["topic"])
        meta.append("<span>%s</span>" % _reading_time(article["body"], lang))
        out.append('<p class="post__meta">%s</p>' % "".join(meta))
        out.append("</div>")
        out.append("</li>")
    out.append("</ol>")
    return "\n".join(out)


def _slug(text):
    """Zelfde ankers als de toc-extensie maakt, zodat verwijzingen kloppen."""
    text = text.lower().replace("&", " ")
    text = re.sub(r"[^a-z0-9\s-]", "", text)
    return re.sub(r"\s+", "-", text.strip())


DOMAIN_ORDER = [
    "Rol van de architect",
    "Strategie en organisatie",
    "Samenwerking met de business",
    "Applicaties en services",
    "Integratie en patterns",
    "Werkwijzen en besluitvorming",
    "Technologie en A.I.",
]
DOMAIN_ORDER_EN = [
    "The architect's role",
    "Strategy and organisation",
    "Working with the business",
    "Applications and services",
    "Integration and patterns",
    "Practices and decisions",
    "Technology and A.I.",
]

# Korte omschrijving per domein, in beide talen.
DOMAIN_TEXT = {
    "Rol van de architect": "Wat het vak inhoudt, welke vaardigheden tellen en waar de architect het verschil maakt.",
    "Strategie en organisatie": "Wendbaarheid, transformatie en de beperkingen die de doorstroom van werk bepalen.",
    "Samenwerking met de business": "Het gesprek tussen IT en de rest van de organisatie, en wat daar misgaat.",
    "Applicaties en services": "Servicetypen, verantwoordelijkheden en het beheer van API's.",
    "Integratie en patterns": "Beproefde oplossingen voor terugkerende integratievraagstukken.",
    "Werkwijzen en besluitvorming": "Besluiten nemen en vastleggen, en vaker en kleiner opleveren.",
    "Technologie en A.I.": "Wat nieuwe technologie werkelijk verandert aan ons werk, en wat niet.",
    "The architect's role": "What the craft involves, which skills count and where the architect makes the difference.",
    "Strategy and organisation": "Agility, transformation and the constraints that govern the flow of work.",
    "Working with the business": "The conversation between IT and the rest of the organisation, and where it breaks down.",
    "Applications and services": "Service types, responsibilities and the management of APIs.",
    "Integration and patterns": "Proven solutions for recurring integration problems.",
    "Practices and decisions": "Making and recording decisions, and delivering smaller and more often.",
    "Technology and A.I.": "What new technology really changes about our work, and what it does not.",
}

# Rustige lijniconen: eenvoudige geometrie, geen illustraties.
DOMAIN_ICON = {
    0: '<path d="M12 3 3 8l9 5 9-5-9-5Z"/><path d="M3 14l9 5 9-5"/>',
    1: '<rect x="3" y="4" width="7" height="7" rx="1"/><rect x="14" y="4" width="7" height="7" rx="1"/><rect x="8.5" y="14" width="7" height="7" rx="1"/><path d="M6.5 11v3h11v-3"/>',
    2: '<circle cx="8" cy="8" r="3.2"/><circle cx="16" cy="16" r="3.2"/><path d="M10.5 10.5 13.5 13.5"/>',
    3: '<rect x="3" y="4" width="18" height="6" rx="1"/><rect x="3" y="14" width="18" height="6" rx="1"/><path d="M8 10v4M16 10v4"/>',
    4: '<circle cx="5" cy="12" r="2"/><circle cx="19" cy="12" r="2"/><circle cx="12" cy="5" r="2"/><circle cx="12" cy="19" r="2"/><path d="M7 12h10M12 7v10"/>',
    5: '<path d="M5 4h11l3 3v13H5z"/><path d="M8 11h8M8 15h5"/>',
    6: '<rect x="4" y="4" width="16" height="16" rx="2"/><path d="M9 9h6v6H9z"/><path d="M9 2v2M15 2v2M9 20v2M15 20v2M2 9h2M2 15h2M20 9h2M20 15h2"/>',
}


def _domains(docs_dir, lang, prefix="", topics_href="onderwerpen/"):
    """Kaarten per architectuurdomein, met aantal artikelen en een verwijzing."""
    order = DOMAIN_ORDER_EN if lang == "en" else DOMAIN_ORDER
    articles = _articles(docs_dir, lang)
    counts = {}
    for article in articles:
        topic = article.get("topic")
        if topic:
            counts[topic] = counts.get(topic, 0) + 1

    out = ['<ul class="domain-grid">']
    for index, name in enumerate(order):
        count = counts.get(name, 0)
        if not count:
            continue
        if lang == "en":
            word = "article" if count == 1 else "articles"
        else:
            word = "artikel" if count == 1 else "artikelen"
        label = "%d %s" % (count, word)
        out.append('<li class="domain">')
        out.append('<a class="domain__link" href="%s#%s">' % (topics_href, _slug(name)))
        out.append(
            '<svg class="domain__icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            'stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">%s</svg>'
            % DOMAIN_ICON[index]
        )
        out.append('<h3 class="domain__name">%s</h3>' % name)
        out.append('<p class="domain__text">%s</p>' % DOMAIN_TEXT.get(name, ""))
        out.append('<p class="domain__count">%s</p>' % label)
        out.append("</a></li>")
    out.append("</ul>")
    return "\n".join(out)


def _featured(docs_dir, lang, prefix=""):
    """Het nieuwste artikel, met meer visueel gewicht dan de rest.

    Een blokelement, zodat Markdown het niet in een alinea wikkelt. De link
    zit op de titel; de rest van de kaart is klikbaar via CSS.
    """
    articles = _articles(docs_dir, lang, 1, prefix)
    if not articles:
        return ""
    a = articles[0]
    label = "Latest article" if lang == "en" else "Nieuwste artikel"
    more = "Read the article" if lang == "en" else "Lees het artikel"
    meta = []
    if a.get("topic"):
        meta.append('<span class="meta__topic">%s</span>' % a["topic"])
    if a.get("date"):
        meta.append('<time datetime="%s">%s</time>' % (a["date"], _format_date(a["date"], lang)))
    meta.append("<span>%s</span>" % _reading_time(a["body"], lang))
    meta.append('<span class="featured__more">%s &rsaquo;</span>' % more)
    return "\n".join([
        '<article class="featured">',
        '<p class="featured__label">%s</p>' % label,
        '<h3 class="featured__title"><a href="%s">%s</a></h3>' % (a["href"], a["title"]),
        '<p class="featured__text">%s</p>' % a.get("description", ""),
        '<p class="featured__meta">%s</p>' % "".join(meta),
        "</article>",
    ])


def _cards(docs_dir, lang, limit=None, prefix="", skip=0):
    """Artikelraster: drie kolommen op brede schermen, één op telefoons."""
    articles = _articles(docs_dir, lang, None, prefix)[skip:]
    if limit:
        articles = articles[:limit]
    out = ['<ul class="card-grid">']
    for a in articles:
        out.append('<li class="card"><a class="card__link" href="%s">' % a["href"])
        out.append('<h3 class="card__title">%s</h3>' % a["title"])
        out.append('<p class="card__text">%s</p>' % a.get("description", ""))
        meta = []
        if a.get("topic"):
            meta.append('<span class="meta__topic">%s</span>' % a["topic"])
        if a.get("date"):
            meta.append('<time datetime="%s">%s</time>' % (a["date"], _format_date(a["date"], lang, short=True)))
        meta.append("<span>%s</span>" % _reading_time(a["body"], lang))
        out.append('<p class="card__meta">%s</p>' % "".join(meta))
        out.append("</a></li>")
    out.append("</ul>")
    return "\n".join(out)


def _by_domain(docs_dir, lang, prefix=""):
    """Alle artikelen, geordend per domein, voor de onderwerpenpagina."""
    order = DOMAIN_ORDER_EN if lang == "en" else DOMAIN_ORDER
    articles = _articles(docs_dir, lang, None, prefix)
    out = []
    for name in order:
        group = [a for a in articles if a.get("topic") == name]
        if not group:
            continue
        out.append('<h2 id="%s">%s</h2>' % (_slug(name), name))
        out.append('<p class="lead">%s</p>' % DOMAIN_TEXT.get(name, ""))
        out.append('<ol class="post-list">')
        for a in group:
            date = a.get("date", "")
            out.append('<li class="post">')
            out.append(
                '<div class="post__date"><time datetime="%s">%s</time></div>'
                % (date, _format_date(date, lang, short=True))
            )
            out.append('<div class="post__body">')
            out.append('<h3 class="post__title"><a href="%s">%s</a></h3>' % (a["href"], a["title"]))
            if a.get("description"):
                out.append('<p class="post__text">%s</p>' % a["description"])
            out.append('<p class="post__meta"><span>%s</span></p>' % _reading_time(a["body"], lang))
            out.append("</div></li>")
        out.append("</ol>")
    return "\n".join(out)


def _related(docs_dir, lang, page_name, prefix=""):
    """Twee artikelen uit hetzelfde domein, onder aan een artikel."""
    articles = _articles(docs_dir, lang, None, prefix)
    current = next((a for a in articles if a["href"].endswith(page_name + "/")), None)
    if not current or not current.get("topic"):
        return ""
    same = [a for a in articles if a.get("topic") == current["topic"] and a is not current]
    if not same:
        return ""
    title = "Related articles" if lang == "en" else "Meer over dit onderwerp"
    out = ['<nav class="related" aria-label="%s">' % title]
    out.append('<p class="related__title">%s</p>' % title)
    out.append('<ul class="related__list">')
    for a in same[:2]:
        out.append(
            '<li><a href="%s">%s<span class="related__meta">%s</span></a></li>'
            % (a["href"], a["title"], _reading_time(a["body"], lang))
        )
    out.append("</ul></nav>")
    return "\n".join(out)


def on_config(config):
    """Hang een content hash aan de eigen CSS en JavaScript."""
    docs_dir = config["docs_dir"]

    def stamp(items):
        stamped = []
        for item in items:
            path = os.path.join(docs_dir, str(item))
            if "://" not in str(item) and os.path.isfile(path):
                with open(path, "rb") as handle:
                    digest = hashlib.sha256(handle.read()).hexdigest()[:8]
                stamped.append("%s?h=%s" % (item, digest))
            else:
                stamped.append(item)
        return stamped

    config["extra_css"] = stamp(config["extra_css"])
    config["extra_javascript"] = stamp(config["extra_javascript"])
    return config


def on_page_markdown(markdown, page, config, files):
    lang = _lang(page)
    # Eén navigatiemodel: de kopbalk. De zijkolom links blijft overal weg.
    hidden = page.meta.setdefault("hide", [])
    if "navigation" not in hidden:
        hidden.append("navigation")
    # Diepte van de gerenderde URL, niet van het bronbestand: met mappen-URLs
    # is a/b.md immers a/b/ en dus een niveau dieper.
    depth = page.url.count("/")

    def expand_list(match):
        list_lang = match.group(1) or lang
        limit = int(match.group(2)) if match.group(2) else None
        # Verwijzingen zijn relatief, zodat ze vanaf elke pagina kloppen.
        prefix = "../" * depth + list_lang + "/"
        return _post_list(config["docs_dir"], list_lang, limit, prefix)

    markdown = _LIST.sub(expand_list, markdown)

    def prefix_for(other_lang):
        return "../" * depth + other_lang + "/"

    def expand_cards(match):
        card_lang = match.group(1) or lang
        limit = int(match.group(2)) if match.group(2) else None
        skip = int(match.group(3)) if match.group(3) else 0
        return _cards(config["docs_dir"], card_lang, limit, prefix_for(card_lang), skip)

    markdown = _CARDS.sub(expand_cards, markdown)

    def expand_featured(match):
        f_lang = match.group(1) or lang
        return _featured(config["docs_dir"], f_lang, prefix_for(f_lang))

    markdown = _FEATURED.sub(expand_featured, markdown)

    def expand_domains(match):
        d_lang = match.group(1) or lang
        if d_lang == "en":
            topics = "topics/" if depth >= 1 else "en/topics/"
        else:
            topics = "../" * depth + "onderwerpen/"
        return _domains(config["docs_dir"], d_lang, "", topics)

    markdown = _DOMAINS.sub(expand_domains, markdown)

    def expand_bydomain(match):
        b_lang = match.group(1) or lang
        return _by_domain(config["docs_dir"], b_lang, prefix_for(b_lang))

    markdown = _BYDOMAIN.sub(expand_bydomain, markdown)

    if _ARTICLE.match(os.path.basename(page.file.src_uri)):
        bits = []
        if page.meta.get("date"):
            bits.append(
                '<time datetime="%s">%s</time>'
                % (page.meta["date"], _format_date(page.meta["date"], lang))
            )
        if page.meta.get("topic"):
            bits.append('<span class="article-meta__topic">%s</span>' % page.meta["topic"])
        bits.append("<span>%s</span>" % _reading_time(markdown, lang))
        meta_html = '<p class="article-meta">%s</p>' % "".join(bits)
        markdown = _TITLE.sub(lambda m: m.group(0) + "\n\n" + meta_html, markdown, count=1)

        name = os.path.basename(page.file.src_uri)[:-3]
        # Vanaf de artikelpagina wijzen de verwijzingen een map omhoog.
        related = _related(config["docs_dir"], lang, name, "../")
        if related:
            markdown += "\n\n" + related

    return _IMG.sub('<img loading="lazy" decoding="async"', markdown)


# Het thema draait in het Nederlands. Op de Engelse pagina's vertalen we de
# labels die een bezoeker ziet; de artikelinhoud blijft ongemoeid.
UI_EN = [
    ("Ga naar inhoud", "Skip to content"),
    ("Zoeken initialiseren", "Initializing search"),
    ("Inhoudsopgave", "Contents"),
    ("Zoeken", "Search"),
    ("Leegmaken", "Clear"),
    ("Donkere weergave", "Dark mode"),
    ("Lichte weergave", "Light mode"),
    ("Terug naar boven", "Back to top"),
    ("Navigatie", "Navigation"),
    ("Vorige", "Previous"),
    ("Volgende", "Next"),
]


def _translate_ui(output):
    """Vervangt themalabels buiten het artikel, zodat teksten intact blijven."""
    start = output.find("<article")
    end = output.find("</article>")
    if start == -1 or end == -1:
        head, article, tail = output, "", ""
    else:
        end += len("</article>")
        head, article, tail = output[:start], output[start:end], output[end:]
    for nl, en in UI_EN:
        head = head.replace(nl, en)
        tail = tail.replace(nl, en)
    # Ook de taal van het document zelf, voor schermlezers en zoekmachines.
    head = head.replace('<html lang="nl"', '<html lang="en"', 1)
    return head + article + tail


def _pattern_style(config, page):
    """Zet de achtergrond-SVG als custom property, met een hash in de URL."""
    rel = "assets/architecture-pattern.svg"
    path = os.path.join(config["docs_dir"], rel)
    if not os.path.isfile(path):
        return ""
    with open(path, "rb") as handle:
        digest = hashlib.sha256(handle.read()).hexdigest()[:8]
    # Absoluut pad: een relatieve url() in een custom property wordt opgelost
    # vanuit de stylesheet, niet vanuit de pagina.
    base = urlparse(config.get("site_url") or "/").path or "/"
    if not base.endswith("/"):
        base += "/"
    url = base + rel + "?h=" + digest
    return '<style>:root{--tfa-pattern:url("%s")}</style>' % url


def on_post_page(output, page, config):
    """Lazy loading voor losse img-tags, plus de taal van de pagina op <body>.

    Met die taal laat de stylesheet in de zijbalk alleen de artikelen van de
    taal zien die de bezoeker leest; de taalknop in de kopbalk regelt de rest.
    """
    output = _IMG.sub('<img loading="lazy" decoding="async"', output)
    output = output.replace("</head>", _pattern_style(config, page) + "</head>", 1)
    lang = _lang(page)
    if lang == "en":
        output = _translate_ui(output)
    return output.replace("<body", '<body data-lang="%s"' % lang, 1)
