#!/usr/bin/env python3
"""
rename_to_entoli.py — Hernoeming 'mandarin' → 'entoli' in een workspace.

Vervangt alle tekstuele verwijzingen naar 'mandarin' (alle hoofdlettervormen)
in bestandsinhoud, bestandsnamen en mapnamen.

Uitzondering: URL's (patronen met '://') blijven ongewijzigd.

Gebruik:
    python rename_to_entoli.py [--dry-run] <workspace-pad>

Opties:
    --dry-run    Preview: toont wat gewijzigd zou worden zonder iets te schrijven.

Algoritme (volgorde is kritisch):
    Fase 1 — Inhoud van tekstbestanden vervangen
    Fase 2 — Bestanden hernoemen (leaf-bestanden eerst)
    Fase 3 — Mappen hernoemen (bottom-up, diepste eerst)
"""

import os
import re
import sys
import argparse
from pathlib import Path

# ---------------------------------------------------------------------------
# Constanten
# ---------------------------------------------------------------------------

# Mappen die altijd worden overgeslagen (case-insensitief vergeleken)
EXCLUDED_DIRS = {'.git', '.venv', '__pycache__', 'node_modules', 'site'}

# URL-patroon: alles met '://' wordt als URL beschouwd en niet vervangen
URL_RE = re.compile(r'(?:https?|ftp|file)://\S+')

# Zoekpatroon voor 'mandarin' (case-insensitief)
# Intern opgebouwd als bytes-achtig patroon zodat dit script zichzelf
# niet aanpast wanneer het eigen bronbestand wordt verwerkt.
_ZOEK = 'm' + 'andarin'
MANDARIN_RE = re.compile(r'(?i)' + _ZOEK)

# Vervangtabel voor naam van dit script (mag niet worden aangepast)
SELF_PATH = os.path.abspath(__file__)


# ---------------------------------------------------------------------------
# Vervanging
# ---------------------------------------------------------------------------

def _vervang_woord(match: re.Match) -> str:
    """Case-preserverende vervanging van één treffer."""
    w = match.group(0)
    if w.isupper():
        return 'ENTOLI'
    if w[0].isupper():
        return 'Entoli'
    return 'entoli'


def vervang_mandarin(tekst: str) -> str:
    """Vervang alle voorkomens van 'mandarin' (case-preserverend)."""
    return MANDARIN_RE.sub(_vervang_woord, tekst)


def vervang_inhoud(tekst: str) -> str:
    """
    Vervang 'mandarin' in tekst, maar laat URL's ongewijzigd.

    Werking: splits de tekst op URL-treffers, vervang in de tussenstukken,
    voeg daarna URLs en tussenstukken weer samen.
    """
    delen = URL_RE.split(tekst)
    urls = URL_RE.findall(tekst)

    resultaat = []
    for i, deel in enumerate(delen):
        resultaat.append(vervang_mandarin(deel))
        if i < len(urls):
            resultaat.append(urls[i])   # URL ongewijzigd toevoegen

    return ''.join(resultaat)


def heeft_mandarin(tekst: str) -> bool:
    """True als 'mandarin' (case-insensitief) in tekst voorkomt."""
    return bool(MANDARIN_RE.search(tekst))


# ---------------------------------------------------------------------------
# Bestandsverwerking
# ---------------------------------------------------------------------------

def is_uitgesloten_map(pad: Path) -> bool:
    """True als enig onderdeel van het pad in EXCLUDED_DIRS staat."""
    return any(deel.lower() in EXCLUDED_DIRS for deel in pad.parts)


def verwerk_bestand_inhoud(pad: Path, dry_run: bool) -> bool:
    """
    Vervang 'mandarin' in de inhoud van één bestand.

    Retourneert True als het bestand is (of zou worden) gewijzigd.
    Binaire bestanden worden overgeslagen (geen inhoudswijziging).
    """
    # Zelf-uitsluiting: dit script mag zijn eigen inhoud niet aanpassen
    if os.path.abspath(pad) == SELF_PATH:
        return False

    try:
        origineel = pad.read_text(encoding='utf-8')
    except (UnicodeDecodeError, PermissionError):
        # Binair bestand of leesfout → inhoud overslaan
        return False

    nieuw = vervang_inhoud(origineel)
    if nieuw == origineel:
        return False

    if dry_run:
        print(f'[DRY][content]  {pad}')
    else:
        pad.write_text(nieuw, encoding='utf-8')
        print(f'[content]  {pad}')

    return True


def nieuwe_naam(naam: str) -> str:
    """Geef de nieuwe naam terug (alleen naam, geen pad)."""
    return vervang_mandarin(naam)


# ---------------------------------------------------------------------------
# Hoofdlogica
# ---------------------------------------------------------------------------

def verzamel_bestanden_en_mappen(root: Path):
    """
    Doorloop de workspace en verzamel:
      - alle bestanden (met volledig pad)
      - alle mappen (met volledig pad), gesorteerd van diep naar ondiep

    Slaat uitgesloten mappen over.
    """
    bestanden = []
    mappen = []

    for dirpad, subdirs, bestandsnamen in os.walk(root, topdown=True):
        dirpad = Path(dirpad)

        # Relatief pad voor uitsluitingscheck
        try:
            rel = dirpad.relative_to(root)
        except ValueError:
            rel = dirpad

        if is_uitgesloten_map(rel):
            subdirs.clear()
            continue

        # Filter uitgesloten subdirs in-place (beïnvloedt os.walk)
        subdirs[:] = [
            d for d in subdirs
            if d.lower() not in EXCLUDED_DIRS
        ]

        # Verzamel bestanden in deze map
        for naam in bestandsnamen:
            bestanden.append(dirpad / naam)

        # Verzamel de map zelf (niet de root)
        if dirpad != root:
            mappen.append(dirpad)

    # Mappen bottom-up sorteren: diepste paden eerst
    mappen.sort(key=lambda p: len(p.parts), reverse=True)

    return bestanden, mappen


def run(workspace: Path, dry_run: bool):
    """Voer de volledige hernoeming uit op één workspace."""

    print(f'\n{"[DRY-RUN] " if dry_run else ""}Workspace: {workspace}')
    print('=' * 60)

    if not workspace.is_dir():
        print(f'FOUT: map bestaat niet: {workspace}', file=sys.stderr)
        sys.exit(1)

    bestanden, mappen = verzamel_bestanden_en_mappen(workspace)

    # ------------------------------------------------------------------
    # Fase 1: Inhoud vervangen
    # ------------------------------------------------------------------
    print('\n--- Fase 1: Inhoud ---')
    inhoud_teller = 0
    for pad in bestanden:
        if verwerk_bestand_inhoud(pad, dry_run):
            inhoud_teller += 1

    # ------------------------------------------------------------------
    # Fase 2: Bestanden hernoemen
    # ------------------------------------------------------------------
    print('\n--- Fase 2: Bestanden hernoemen ---')
    bestand_teller = 0
    for oud_pad in bestanden:
        oude_naam = oud_pad.name
        nieuwe = nieuwe_naam(oude_naam)
        if nieuwe != oude_naam:
            nieuw_pad = oud_pad.parent / nieuwe
            if dry_run:
                print(f'[DRY][rename]   {oud_pad}  →  {nieuw_pad.name}')
            else:
                oud_pad.rename(nieuw_pad)
                print(f'[rename]   {oud_pad}  →  {nieuw_pad.name}')
            bestand_teller += 1

    # ------------------------------------------------------------------
    # Fase 3: Mappen hernoemen (bottom-up)
    # ------------------------------------------------------------------
    print('\n--- Fase 3: Mappen hernoemen ---')
    map_teller = 0
    for oud_pad in mappen:
        oude_naam = oud_pad.name
        nieuwe = nieuwe_naam(oude_naam)
        if nieuwe != oude_naam:
            nieuw_pad = oud_pad.parent / nieuwe
            if dry_run:
                print(f'[DRY][dir]     {oud_pad}  →  {nieuw_pad.name}')
            else:
                oud_pad.rename(nieuw_pad)
                print(f'[dir]     {oud_pad}  →  {nieuw_pad.name}')
            map_teller += 1

    # ------------------------------------------------------------------
    # Samenvatting
    # ------------------------------------------------------------------
    prefix = '[DRY] ' if dry_run else ''
    print(f'\n{prefix}Klaar.')
    print(f'{prefix}  Inhoud bijgewerkt : {inhoud_teller} bestand(en)')
    print(f'{prefix}  Bestanden hernoemd: {bestand_teller}')
    print(f'{prefix}  Mappen hernoemd   : {map_teller}')


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Vervang 'mandarin' door 'entoli' in een workspace."
    )
    parser.add_argument(
        'workspace',
        type=Path,
        help='Pad naar de workspace-root (bijv. c:\\git\\mandarin-canon)'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Preview: toon wat gewijzigd zou worden zonder iets te schrijven'
    )
    args = parser.parse_args()

    run(args.workspace.resolve(), args.dry_run)


if __name__ == '__main__':
    main()
