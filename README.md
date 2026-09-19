# 2-Minutes Architecture

Deze repository bevat de Markdown-bronbestanden voor de blogs van **2 Minuten IT-Architectuur**.

**Site:** https://www.2-minuten-it-architectuur.nl/

## Lokaal bouwen

```bash
pip install -r requirements-docs.txt
mkdocs serve      # lokale preview op http://127.0.0.1:8000
mkdocs build --strict
```

## Structuur

| Pad | Inhoud |
|---|---|
| `content/nl/`, `content/en/` | de artikelen, één bestand per blog |
| `content/index.md` | homepage |
| `content/stylesheets/extra.css` | alle vormgeving: design tokens, typografie en componenten |
| `hooks/site_hooks.py` | buildhooks voor metaregel, artikellijst, kerncijfers, lazy loading en cache busting |
| `overrides/partials/header.html` | eigen kopbalk met merkteken, sitenaam en taalknop |
| `docs/assets/` | bronbestanden van logo en taalvlaggen (niet meegebouwd) |
| `content/assets/` | de versies die de site gebruikt, afgeleid van `docs/assets/` |
| `site/` | gegenereerde site, wordt meegecommit |

## Een artikel toevoegen

Maak een bestand `content/nl/<nummer>-<slug>.md` met frontmatter:

```markdown
---
date: 2026-09-18
topic: "Services en API's"
description: "Eén zin die het artikel samenvat, ook gebruikt als meta description."
---

# Titel van het artikel

Eerste alinea.
```

De publicatiedatum, het onderwerp en de geschatte leestijd komen automatisch onder de titel te staan. Het artikel verschijnt vanzelf in de lijst op de homepage en de overzichtspagina, gesorteerd op datum; daarvoor hoeft alleen de `nav` in `mkdocs.yml` te worden bijgewerkt.

Op een overzichtspagina roepen twee placeholders die opbouw aan:

- `{{ artikellijst }}` voor de lijst, met `{{ artikellijst:nl:4 }}` voor een taal en een maximum;
Talen: de homepage op `/` is Nederlands, die op `/en/` Engels. De taalknop in de kopbalk verwijst naar de andere versie; de zijbalk toont alleen de artikelen van de taal die de bezoeker leest. Het thema draait in het Nederlands, dus de themalabels op Engelse pagina's worden in `hooks/site_hooks.py` vertaald.

## Caching

De site draait op GitHub Pages. Daar zijn geen eigen `Cache-Control`-headers in te stellen: GitHub Pages serveert alles met `max-age=600` en stuurt zelf een `ETag` mee, zodat een browser na tien minuten revalideert en bij een ongewijzigd bestand een `304` terugkrijgt. HTML wordt daarmee snel genoeg ververst na een publicatie. Compressie (gzip/brotli) regelt GitHub Pages eveneens zelf.

Omdat de headers vastliggen, is cache busting via bestandsnamen geregeld:

- **Themabestanden** van Material for MkDocs krijgen bij elke build een content hash in de bestandsnaam (`assets/javascripts/bundle.<hash>.min.js`).
- **Eigen CSS en JavaScript** krijgen in `hooks/site_hooks.py` (`on_config`) een sha256-hash van acht tekens als queryparameter: `stylesheets/extra.css?h=9eb16f45`. Verandert de inhoud van het bestand, dan verandert de URL en haalt de browser de nieuwe versie op. Verandert er niets, dan blijft de gecachte versie geldig.

Handmatige versienummers zijn daarmee nergens nodig. Nieuwe HTML kan nooit met oude CSS worden gecombineerd, omdat de HTML zelf de gehashte URL bevat.

Een service worker of PWA-caching is bewust niet toegevoegd: de site is klein en statisch, en een service worker zou bezoekers juist het risico geven dat zij na een publicatie een verouderd artikel blijven zien.

## Publiceren

Een push naar `main` start de workflow in `.github/workflows/pages-build-deployment.yml`, die `mkdocs build --strict` draait en het resultaat naar GitHub Pages deployt.
