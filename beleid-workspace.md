---
workspace: 2-minutes-architecture
value_stream: KNV
value_stream-fasen: ["KNV.01", "KNV.02", "KNV.03", "KNV.04"]
canon_github_url: https://github.com/hans-blok/entoli-canon.git
---

# Beleid voor de 2-minutes-architecture workspace

Deze workspace hoort bij de waardestroom **Kennisvastlegging** **(KNV)**.

**Type**: Waarde value stream  
**Omschrijving**: Deze value stream richt zich op het expliciet maken, structureren en duurzaam vastleggen van kennis. Het doel is om kennis herbruikbaar, doorzoekbaar en overdraagbaar te maken binnen en buiten het ecosysteem. Agents in deze value stream produceren **bedrijfs-artefacten** (een specialisatie van normerende artefacten).

**Fasen**:
01. **Kennisverkenning**  
   Het identificeren van kennisdomeinen, lacunes en bestaande kennisbronnen die geëxpliciteerd moeten worden.
02. **Structurering**  
   Het ordenen en categoriseren van kennis volgens een herkenbare en toegankelijke structuur.
03. **Vastlegging**  
   Het daadwerkelijk documenteren en formaliseren van kennis in een geschikt formaat.
04. **Publicatie en Onderhoud**  
   Het beschikbaar maken van kennis voor gebruikers en het actueel houden ervan gedurende de levenscyclus.

## Verplichte leesvolgorde van grondslagen

Elke geautomatiseerde rol, agent of runner hanteert bij aanvang van zijn functioneren de volgende verplichte leesvolgorde:

**In de centrale canon repository** (zie `canon_github_url` in de frontmatter):
1. `grondslagen/.bronnen/`
2. filtering op de algemene ontologie en de ontologie die specifiek is voor de toegewezen value stream
3. toepassing van generieke regels en de regels die van toepassing zijn op de relevante value-streamfase

**In deze workspace**:
4. workspace-specifiek beleid (dit bestand)

Het overslaan, herordenen of impliciet toepassen van deze leesvolgorde is niet toegestaan.

**Zonder aantoonbare toepassing van de constitutie is handelen ongeldig.**

## Dit beleid is workspace-specifiek

Dit beleid beschrijft alleen de workspace-specifieke scope. Voor alle regels, uitzonderingen, details en constitutionele bepalingen volgen we volledig de richtlijnen in de centrale canon repository.

De constitutie, algemene regels en governance voor alle workspaces staan in de centrale canon repository, zoals vastgelegd in `canon_github_url` in de frontmatter.

## Canon Repository Synchronisatie

In alle geautomatiseerde en handmatige processen wordt de centrale canon repository geraadpleegd. Dit gebeurt altijd eerst met een `git pull` om te waarborgen dat de meest recente grondslagen worden gebruikt.

**Foutmelding**: Wanneer de canon-repository niet bereikbaar is of niet kan worden gevonden, wordt een foutmelding gegeven en stopt het proces.

## Scope

### Wat we in deze workspace vastleggen

- Het publiceren van blogs over IT-architectuur.
- Het vastleggen en beheren van content en artikelen met betrekking tot IT-architectuur ten behoeve van publicatie.

### Wat niet in deze workspace hoort

Andere domeinen vallen buiten deze workspace en horen in andere repositories. Voorbeelden hiervan zijn:
- Ontwikkeling van IT-systemen en applicaties (Valt onder de bouw value streams).
- Persoonlijke aantekeningen of niet-IT gerelateerde notities.

## Convention over Configuration

Deze workspace hanteert het principe **Convention over Configuration** (*charter-driven self-discovery*):

- **Minimale invoer**: Agents en runners verwachten alleen de strikt noodzakelijke parameters van de gebruiker.
- **Automatische ontdekking**: Alle overige artefacten worden automatisch afgeleid uit de folder-structuur en naamconventies.
- **Charter als beleidsbron**: Het charter van een agent bepaalt welke artefacten relevant zijn voor die agent.
- **Geen redundante invoer**: Parameters die uit conventie of charter af te leiden zijn, worden niet aan de gebruiker gevraagd.

## Workspace-specifieke aanvullingen

- [Aanvulling 1: bijv. taalgebruik, documentatiestijl]
- [Aanvulling 2: bijv. specifieke werkwijze of proces]
- [Aanvulling 3: bijv. logging of traceerbaarheid]

---

*Laatste update: [DATUM] door [NAAM]*
