# Hints for notebook producers

## Template

You should use [this template](./template_argopy_training_EAONE_soluce.ipynb) to produce your notebooks.

## Pre-commit processing of notebooks

In order to preserve a uniform visual design of Argopy training notebooks, we recommend the following procedure:

- create a `notebooks-with-soluce` folder at the root level of your local repo clone, it will be ignored by git.
- place in this folder, and/or sub-folders, your practice notebooks and name them with a `_soluce.ipynb` suffix.
- then execute the `for_nb_producers/process-notebooks.py` script. This will sequentially:
  - remove all soluce code cells (see below),
  - copy the notebook file to the `content` root folder, and remove the `_soluce` suffix,
  - process disclaimer markdown cell (see below), 
  - insert a table of content (see below),
  - process header markdown cell and update version (see below).

### Hidden code cell with soluce

If you want to hide code cells, typically with an exercise solution, you can:
- insert `##soluce` in the first line of a code cell,
- or tag a code cell with `soluce``.


### Disclaimer in a markdown cell

In order to insert a disclaimer, you should:
- tag a cell with `disclaimer`, the cell content will be replaced by the disclaimer template.


### Header markdown cell

A typical header cell is expected to have these elements:

```markdown
<!--HEADER-->
TITLE: Some title here
AUTHOR: G. Maze
AUTHOR_URL: https://annuaire.ifremer.fr/cv/17182

**Description:**

This notebook describes how to ....
```

If your notebook deals with an Argopy feature introduced in a version higher than v1.3.0 (default), then you should add this version like this: ``VERSION:v1.4.0`` right after ``AUTHOR_URL`` above. Then, all markdown cell lines with a link to the RTD documentation (pointing to a specific version or `latest`) will be updated to point toward this version identified in the header.

### Table of content in a markdown cell

In order to insert the table of content of a notebook, you can:
- add `<!--TOC-->` anywhere in a markdown cell,
- or tag a cell with `toc`, the cell content will be replaced by the table of content.
