#!/usr/bin/env python3
"""fetch_ecosysteem_coordinator.py - Kopieert ecosysteem-coordinator prompts, contracts en tasks
vanuit entoli-agents naar deze workspace.

Bron:
  artefacten/fnd/fnd.01.ecosysteem-coordinator/prompts/*.prompt.md
  artefacten/fnd/fnd.01.ecosysteem-coordinator/agent-contracten/*.agent.md
  artefacten/fnd/fnd.01.ecosysteem-coordinator/tasks/*.tasks.json

Doel:
  .github/prompts/
  .github/agents/
  .vscode/tasks.json

Gebruik:
    python scripts/fetch_ecosysteem_coordinator.py
    python scripts/fetch_ecosysteem_coordinator.py --source ../entoli-agents --target .
    python scripts/fetch_ecosysteem_coordinator.py --dry-run
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Tuple, TextIO

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent
SIBLING_AGENTS = REPO_ROOT.parent / "entoli-agents"

DEFAULT_SOURCE = (
    SIBLING_AGENTS.resolve()
    if (REPO_ROOT.name != "entoli-agents" and SIBLING_AGENTS.exists())
    else REPO_ROOT
)
DEFAULT_TARGET = REPO_ROOT


class TeeWriter:
    """Schrijf output naar zowel console als logbestand."""
    
    def __init__(self, console: TextIO, logfile: TextIO):
        self.console = console
        self.logfile = logfile
    
    def write(self, text: str):
        # Console: vervang unicode tekens die niet werken op Windows cp1252
        try:
            self.console.write(text)
        except UnicodeEncodeError:
            # Fallback: vervang problematische tekens
            safe_text = text.replace('\u2717', 'x').replace('\u2713', 'v')
            self.console.write(safe_text)
        self.logfile.write(text)
        self.logfile.flush()
    
    def flush(self):
        self.console.flush()
        self.logfile.flush()


def collect_ecosysteem_files(artefacten_root: Path) -> Tuple[List[Tuple[Path, str]], List[Tuple[Path, str]], List[Path]]:
    """Zoek alle prompt-, agent- en task-bestanden voor fnd.01.ecosysteem-coordinator.

    Retourneert (prompts, contracts, task_files) als lijsten van (src_path, dest_name) en task_files.
    """
    base = artefacten_root / "fnd" / "fnd.01.ecosysteem-coordinator"
    if not base.is_dir():
        raise SystemExit(
            f"ERROR: Map niet gevonden: {base}.\n"
            "Zorg dat je source wijst naar de entoli-agents repository (met artefacten/fnd/...)."
        )

    prompts_dir = base / "prompts"
    contracts_dir = base / "agent-contracten"
    tasks_dir = base / "tasks"

    prompts: List[Tuple[Path, str]] = []
    contracts: List[Tuple[Path, str]] = []
    task_files: List[Path] = []

    if prompts_dir.is_dir():
        for f in sorted(prompts_dir.glob("*.prompt.md")):
            prompts.append((f, f.name))

    if contracts_dir.is_dir():
        for f in sorted(contracts_dir.glob("*.agent.md")):
            contracts.append((f, f.name))

    if tasks_dir.is_dir():
        for f in sorted(tasks_dir.glob("*.tasks.json")):
            task_files.append(f)

    return prompts, contracts, task_files


def copy_files(
    items: List[Tuple[Path, str]],
    target_dir: Path,
    dry_run: bool,
    label: str,
) -> int:
    """Kopieer bestanden naar target_dir; retourneert aantal gekopieerde items."""
    if not items:
        print(f"{label}: (geen)")
        return 0

    if not dry_run:
        target_dir.mkdir(parents=True, exist_ok=True)

    count = 0
    for src, name in items:
        dest = target_dir / name
        if dry_run:
            print(f"  [dry] {label}: {src} -> {dest}")
        else:
            shutil.copy2(src, dest)
            print(f"  OK {label}: {src.name} -> {dest}")
        count += 1

    return count


def clean_folder(folder_path: Path, pattern: str, dry_run: bool) -> int:
    """Verwijder alle bestanden in folder die matchen met pattern."""
    if not folder_path.exists():
        return 0
    
    files = list(folder_path.glob(pattern))
    if not files:
        return 0
    
    for f in files:
        if dry_run:
            print(f"  [dry] Verwijder: {f.name}")
        else:
            f.unlink()
            print(f"  ✗ Verwijderd: {f.name}")
    
    return len(files)


def merge_and_write_tasks(
    task_files: List[Path],
    target_file: Path,
    source_root: Path,
    target_root: Path,
    dry_run: bool,
) -> int:
    """Merge task-bestanden en schrijf naar tasks.json; retourneert aantal tasks.
    
    Herschrijft paden in args zodat ze verwijzen naar de source repo relatief aan de target.
    """
    if not task_files:
        print("Tasks: (geen)")
        return 0

    # Bereken relatief pad van target naar source (bijv. ../entoli-agents)
    try:
        rel_source = Path("..") / source_root.name
    except Exception:
        rel_source = source_root

    merged: Dict[str, Any] = {
        "version": "2.0.0",
        "tasks": [],
        "inputs": [],
    }

    task_labels_seen: set = set()
    input_ids_seen: set = set()

    for task_file in task_files:
        try:
            with open(task_file, "r", encoding="utf-8") as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            print(f"  FOUT: Ongeldige JSON in {task_file}: {e}")
            continue

        # Merge tasks
        for task in data.get("tasks", []):
            label = task.get("label", "")
            if label in task_labels_seen:
                print(f"  WAARSCHUWING: Duplicate task label '{label}', overschreven")
            else:
                task_labels_seen.add(label)
            
            # Herschrijf paden in args die beginnen met 'artefacten/'
            if "args" in task:
                new_args = []
                for arg in task["args"]:
                    if isinstance(arg, str) and arg.startswith("artefacten/"):
                        # Voeg relatieve source pad toe
                        new_args.append(str(rel_source / arg).replace("\\", "/"))
                    else:
                        new_args.append(arg)
                task["args"] = new_args
            
            # Remove existing task with same label and add new one
            merged["tasks"] = [t for t in merged["tasks"] if t.get("label") != label]
            merged["tasks"].append(task)

        # Merge inputs
        for inp in data.get("inputs", []):
            inp_id = inp.get("id", "")
            if inp_id in input_ids_seen:
                print(f"  WAARSCHUWING: Duplicate input ID '{inp_id}', overschreven")
            else:
                input_ids_seen.add(inp_id)
            # Remove existing input with same id and add new one
            merged["inputs"] = [i for i in merged["inputs"] if i.get("id") != inp_id]
            merged["inputs"].append(inp)

        print(f"  OK task-source: {task_file.name}")

    if dry_run:
        print(f"  [dry] tasks.json: {len(merged['tasks'])} tasks, {len(merged['inputs'])} inputs -> {target_file}")
    else:
        target_file.parent.mkdir(parents=True, exist_ok=True)
        with open(target_file, "w", encoding="utf-8") as f:
            json.dump(merged, f, indent=2, ensure_ascii=False)
            f.write("\n")
        print(f"  OK tasks.json: {len(merged['tasks'])} tasks, {len(merged['inputs'])} inputs -> {target_file}")

    return len(merged["tasks"])


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        description="Kopieer ecosysteem-coordinator prompts en contracts vanuit entoli-agents."
    )
    parser.add_argument(
        "--source",
        type=Path,
        default=DEFAULT_SOURCE,
        help=f"Pad naar entoli-agents (default: {DEFAULT_SOURCE})",
    )
    parser.add_argument(
        "--target",
        type=Path,
        default=DEFAULT_TARGET,
        help=f"Doel workspace (default: {DEFAULT_TARGET})",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Toon wat er zou worden gekopieerd zonder te schrijven",
    )
    args = parser.parse_args(argv)

    source_root = args.source.expanduser().resolve()
    target_root = args.target.expanduser().resolve()
    artefacten_root = source_root / "artefacten"

    if not artefacten_root.is_dir():
        parser.error(
            f"artefacten/ map ontbreekt in {source_root}. "
            "Gebruik --source om de entoli-agents repo aan te wijzen."
        )

    # Setup logging naar /logs
    logs_dir = target_root / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    log_file = logs_dir / f"fetch-ecosysteem-coordinator-{timestamp}.log"
    
    with open(log_file, "w", encoding="utf-8") as logf:
        # Redirect stdout naar TeeWriter
        original_stdout = sys.stdout
        sys.stdout = TeeWriter(original_stdout, logf)
        
        try:
            return _execute_fetch(args, source_root, target_root, artefacten_root, log_file)
        finally:
            sys.stdout = original_stdout


def _execute_fetch(
    args: argparse.Namespace,
    source_root: Path,
    target_root: Path,
    artefacten_root: Path,
    log_file: Path,
) -> int:
    """Voer de eigenlijke fetch uit (met logging actief)."""

    print(f"\nFetch ecosysteem-coordinator  |  bron: {source_root}  ->  doel: {target_root}\n")

    # 1. Cleanup bestaande bestanden
    prompts_dir = target_root / ".github" / "prompts"
    agents_dir = target_root / ".github" / "agents"
    tasks_file = target_root / ".vscode" / "tasks.json"

    print("Opruimen bestaande bestanden:")
    n_cleaned = clean_folder(prompts_dir, "*.prompt.md", args.dry_run)
    n_cleaned += clean_folder(agents_dir, "*.agent.md", args.dry_run)
    
    if tasks_file.exists():
        if args.dry_run:
            print(f"  [dry] Verwijder: {tasks_file}")
        else:
            tasks_file.unlink()
            print(f"  ✗ Verwijderd: {tasks_file}")
        n_cleaned += 1
    
    if n_cleaned == 0:
        print("  (niets te verwijderen)")
    print()

    # 2. Verzamel nieuwe bestanden
    prompts, contracts, task_files = collect_ecosysteem_files(artefacten_root)

    print(f"Prompts ({len(prompts)}):")
    n_prompts = copy_files(
        prompts, target_root / ".github" / "prompts", args.dry_run, "prompt"
    )

    print(f"\nAgent-contracten ({len(contracts)}):")
    n_contracts = copy_files(
        contracts, target_root / ".github" / "agents", args.dry_run, "agent"
    )

    print(f"\nTasks ({len(task_files)} bronbestanden):")
    n_tasks = merge_and_write_tasks(
        task_files, target_root / ".vscode" / "tasks.json", source_root, target_root, args.dry_run
    )

    mode = "[DRY-RUN] " if args.dry_run else ""
    print(f"\n{'-'*60}")
    print(f"{mode}Klaar voor ecosysteem-coordinator (fnd.01)")
    print(f"  Prompts gekopieerd : {n_prompts}")
    print(f"  Agents gekopieerd  : {n_contracts}")
    print(f"  Tasks samengevoegd : {n_tasks}")
    print(f"  Log: {log_file.relative_to(target_root)}")
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
