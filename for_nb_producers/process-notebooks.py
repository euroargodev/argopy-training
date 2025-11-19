import json
import os
import shutil
from pathlib import Path
import logging
from dataclasses import dataclass
import argopy


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

def copy_notebook(input_nb_path, output_nb_path):
    """Copy a Jupyter notebook to a new location, possibly overwriting existing one."""
    if output_nb_path.is_file():
        output_nb_path.unlink()
    shutil.copy2(input_nb_path, output_nb_path)
    return output_nb_path

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
                "\n***\n",
                "#### 👀 Useful argopy commands\n",
                "```python\n",
                "argopy.reset_options()\n",
                "argopy.show_options()\n",
                "argopy.status()\n",
                "argopy.clear_cache()\n",
                "argopy.show_versions()\n",
                "```\n",
                "#### ⚖️ License Information\n",
                "This Jupyter Notebook is licensed under the **European Union Public Licence (EUPL) v1.2**.\n",
                "\n",
                "| Permissions      | Limitations     | Conditions                     |\n",
                "|------------------|-----------------|--------------------------------|\n",
                "| ✔ Commercial use | ❌ Liability     | ⓘ License and copyright notice |\n",
                "| ✔ Modification   | ❌ Trademark use | ⓘ Disclose source              |\n",
                "| ✔ Distribution   | ❌ Warranty      | ⓘ State changes                |\n",
                "| ✔ Patent use     |                  | ⓘ Network use is distribution  |\n",
                "| ✔ Private use    |                  | ⓘ Same license                 |\n",
                "\n",
                "For more details, visit: [EUPL v1.2 Full Text](https://github.com/euroargodev/argopy-training/blob/main/LICENSE).\n",
                "\n",
                "#### 🤝 Sponsor\n",
                "![logo](https://raw.githubusercontent.com/euroargodev/argopy-training/refs/heads/main/for_nb_producers/disclaimer_argopy_EAONE.png)",
                "\n***\n",
            ]
            cell['metadata']['editable'] = False
        cells.append(cell)
    notebook["cells"] = cells

    # Ensure the output directory exists
    os.makedirs(os.path.dirname(output_nb_path), exist_ok=True)

    # Save cleaned notebook
    with open(output_nb_path, "w", encoding="utf-8") as f:
        json.dump(notebook, f, indent=1)
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
    notebook["cells"] = cells

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
    notebook["cells"] = cells

    # Ensure the output directory exists
    os.makedirs(os.path.dirname(output_nb_path), exist_ok=True)

    # Save cleaned notebook
    with open(output_nb_path, "w", encoding="utf-8") as f:
        json.dump(notebook, f, indent=1)
    return output_nb_path


@dataclass
class Header:
    title: str = None
    author: str = None
    author_url: str = None
    version: str = None
    version_default : str = f"v{argopy.__version__}"

    @property
    def html(self):
        style = "".join([
            '<style type="text/css">',
            '.tg  {border-collapse:collapse;border-spacing:0;}',
            '.tg td{border-color:rgb(16, 137, 182);border-style:solid;border-width:1px;font-family:Arial, sans-serif;font-size:14px;overflow:hidden;padding:10px 5px;word-break:normal;}',
            '.tg th{border-color:rgb(16, 137, 182);border-style:solid;border-width:1px;font-family:Arial, sans-serif;font-size:14px;font-weight:normal;overflow:hidden;padding:10px 5px;word-break:normal;}',
            '.tg .tg-73oq{border-color:rgb(10, 89, 162);text-align:left;vertical-align:middle}',
            '.tg .tg-42lt{border-color:rgb(10, 89, 162);text-align:center;vertical-align:middle}',
            '.tg .tg-5qt9{font-size:small;text-align:left;vertical-align:middle}',
            '</style>'
        ])

        version = self.version if self.version is not None else self.version_default
        table = "".join([
            '<table class="tg"><thead>',
            '  <tr>',
            '    <th class="tg-73oq"><img src="https://raw.githubusercontent.com/euroargodev/argopy/master/docs/_static/argopy_logo_long.png" alt="Argopy logo" width="120" height="60"></th>',
            f"    <th class='tg-42lt'><h1>{self.title}</h1></th>",
            '  </tr></thead>',
            '<tbody>',
            '  <tr>',
            f'    <td class="tg-5qt9" colspan="2"><span style="font-weight:bold">Author :</span> <a href="{self.author_url}" target="_blank" rel="noopener noreferrer">{self.author}</a></td>',
            '  </tr>',
            '  <tr>',
            f'    <td class="tg-5qt9" colspan="2">🏷️ This notebook is compatible with Argopy versions &gt;= <a href="https://argopy.readthedocs.io/en/{version}" target="_blank" rel="noopener noreferrer">{version}</a></td>',
            '  </tr>',
            '  <tr>',
            '    <td class="tg-5qt9" colspan="2">© <a href="https://github.com/euroargodev/argopy-training/blob/main/LICENSE" target="_blank" rel="noopener noreferrer">European Union Public Licence (EUPL) v1.2</a>, see at the bottom of this notebook for more.</td>',
            '  </tr>',
            '</tbody>',
            '</table>',
        ])

        return f"{style}{table}"


def insert_header(input_nb_path, output_nb_path):
    with open(input_nb_path, "r", encoding="utf-8") as f:
        notebook = json.load(f)

    def read_data(data, cell_source):
        data_index = next((i for i, item in enumerate(cell_source) if f'{data}:' in item), None)
        if data_index is not None:
            return cell_source[data_index].split(":")[-1].strip()
        return None

    # Look for <!--HEADER--> in a cell and replace with header html:
    cells, head = [], None
    for cell in notebook["cells"]:
        if cell['cell_type'] == 'markdown':
            # Find the index of the line containing '<!--HEADER-->'
            header_index = next((i for i, item in enumerate(cell['source']) if '<!--HEADER-->' in item), None)
            if header_index is not None:
                print("\tFound HEADER to insert")
                # Find header data:
                head = Header(title = read_data('TITLE', cell['source']),
                       author = read_data('AUTHOR', cell['source']),
                       author_url = read_data('AUTHOR_URL', cell['source']),
                       version = read_data('VERSION', cell['source']))
                print(head)
                # Replace the line with the HEADER contents:
                cell['source'][header_index:header_index + 1] = [head.html]
                # Remove raw header data:
                for data in ['TITLE', 'AUTHOR', 'AUTHOR_URL', 'VERSION']:
                    [cell['source'].pop(i) for i, item in enumerate(cell['source']) if f"{data}:" in item]
        cells.append(cell)
    notebook["cells"] = cells

    # Find line with a link to the documentation and update version according to the HEADER
    cells = []
    for cell in notebook["cells"]:
        if cell['cell_type'] == 'markdown':
            # eg: This notebook shows how to use the [DataFetcher](https://argopy.readthedocs.io/en/v1.3.0/generated/argopy.fetchers.ArgoDataFetcher.html#argopy.fetchers.ArgoDataFetcher):
            if head is not None:
                version = head.version if head.version is not None else Header.version_default
            else:
                version = Header.version_default
            for i, item in enumerate(cell['source']):
                if 'https://argopy.readthedocs.io/en/v1.3.0' in item:
                    cell['source'][i] = item.replace('https://argopy.readthedocs.io/en/v1.3.0',
                                                     f'https://argopy.readthedocs.io/en/{version}')
                if 'https://argopy.readthedocs.io/en/latest' in item:
                    cell['source'][i] = item.replace('https://argopy.readthedocs.io/en/latest',
                                                     f'https://argopy.readthedocs.io/en/{version}')
        cells.append(cell)
    notebook["cells"] = cells

    # Ensure the output directory exists
    os.makedirs(os.path.dirname(output_nb_path), exist_ok=True)

    # Save cleaned notebook
    with open(output_nb_path, "w", encoding="utf-8") as f:
        json.dump(notebook, f, indent=1)
    return output_nb_path


def fix_orth(input_nb_path, output_nb_path):
    with open(input_nb_path, "r", encoding="utf-8") as f:
        notebook = json.load(f)

    cells = []
    for cell in notebook["cells"]:
        if cell['cell_type'] == 'markdown':
            for i, line in enumerate(cell['source']):
                cell['source'][i] = cell['source'][i].replace("EXERCICE", "EXERCISE")
                cell['source'][i] = cell['source'][i].replace("exercice", "exercise")
        cells.append(cell)
    notebook["cells"] = cells

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
                fix_orth(op, op)
                print(f"Cleaning {notebook_path} -> {op}")
            else:
                op = copy_notebook(notebook_path, output_path)
                fix_orth(op, op)
                print(f"Unchanged {notebook_path} -> {op}")

            fix_disclaimer(op, op)
            insert_toc(op, op)
            insert_header(op, op)

        # else:
        #     print(f"Skipping {notebook_path}")

if __name__ == "__main__":
    nbinput = "../notebooks-with-soluce"
    nboutput = "../content"
    process_all_notebooks(nbinput, nboutput)
