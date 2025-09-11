**Hint for notebook producers**

### Template

You should use [this template](./template_argopy_training_EAONE_soluce.ipynb) to produce your notebooks.

### Pre-commit processing of notebooks

It could also be useful to develop notebooks with some code snippets as solutions to training exercice.

In this scenario, removing the code soluce in the published notebooks, while preserving it on your local copy is useful.

In order to do this, you can:
- create a `notebooks-with-soluce` folder at the root level of your local repo clone, it will be ignored by git.
- place in this folder, or sub-folder, your practice notebooks and name them with a `_soluce.ipynb` suffix.
- then execute the `for_nb_producers/clean-notebooks.py` script, it will:
  - remove all code cells that have either a `soluce` tag or simply start with `##soluce`
  - cleaned notebook are renamed without the `_soluce` suffix and copied to the `notebooks` root folder.
- Executing the `for_nb_producers/clean-notebooks.py` script will also replace notebook cells with a `disclaimer` tag with the appropriate content. There should be only one cell, typically at the bottom of a notebook, with this tag.

