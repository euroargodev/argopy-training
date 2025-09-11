import json
import os
import logging
log = logging.getLogger("hook.nbsoluce")


def clean_notebook(notebook_path):
    """Remove cells tagged with 'soluce' from a Jupyter notebook."""
    with open(notebook_path, 'r', encoding='utf-8') as f:
        notebook = json.load(f)

    # Filter out cells with the 'soluce' tag
    notebook['cells'] = [
        cell for cell in notebook['cells']
        if not cell.get('metadata', {}).get('tags', []).count('soluce')
    ]

    # Filter out cells starting with '##soluce'
    firstcellcodeline = lambda c: c.get('source', [])[0] if len(c.get('source', []))>0 else ''
    notebook['cells'] = [
        cell for cell in notebook['cells']
        if not (cell['cell_type'] == 'code' and '##soluce' in firstcellcodeline(cell))
    ]

    # Save the cleaned notebook
    with open(notebook_path.replace("_soluce.ipynb", ".ipynb"), 'w', encoding='utf-8') as f:
        json.dump(notebook, f, indent=1)

# def clean_all_notebooks(directory='.'):
#     """Clean all Jupyter notebooks in the specified directory."""
#     for notebook_path in glob.glob(os.path.join(directory, '*_soluce.ipynb')):
#         print(f"Cleaning {notebook_path}...")
#         clean_notebook(notebook_path)

def clean_all_notebooks(directory='.'):
    """Recursively clean all Jupyter notebooks in the specified directory and its subdirectories."""
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('_soluce.ipynb'):
                notebook_path = os.path.join(root, file)
                print(f"Cleaning {notebook_path}...")
                log.info(f"Cleaning {notebook_path}...")
                clean_notebook(notebook_path)

if __name__ == '__main__':
    clean_all_notebooks(directory='../notebooks')
