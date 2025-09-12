| <img src="https://raw.githubusercontent.com/euroargodev/argopy/master/docs/_static/argopy_logo_long.png" alt="argopy logo" width="200"/><br>A python library dedicated to Argo data access, visualisation and manipulation for regular users as well as Argo experts and operators | 
|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------:|
|                                                                     [![DOI][joss-badge]][joss-link] [![Pypi][pip-badge]][pip-link] [![Conda][conda-badge]][conda-link]                                                                     |

[joss-badge]: https://img.shields.io/badge/DOI-10.21105%2Fjoss.02425-brightgreen
[joss-link]: https://dx.doi.org/10.21105/joss.02425
[ci-badge]: https://github.com/euroargodev/argopy/actions/workflows/pytests.yml/badge.svg
[cov-badge]: https://codecov.io/gh/euroargodev/argopy/branch/master/graph/badge.svg
[cov-link]: https://codecov.io/gh/euroargodev/argopy
[rtd-badge]: https://img.shields.io/readthedocs/argopy?logo=readthedocs
[rtd-link]: https://argopy.readthedocs.io/en/latest/?badge=latest
[pip-badge]: https://img.shields.io/pypi/v/argopy
[pip-link]: https://pypi.org/project/argopy/
[conda-badge]: https://img.shields.io/conda/vn/conda-forge/argopy?logo=anaconda
[conda-link]: https://anaconda.org/conda-forge/argopy
[ossf-badge]: https://www.bestpractices.dev/projects/5939/badge
[ossf-link]: https://www.bestpractices.dev/projects/5939

# Material for Argopy training camps

This repository is dedicated to host the material required for Argopy training sessions.

## Install and setup

**You will need to set up your Python environment with the last Argopy version and all required dependencies.**

> Note that Argopy training camps do not start with an installation tutorial. We expect from attendees a working Argopy environment to start the training.

Since all the training material is provided as [Jupyter notebooks](https://jupyter.org/install), you will also need to set up **Jupyter** (we recommend JupyterLab) and install the Python kernel where you installed Argopy.

To get you started though, succinct install and setup instructions are given in the "[how_to_install](./how_to_install)" folder of this repository.

## Training Content

A typical Argopy training camp is organized in 2 sessions.

### Session 1: General introduction to Argopy

To start with, check this PDF with a general introduction to the Argopy library.

Then move on to execute the following hands-on notebook:

| Theme                             | Notebook                                                                       | 
|-----------------------------------|--------------------------------------------------------------------------------|
| 🚀 [Hands on](notebooks/hands-on) | [Examples of Argo features](./notebooks/hands-on/argopy-getting-started.ipynb) |

### Session 2: Practice with thematic notebooks

Select the thematic you are the most interested in, and raise your expertise by going through each notebook and exercice there-in.

| Theme                                                            | Notebooks                                                                                                       |
|------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------|
| 📊 [Argo data fetching](./notebooks/argo-data-fetching)          | [Select and fetch data](./notebooks/argo-data-fetching/select-and-fetch-data.ipynb)                             |
|                                                                  | [Source and user mode](./notebooks/argo-data-fetching/fetching-options.ipynb)                                   |
|                                                                  | [BGC data specifics](./notebooks/argo-data-fetching/bgc-specifics.ipynb)                                        |
|                                                                  | [Direct access to one float dataset](./notebooks/argo-data-fetching/direct-access-to-float-dataset.ipynb)       |
|                                                                  | How to handle large data selection                                                                              |
| 🛠️ [Argo data manipulation](./notebooks/argo-data-manipulation) | Filtering (QC flags, data mode)                                                                                 |
|                                                                  | [Vertical interpolation & binning](./notebooks/argo-data-manipulation/vertical-interpolation-and-binning.ipynb) |
|                                                                  | [Compute (TEOS, Optic, CANYON-MED)](./notebooks/argo-data-manipulation/compute.ipynb)                           |
|                                                                  | [Compute your own per-profile diagnostic](./notebooks/argo-data-manipulation/compute-custom.ipynb)              |
| 🗃️ [Argo index and meta-data](./notebooks/argo-index-meta-data) | Explore Argo index files                                                                                        |
|                                                                  | Argo Reference tables lookup                                                                                    |
