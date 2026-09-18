"""Build hooks voor 2 Minuten IT-Architectuur.

Verzorgt vier dingen, zonder extra afhankelijkheden:

1. metaregel onder de artikeltitel: publicatiedatum, onderwerp en leestijd;
2. artikelkaarten op de overzichtspagina's via de placeholder {{ artikelkaarten }};
3. lazy loading en async decoding voor afbeeldingen in de artikelen;
4. cache busting: aan extra_css en extra_javascript wordt een content hash
   gehangen, zodat een nieuwe deployment nooit oude CSS bij nieuwe HTML serveert.
"""

import hashlib
import os
import re

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
_CARDS = re.compile(r"\{\{\s*artikelkaarten(?::(nl|en))?(?::(\d+))?\s*\}\}")


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


def _cards(docs_dir, lang, limit=None, prefix=""):
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

    out = ['<ul class="card-grid">']
    for article in articles:
        out.append('<li class="card">')
        out.append(
            '<a class="card__link" href="%s"><h3 class="card__title">%s</h3></a>'
            % (article["href"], article["title"])
        )
        if article.get("description"):
            out.append('<p class="card__text">%s</p>' % article["description"])
        meta_bits = []
        if article.get("topic"):
            meta_bits.append('<span class="card__topic">%s</span>' % article["topic"])
        if article.get("date"):
            meta_bits.append(
                '<time datetime="%s">%s</time>'
                % (article["date"], _format_date(article["date"], lang, short=True))
            )
        meta_bits.append("<span>%s</span>" % _reading_time(article["body"], lang))
        out.append('<p class="card__meta">%s</p>' % "".join(meta_bits))
        out.append("</li>")
    out.append("</ul>")
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

    def expand(match):
        card_lang = match.group(1) or lang
        limit = int(match.group(2)) if match.group(2) else None
        # Kaarten verwijzen relatief, zodat ze vanaf elke pagina kloppen.
        depth = page.file.src_uri.count("/")
        prefix = "../" * depth + card_lang + "/"
        return _cards(config["docs_dir"], card_lang, limit, prefix)

    markdown = _CARDS.sub(expand, markdown)

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

    return _IMG.sub('<img loading="lazy" decoding="async"', markdown)


def on_post_page(output, page, config):
    """Afbeeldingen uit Markdown krijgen dezelfde lazy loading als losse img-tags."""
    return _IMG.sub('<img loading="lazy" decoding="async"', output)
