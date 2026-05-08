---
agent: ecosysteem-coordinator
intent: run-latest-execution
intent-id: 1070
betekeniseffect: realiserend
versie: 1.0.0
digest: 6179
status: vers
---
# Ecosysteem-coordinator — Run Latest Execution

## Rolbeschrijving (korte samenvatting)

Voert het meest recente execution-bestand in `executions/` uit via `./scripts/run_agent.sh`. Het meest recente bestand wordt automatisch bepaald op basis van tijdstempel — geen parameters vereist.

**VERPLICHT**: Raadpleeg de agent charter voor volledige context, grenzen en werkwijze.  
**Conventie**: Charter bevindt zich in `ecosysteem-coordinator.charter.md` in de parent folder van dit contract.

## Contract

### Input (wat gaat erin)

**Verplichte parameters**:
- Geen — de intent selecteert automatisch het meest recente `executions/*.prompt-instruction.md` bestand

**Optionele parameters**:
- Geen

**Automatisch bepaald**:
- Meest recente bestand via `ls -t executions/*.prompt-instruction.md | head -n1`

### Output (wat komt eruit)

De ecosysteem-coordinator levert:
- **Exit-status**: De exit-code van `run_agent.sh` wordt als eigen exit-code teruggegeven
- **Console output**: Doorgegeven vanuit `run_agent.sh`

Er worden geen nieuwe artefacten aangemaakt door deze intent zelf.

### Procedure (hoe werkt het)

1. Bepaal het meest recente bestand: `Get-ChildItem -Recurse -Path executions -Filter '*.prompt-instruction.md' | Sort-Object Name -Descending | Select-Object -First 1`
2. Controleer dat er ten minste één bestand bestaat; bij geen bestanden: hard falen met foutmelding
3. Zoek de Claude CLI op: `Get-ChildItem "$env:USERPROFILE\.vscode\extensions\anthropic.claude-code-*\resources\native-binary\claude.exe" | Sort-Object Name -Descending | Select-Object -First 1`
4. Voer uit: `Get-Content <bestand> -Raw | & <claude.exe>`
5. Geef de exit-code van de Claude CLI terug als eigen exit-code

### Foutafhandeling

| Situatie | Gedrag |
|----------|--------|
| Geen `executions/*.prompt-instruction.md` bestanden aanwezig | Hard falen met duidelijke foutmelding |
| Claude CLI (`claude.exe`) niet gevonden in VS Code extensions-map | Hard falen met verwijzing naar ontbrekende installatie |
| Claude CLI geeft non-zero exit | Exit-code wordt 1:1 doorgegeven |

### Grenzen

- Selecteert uitsluitend bestanden met extensie `.prompt-instruction.md` in de `executions/` map (recursief, gesorteerd op naam)
- Voert geen eigen verwerking uit op de inhoud van het execution-bestand — delegeert volledig aan de Claude CLI
- Zoekt de Claude CLI automatisch op in `$env:USERPROFILE\.vscode\extensions\anthropic.claude-code-*`
- Wijzigt geen artefacten, ledger of logbestanden
