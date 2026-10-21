"""Check the public code snapshot without executing analysis or reading lab data."""
from pathlib import Path
import ast
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK = ROOT / "notebooks" / "BACE1_PDB_pIC50.ipynb"
PUBLIC_FIGURES = {
    "assets/poster_results.png",
    "assets/synthetic_fingerprint_heatmap.png",
    "assets/synthetic_model_violin.png",
}
BLOCKED_EXTENSIONS = {
    ".csv", ".tsv", ".xls", ".xlsx", ".parquet", ".feather", ".npy", ".npz",
    ".smi", ".sdf", ".mol", ".mol2", ".pdb", ".cif", ".pkl", ".pickle",
    ".joblib", ".pt", ".pth", ".png", ".jpg", ".jpeg", ".pdf", ".html",
    ".zip", ".h5", ".hdf5",
}


def check():
    notebook = json.loads(NOTEBOOK.read_text(encoding="utf-8"))
    errors = []
    if notebook.get("nbformat") != 4:
        errors.append("Expected notebook format 4.")
    if set(notebook.get("metadata", {})) - {"kernelspec", "language_info"}:
        errors.append("Unexpected top-level notebook metadata.")
    code_cells = 0
    for index, cell in enumerate(notebook.get("cells", [])):
        text = "".join(cell.get("source", []))
        if cell.get("outputs"):
            errors.append(f"Cell {index}: saved outputs must be cleared.")
        if cell.get("execution_count") is not None:
            errors.append(f"Cell {index}: execution count must be cleared.")
        if cell.get("metadata") or cell.get("attachments"):
            errors.append(f"Cell {index}: remove metadata/attachments.")
        if re.search(r"data:image|image/(?:png|jpeg)|<table\b", text, re.I):
            errors.append(f"Cell {index}: possible embedded output.")
        if re.search(r"PubchemFP\d+|/Users/|/home/|/content/drive/", text):
            errors.append(f"Cell {index}: private selection or local path found.")
        if re.search(r"(?:gh[pousr]_[A-Za-z0-9]{20,}|sk-[A-Za-z0-9]{24,})", text):
            errors.append(f"Cell {index}: possible credential token.")
        if cell.get("cell_type") == "code":
            code_cells += 1
            # Notebook shell/package magics are not Python syntax. Mask those
            # lines for compilation; never execute them or download anything.
            lines = []
            for line in text.splitlines():
                if re.match(r"\s*(?:!|%|pip\s+install\b)", line):
                    lines.append("# notebook shell/package command omitted from static compilation")
                else:
                    lines.append(line)
            try:
                ast.parse("\n".join(lines), filename=f"notebook cell {index}")
            except SyntaxError as exc:
                errors.append(f"Cell {index}: {exc.msg}, line {exc.lineno}.")
    for path in ROOT.rglob("*"):
        relative = path.relative_to(ROOT)
        if ".git" in relative.parts or "__pycache__" in relative.parts:
            continue
        if (path.is_file() and path.suffix.lower() in BLOCKED_EXTENSIONS
                and relative.as_posix() not in PUBLIC_FIGURES):
            errors.append(f"Data/output artifact found in public folder: {relative}")
    if errors:
        for error in errors:
            print("FAIL:", error, file=sys.stderr)
        return 1
    print(f"PASS: {code_cells} code cells checked; outputs, execution metadata, "
          "hard-coded private fingerprint identities and common data artifacts absent.")
    print("No lab analysis, model training or software download was executed. "
          "This check does not certify authorization to share code or methods.")
    return 0


if __name__ == "__main__":
    raise SystemExit(check())
