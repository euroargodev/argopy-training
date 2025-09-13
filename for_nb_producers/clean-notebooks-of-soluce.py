import json
import os
import shutil
from pathlib import Path
import logging

log = logging.getLogger("hook.nbsoluce")

firstcellcodeline = lambda c: (
    c.get("source", [])[0] if len(c.get("source", [])) > 0 else ""
)

def clean_notebook_soluce(input_nb_path, output_nb_path):
    """Remove cells tagged with 'soluce' from a Jupyter notebook."""
    with open(input_nb_path, "r", encoding="utf-8") as f:
        notebook = json.load(f)

    # Filter out cells with the 'soluce' tag
    notebook["cells"] = [
        cell
        for cell in notebook["cells"]
        if not cell.get("metadata", {}).get("tags", []).count("soluce")
    ]

    # Filter out cells starting with '##soluce'
    notebook["cells"] = [
        cell
        for cell in notebook["cells"]
        if not (cell["cell_type"] == "code" and "##soluce" in firstcellcodeline(cell))
    ]

    # We also remove all code cell output:
    cells = []
    for cell in notebook["cells"]:
        if cell["cell_type"] == "code":
            cell["outputs"] = []
            cell['execution_count'] = None
        cells.append(cell)
    notebook["cells"] = cells

    # Ensure the output directory exists
    os.makedirs(os.path.dirname(output_nb_path), exist_ok=True)

    # Save cleaned notebook
    p = output_nb_path.with_stem(
        output_nb_path.stem.replace("-soluce", "")
    ).with_suffix(".ipynb")
    with open(p, "w", encoding="utf-8") as f:
        json.dump(notebook, f, indent=1)
    return p

def fix_disclaimer(input_nb_path, output_nb_path):
    """Fill in disclaimer cell"""
    with open(input_nb_path, "r", encoding="utf-8") as f:
        notebook = json.load(f)

    # Look for the disclaimer cell and add content:
    cells = []
    for cell in notebook["cells"]:
        if cell.get("metadata", {}).get("tags", []).count("disclaimer"):
            print("\tFound disclaimer to insert")
            cell["source"] = [
                "## 🏁 End of the notebook\n",
                "***\n",
                "Useful argopy commands:\n",
                "```python\n",
                "argopy.reset_options()\n",
                "argopy.show_options()\n",
                "argopy.status()\n",
                "argopy.clear_cache()\n",
                "argopy.show_versions()\n",
                "```\n",
                "***\n",
                "![logo](https://raw.githubusercontent.com/euroargodev/argopy-training/refs/heads/main/for_nb_producers/template_argopy_training_EAONE.png)"
            ]
        cells.append(cell)
    notebook["cells"] = cells

    # Ensure the output directory exists
    os.makedirs(os.path.dirname(output_nb_path), exist_ok=True)

    # Save cleaned notebook
    with open(output_nb_path, "w", encoding="utf-8") as f:
        json.dump(notebook, f, indent=1)
    return output_nb_path

def copy_notebook(input_nb_path, output_nb_path):
    """Copy a Jupyter notebook to a new location, possibly overwriting existing one."""
    if output_nb_path.is_file():
        output_nb_path.unlink()
    shutil.copy2(input_nb_path, output_nb_path)
    return output_nb_path

def insert_toc(input_nb_path, output_nb_path):
    with open(input_nb_path, "r", encoding="utf-8") as f:
        notebook = json.load(f)

    def generate_toc(notebook):
        """Generate a Markdown TOC from notebook headings."""
        toc_lines = ["\n**Table of Contents**\n"]
        for cell in notebook['cells']:
            if cell['cell_type'] == "markdown":
                for line in cell['source']:
                    if line.startswith("#") and not line.startswith("## Notebook Title"):
                        # Extract heading level and text
                        level = line.count("#")
                        if level >= 2:
                            text = line.lstrip("#").strip()
                            indent = "  " * (level - 2)
                            toc_lines.append(f"{indent}- [{text}](#{text.lower().replace(' ', '-')})\n")
        return toc_lines

    # Get notebook TOC:
    toc = generate_toc(notebook)

    # Look for a TOC cell and replace content:
    cells = []
    for cell in notebook["cells"]:
        if cell.get("metadata", {}).get("tags", []).count("toc"):
            cell["source"] = toc
        cells.append(cell)

    # Also look for the <!--TOC--> tag in cell, and replace it:
    cells = []
    for cell in notebook["cells"]:
        if cell['cell_type'] == 'markdown':
            # Find the index of the line containing '<!--TOC-->'
            toc_index = next((i for i, item in enumerate(cell['source']) if '<!--TOC-->' in item), None)
            if toc_index is not None:
                print("\tFound TOC to insert")
                # Replace the line with the TOC contents
                cell['source'][toc_index:toc_index + 1] = toc
        cells.append(cell)

    # Ensure the output directory exists
    os.makedirs(os.path.dirname(output_nb_path), exist_ok=True)

    # Save cleaned notebook
    with open(output_nb_path, "w", encoding="utf-8") as f:
        json.dump(notebook, f, indent=1)
    return output_nb_path

def process_all_notebooks(folder_in=".", folder_out="."):
    """Recursively process all Jupyter notebooks in the specified directory and its subdirectories."""
    input_dir = Path(folder_in)
    output_dir = Path(folder_out)
    output_dir.mkdir(parents=True, exist_ok=True)

    for notebook_path in input_dir.rglob("*.ipynb"):
        # Get the relative path of the notebook from the input directory
        relative_path = notebook_path.relative_to(input_dir)
        if ".ipynb_checkpoints" not in relative_path.parts:

            # Construct the corresponding output path
            output_path = output_dir / relative_path

            if "-soluce.ipynb" in notebook_path.name:
                op = clean_notebook_soluce(notebook_path, output_path)
                print(f"Cleaning {notebook_path} -> {op}")
            else:
                op = copy_notebook(notebook_path, output_path)
                print(f"Unchanged {notebook_path} -> {op}")

            fix_disclaimer(op, op)
            insert_toc(op, op)


        # else:
        #     print(f"Skipping {notebook_path}")

if __name__ == "__main__":
    nbinput = "../notebooks-with-soluce"
    nboutput = "../notebooks"
    process_all_notebooks(nbinput, nboutput)
