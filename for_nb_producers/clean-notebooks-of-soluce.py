import json
import os
import shutil
from pathlib import Path
import logging

log = logging.getLogger("hook.nbsoluce")


def clean_notebook(input_nb_path, output_nb_path):
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
    firstcellcodeline = lambda c: (
        c.get("source", [])[0] if len(c.get("source", [])) > 0 else ""
    )
    notebook["cells"] = [
        cell
        for cell in notebook["cells"]
        if not (cell["cell_type"] == "code" and "##soluce" in firstcellcodeline(cell))
    ]

    # Ensure the output directory exists
    os.makedirs(os.path.dirname(output_nb_path), exist_ok=True)

    # Save cleaned notebook
    p = output_nb_path.with_stem(
        output_nb_path.stem.replace("_soluce", "")
    ).with_suffix(".ipynb")
    with open(p, "w", encoding="utf-8") as f:
        json.dump(notebook, f, indent=1)
    return p


def copy_notebook(input_nb_path, output_nb_path):
    """Copy a Jupyter notebook to a new location, possibly overwriting existing one."""
    if output_nb_path.is_file():
        output_nb_path.unlink()
    shutil.copy2(input_nb_path, output_nb_path)


def clean_all_notebooks(folder_in=".", folder_out="."):
    """Recursively clean all Jupyter notebooks in the specified directory and its subdirectories."""
    input_dir = Path(folder_in)
    output_dir = Path(folder_out)

    # Clear or create the output directory
    # if output_dir.exists():
    #     shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    for notebook_path in input_dir.rglob("*.ipynb"):
        # Get the relative path of the notebook from the input directory
        relative_path = notebook_path.relative_to(input_dir)
        if ".ipynb_checkpoints" not in relative_path.parts:

            # Construct the corresponding output path
            output_path = output_dir / relative_path

            if "_soluce.ipynb" in notebook_path.name:
                op = clean_notebook(notebook_path, output_path)
                print(f"Cleaning {notebook_path} -> {op}")
            else:
                print(f"Unchanged {notebook_path} -> {output_path}")
                copy_notebook(notebook_path, output_path)

        # else:
        #     print(f"Skipping {notebook_path}")

if __name__ == "__main__":
    nbinput = "../notebooks-with-soluce"
    nboutput = "../notebooks"
    clean_all_notebooks(nbinput, nboutput)
