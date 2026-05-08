---
agent: ecosysteem-coordinator
intent: genereer-instructies
intent-id: 1004
betekeniseffect: realiserend
versie: 1.2.0
digest: 7cea
status: vers
---
# Ecosysteem-coordinator — Genereer Instructies

## Rolbeschrijving (korte samenvatting)

Voert **broninjectie** uit voor een opgegeven agent en intent. De runner assembleert twee soorten bronnen:

- **Kaderbronnen** — het normatieve kader dat de executie stuurt: constitutie, workspace-beleid, doctrines, agent charter en agent contract (in die volgorde). Welke doctrines worden opgenomen, wordt vóór inhoudelijke opname bepaald door het **bronselectiebeleid** (`bronselectiebeleid.json` in entoli-canon).
- **Werkbronnen** — het uitvoeringsmateriaal: de opgegeven parameters en prompt-specifieke instructies

Het resultaat van de bronassemblage is het **bronpakket**: de execution file in `executions/` die het LLM als volledige context ontvangt. Het bronpakket is opgebouwd als een gelaagde inhoudsstructuur met 7 afzonderlijke secties (zie Output).

**VERPLICHT**: Raadpleeg de agent charter voor volledige context, grenzen en werkwijze.  
**Conventie**: Charter bevindt zich in `ecosysteem-coordinator.charter.md` in de parent folder van dit contract.

## Contract

### Input (wat gaat erin)

**Verplichte parameters**:
- agent: Naam van de agent waarvoor instructies worden gegenereerd (type: string, kebab-case).
- intent: Intent naam voor instructie-generatie (type: string, kebab-case).

**Optionele parameters**:
- execution_file: Pad waar execution-bestand wordt geschreven (type: string, default: auto-generated in executions/).
- params: Key=value parameters voor placeholder substitutie (type: list[string], format: "key=value").
- skip_bootstrap: Sla canon-consultatie over (type: boolean, default: false, alleen voor development).
- method: Execution method voor audit (type: string, choices: manual|runner|pipeline, default: manual).

### Output (wat komt eruit)

De ecosysteem-coordinator levert:
- **Het bronpakket** (execution file): het samengestelde geheel van kaderbronnen en werkbronnen als gelaagde inhoudsstructuur, opgebouwd uit 7 secties:
  1. YAML frontmatter: `execution_id`, `execution_digest`, `timestamp`, `agent`, `intent`, `value_stream_fase`, `canon_ref`, `bronhouding`, `modus`
  2. Opdracht en parameters
  3. Geldende bronhouding en bronregime (excerpt bronhouding-doctrine + bronselectierapport)
  4. Normatieve grondslagen (constitutie → workspace-beleid → geselecteerde doctrines)
  5. Agentcontext (charter → contract → prompt)
  6. Werkbronnen (optioneel — input-bestanden)
  7. Bronmanifest en traceerbaarheid (tabel alle bronnen, incl. uitgesloten met reden, opnamevorm en reden_van_opname)
- **Het execution-trace-bestand** (`.trace.yaml`): apart traceerbaarheidsartefact naast het execution-bestand met execution-anker (execution_id + execution_digest) en per-bron bronpad, type, digest, reden_van_opname, opnamevorm
- **Console output**: samenvatting van de bronassemblage, bronselectieprofiel en pad naar het bronpakket

**Deliverable bestand**: `executions/{hash}.{agent}.{intent}.md` (execution-bestand) + `executions/{hash}.{agent}.{intent}.trace.yaml` (trace-bestand)

**Outputformaat** (bronpakket / execution file):
```markdown
---
execution_id: {4-char-hash}
execution_digest: {12-char-sha256}
timestamp: {ISO-8601}
agent: {agent}
intent: {intent}
value_stream_fase: {vs.fase}
canon_ref: {commit-sha}
bronhouding: {bronhouding-type}
modus: handmatig
---

# Opdracht

Voer de intent `{intent}` uit voor de agent `{agent}`...

## Parameters
- {key}: {value}

---

# Geldende bronhouding en bronregime

{excerpt doctrine-bronhouding-en-exploratie}

## Actief bronregime: {bronhouding-type}

{instructie}

## Bronselectie
- Toegepast profiel: `{sleutel}`
- Opgenomen doctrines (N): ...
- Uitgesloten doctrines (M): ...

---

# Normatieve grondslagen

## Constitutie
{content}

## Workspace-beleid
{content}

## Doctrines
### {pad}
{content}

---

# Agentcontext

## Charter
{content}

## Contract
{content}

## Prompt
{content}

---

# Werkbronnen  *(optioneel)*
## {bestandsnaam}
{content}

---

# Bronmanifest

| Bron | Bronrol | Type | Digest | Status | Opname | Opnamevorm | Reden |
|------|---------|------|--------|--------|--------|------------|-------|
| constitutie.md | kaderbron | constitutie | `{digest}` | {status} | opgenomen | volledig | altijd verplicht (structureel) |
| {doctrine} | kaderbron | doctrine | `{digest}` | {status} | opgenomen | volledig | bronselectieprofiel '{sleutel}' |
| {doctrine} | kaderbron | doctrine | `{digest}` | {status} | uitgesloten: profiel `{sleutel}` | — | uitgesloten: profiel '{sleutel}' |
```

**Formaat-normering**: 
- Markdown met YAML frontmatter
- UTF-8 encoding zonder BOM

**Contractuele templatebinding**:

```yaml
template: ~
```

### Foutafhandeling

De ecosysteem-coordinator:
- stopt wanneer agent niet gevonden wordt in artefacten/ structuur;
- stopt wanneer intent niet gevonden wordt (geen matching prompt of contract);
- stopt wanneer charter ontbreekt voor opgegeven agent;
- vraagt NIET om verduidelijking (auto-discovery based);
- escaleert naar agent-engineer indien prompt-bestand ontbreekt (scaffolding nodig);
- logt warning wanneer contract ontbreekt maar gaat door met alleen charter + prompt.

---

## Werkwijze

### Stappen
1. **Consulteer canon**: Registreer canon SHA als audit-anker (tenzij skip_bootstrap)
2. **Locate agent artefacten**: Zoek agent folder in artefacten/{vs}/{vs}.{fase}.{agent}/
3. **Bronselectie**: Raadpleeg `bronselectiebeleid.json` in entoli-canon en bepaal de doctrine-whitelist voor `{agent}.{intent}` vóór inhoudelijke opname; bronhouding-doctrine is altijd verplicht
4. **Laad kaderbronnen** in volgorde:
   - Constitutie (uit entoli-canon)
   - Workspace-beleid (`beleid-workspace.md`)
   - Geselecteerde doctrines (gefilterd op basis van bronselectiebeleid + value_stream_fase)
   - Charter (`{agent}.charter.md`)
   - Contract (`{agent}.{intent}.agent.md`)
5. **Laad werkbronnen**: parameters en prompt-specifieke instructies (`entoli.{agent}.{intent}.prompt.md`)
6. **Voer placeholder-substitutie uit**: werkbronnen injecteren in templates
7. **Stel het bronpakket samen** als 7-laagse inhoudsstructuur
8. **Schrijf het bronpakket**: naar execution_file pad; bereken `execution_digest` (SHA-256 van body, 12 hex tekens)
9. **Schrijf trace-bestand**: genereer `{hash}.{agent}.{intent}.trace.yaml` naast het execution-bestand met execution-anker + per-bron opnameregistratie

### Kwaliteitsborging
- Execution ID is uniek (timestamp + agent hash); execution_digest is inhoudgebonden (SHA-256 body)
- Execution-anker (execution_id + execution_digest) aanwezig in zowel execution-bestand als trace-bestand
- Canon reference is altijd aanwezig als audit-anker (of expliciet "skipped")
- Kaderbronnen zijn altijd aanwezig en in de juiste volgorde
- Alle bronnen worden geregistreerd met opnamevorm en reden_van_opname in bronmanifest én trace-bestand

---

## Governance

**Doctrine-naleving:**
- **doctrine-agent-charter-normering.md** (v2.1.0, AEO.DOC.001):
  - Principe 1 (Identiteit vóór Implementatie): Assembleert bestaande definities
  - Principe 7 (Transparante Verantwoording): Volledige logging van samenstellingsproces
  - Principe 9 (Output-formaat Normering): Markdown default

- **doctrine-templategebruik.md** (v1.0.0):
  - Contractuele templatebinding expliciet opgenomen

**Canon-consultatie:**
- Roept `ecosysteem-coordinator.consulteer-canon` aan als eerste stap
- Canon-context wordt opgenomen in execution bestand

**Transparantie-verplichtingen:**

Bij uitvoering logt de agent:
- ✓ Alle geladen kaderbronnen (constitutie, beleid, doctrines, charter, contract) met paden
- ✓ Alle geladen werkbronnen (parameters, prompt)
- ✓ Gegenereerd bronpakket (pad, execution_id en execution_digest)
- ✓ Gegenereerd trace-bestand (pad)
- ✓ Canon commit reference (audit-anker)


**Escalatie-paden:**
- → agent-engineer: indien prompt-bestand ontbreekt (scaffolding vereist)
- → capability-architect: indien charter ontbreekt (boundary niet gedefinieerd)
- STOP: bij agent folder niet gevonden

---

## Metadata

**Intent-ID**: `aeo.02.ecosysteem-coordinator.genereer-instructies`  
**Versie**: 1.0.0  
**Value Stream**: Agent Ecosysteem Ontwikkeling (aeo)  
**Fase**: 02 — Ecosysteeminrichting  
**Classificatie**: Conditioneel / Input-gebonden
