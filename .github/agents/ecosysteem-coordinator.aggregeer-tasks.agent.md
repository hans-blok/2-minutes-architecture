---
agent: ecosysteem-coordinator
intent: aggregeer-tasks
intent-id: 1003
betekeniseffect: geen-(conditioneel)
versie: 1.1.0
digest: 98d6
status: vers
---
# Ecosysteem-coordinator — Aggregeer Tasks

## Rolbeschrijving (korte samenvatting)

Aggregeer workspace-scopegebonden task-configuraties tot één uitvoerbare `.vscode/tasks.json`. De scope wordt volledig bepaald door `value_stream-fasen` in `beleid-workspace.md` — geen parameters vereist.

Altijd inbegrepen:
1. Alle tasks uit `fnd.01` (fundamentele agents)
2. Alle tasks voor fasen geconfigureerd in `beleid-workspace.md` (`value_stream-fasen`)

**VERPLICHT**: Raadpleeg de agent charter voor volledige context, grenzen en werkwijze.  
**Conventie**: Charter bevindt zich in `ecosysteem-coordinator.charter.md` in de parent folder van dit contract.

## Contract

### Input (wat gaat erin)

**Verplichte parameters**:
- Geen — de intent leest de scope automatisch uit `beleid-workspace.md` (`value_stream-fasen`)

**Optionele parameters**:
- output_file: Override voor output-pad (type: string, default: `.vscode/tasks.json`).
- dry_run: Toon wat zou worden samengevoegd zonder te schrijven (type: boolean, default: false).

**Automatisch gelezen uit `beleid-workspace.md`**:
- `value_stream-fasen`: Lijst van extra te verwerken fasen (bijv. `["aeo.02", "sfw.01"]`)

**Defensieve maatregelen (verplicht)**:
- Alleen de YAML frontmatter key `value_stream-fasen` in `beleid-workspace.md` bepaalt scope. Illustraties, voorbeelden en toelichtende opsommingen elders in het beleidsdocument mogen nooit als declaratieve input worden geïnterpreteerd.
- De eerste verwerkingsstap is het parsen van de YAML frontmatter. Bij ontbreken van `value_stream-fasen` faalt het proces hard — geen fallback, geen inferentie uit documentinhoud, geen alternatieve bronnen.

**Altijd meegenomen**:
- `fnd.01`: Fundamentele agents worden altijd toegevoegd, ongeacht workspace-configuratie

### Output (wat komt eruit)

De ecosysteem-coordinator levert:
- **Samengevoegde tasks.json**: Volledig JSON-bestand met alle agent tasks voor alle geconfigureerde fasen
  - version: "2.0.0"
  - tasks: Alle tasks uit agent-specifieke bestanden per geconfigureerde fase
  - inputs: Gecombineerde input-definities voor VS Code prompts
- **Console rapport**: Overzicht van verwerkte fasen, bestanden en task-counts

**Deliverable bestand**: `.vscode/tasks.json`

**Output-specificatie**:
```yaml
intent: aggregeer-tasks
output:
  - type: tasks-configuratie
    herkomstpositie: initiërend
    template: ~
```

**Outputformaat** (tasks.json):
```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "{vs}.{fase} - {agent}: {intent}",
      "type": "process",
      "command": "python",
      "args": [
        "artefacten/{vs}/{vs}.{fase}.{agent}/runners/{agent}.runner.py",
        "{intent}",
        "--param-1", "${input:paramName}"
      ]
    }
  ],
  "inputs": [
    {
      "id": "paramName",
      "type": "promptString",
      "description": "Parameter beschrijving"
    }
  ]
}
```

**Formaat-normering**:
- JSON conform VS Code tasks schema v2.0.0
- UTF-8 encoding
- 2-space indentation

**Contractuele templatebinding**:

```yaml
template: ~
```

### Foutafhandeling

De ecosysteem-coordinator:
- stopt wanneer `beleid-workspace.md` niet gevonden kan worden;
- stopt wanneer `value_stream-fasen` ontbreekt of leeg is in de YAML frontmatter van `beleid-workspace.md` (hard fail — geen zoeken in documentinhoud of andere bronnen);
- stopt wanneer geen task-bestanden gevonden worden voor de geconfigureerde fasen;
- stopt wanneer een task-bestand ongeldige JSON bevat;
- waarschuwt bij duplicate task labels (neemt laatste waarde);
- waarschuwt bij duplicate input IDs (neemt laatste waarde);
- vraagt NIET om verduidelijking (deterministische aggregatie op basis van workspace-configuratie).

---

## Werkwijze

### Stappen
1. **Lees `beleid-workspace.md`**: Extraheer `value_stream-fasen` lijst
2. **Rapporteer scope**: Print geconfigureerde fasen
3. **Scan per fase**: Zoek `artefacten/{vs}/{vs}.{fase}.*/tasks/*.tasks.json` voor elke fase
4. **Scan `.vscode/tasks/`**: Voeg eventuele handmatige task-bestanden toe
5. **Parse JSON**: Laad elk bestand en valideer structuur
6. **Merge tasks**: Combineer alle tasks arrays met deduplicatie op label
7. **Merge inputs**: Combineer alle inputs arrays met deduplicatie op ID
8. **Write output**: Schrijf samengevoegde tasks.json naar output_file
9. **Report**: Print overzicht van verwerkte fasen, bronbestanden en task-counts

### Kwaliteitsborging
- Alle geconfigureerde fasen worden verwerkt (geen stille weglating)
- Output JSON is syntactisch correct (valideer voor schrijven)
- Verwerkte bestanden en fasen worden gerapporteerd op stdout
- Task labels zijn uniek (warning bij duplicaten)

---

## Governance

**Doctrine-naleving:**
- **doctrine-agent-charter-normering.md** (v2.4.0, AEO.DOC.001):
  - Principe 4 (Scheiding van Wat en Hoe): Aggregeert alleen, wijzigt geen task-definities
  - Principe 7 (Transparante Verantwoording): Logt alle verwerkte fasen en bronbestanden
  - Richtlijn herkomstpositie: output `initiërend`
- **doctrine-traceability.md** (v1.1.0): Herkomstpositie `initiërend` — tasks.json start nieuwe configuratie-keten

- **doctrine-templategebruik.md** (v1.0.0):
  - Contractuele templatebinding expliciet opgenomen

**Canon-consultatie:**
- Geen canon-consultatie vereist (pure aggregatie op basis van workspace-configuratie)

**Transparantie-verplichtingen:**

Bij uitvoering logt de agent:
- ✓ Gelezen configuratie: `beleid-workspace.md` (value_stream-fasen)
- ✓ Verwerkte fasen
- ✓ Alle gelezen task-bestanden (paden)
- ✓ Aantal tasks per bronbestand
- ✓ Totaal aantal samengevoegde tasks
- ✓ Eventuele duplicaat-warnings

Logging-formaat: Console output

**Escalatie-paden:**
- → agent-engineer: indien task-bestanden ontbreken voor geconfigureerde fasen
- STOP: bij ontbrekende of ongeldige `value_stream-fasen` in `beleid-workspace.md`
- STOP: bij geen task-bestanden gevonden voor geconfigureerde fasen
- STOP: bij JSON parse errors

---

## Metadata

**Intent-ID**: `aeo.02.ecosysteem-coordinator.activeer-workspace-configuratie`  
**Versie**: 1.0.0  
**Value Stream**: Agent Ecosysteem Ontwikkeling (aeo)  
**Fase**: 02 — Ecosysteeminrichting  
**Classificatie**:
- Betekeniseffect: Geen (conditioneel)
- Werking: Conditioneel
- Bron-houding: Workspace-gebonden
