<img src="https://raw.githubusercontent.com/euroargodev/argopy/master/docs/_static/argopy_logo_long_training.png" alt="argopy logo" width="200"/>

[![DOI][joss-badge]][joss-link] [![Pypi][pip-badge]][pip-link] [![Conda][conda-badge]][conda-link]

[joss-badge]: https://img.shields.io/badge/DOI-10.21105%2Fjoss.02425-brightgreen
[joss-link]: https://dx.doi.org/10.21105/joss.02425
[pip-badge]: https://img.shields.io/pypi/v/argopy
[pip-link]: https://pypi.org/project/argopy/
[conda-badge]: https://img.shields.io/conda/vn/conda-forge/argopy?logo=anaconda
[conda-link]: https://anaconda.org/conda-forge/argopy

# Training camp installation and setup instructions

> Note that training camps do not include an installation and setup session. 

**List of requirements for participants**:
- [ ] have a working argopy environment, [running version 1.3.1 of argopy](https://argopy.readthedocs.io/en/v1.3.1/install.html)
- [ ] have [Jupyterlab or Jupyter](https://jupyter.org/install) installed, since training is with notebooks
- [ ] [clone](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository#cloning-a-repository) or [download](https://docs.github.com/en/repositories/working-with-files/using-files/downloading-source-code-archives#downloading-source-code-archives) this repository content in order to have training notebooks available to Jupyter for execution.

***

More detailed instructions below:
<!-- TOC start -->
* [1. Install a Python environment](#1-install-a-python-environment)
   + [Method 1 (recommended)](#method-1-recommended-tested-versions)
   + [Method 2](#method-2-free-versions)
* [2. Download training material ](#2-download-training-material)
   + [Method 1 (recommended)](#method-1-recommended-repository-cloning)
   + [Method 2](#method-2-repository-archive-download)
* [3. Test your installation](#3-test-your-installation)
* [4. Execute training notebooks](#4-execute-training-notebooks)
<!-- TOC end --> 

## 1. Install a Python environment

Below are two succinct methods to install a Python environment with all the necessary libraries to execute argopy training notebooks.

### Method 1 (recommended, tested versions)
[![Install Method 1](https://github.com/euroargodev/argopy-training/actions/workflows/check_install.yml/badge.svg?branch=main)](https://github.com/euroargodev/argopy-training/actions/workflows/check_install.yml)

Assuming you have an environment manager like [conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html#regular-installation) or [mamba](https://mamba.readthedocs.io/en/latest/installation/mamba-installation.html), or even [miniconda](https://www.anaconda.com/docs/getting-started/miniconda/install#quickstart-install-instructions) or [micromamba](https://mamba.readthedocs.io/en/latest/installation/micromamba-installation.html), use the **yml** file included in this repository to build a fully functional and complete environment with argopy, using library versions argopy has been tested with: 
```
conda env create -f https://raw.githubusercontent.com/euroargodev/argopy-training/refs/heads/main/get_ready/argopy-training.yml
```
This command will create and install a complete `argopy-training` environment.

Don't forget to add this environment kernel to Jupyter:
```bash
python -m ipykernel install --name argopy-training --user
```

### Method 2 (free versions)
[![Install Method 2](https://github.com/euroargodev/argopy-training/actions/workflows/check_install_upstream.yml/badge.svg)](https://github.com/euroargodev/argopy-training/actions/workflows/check_install_upstream.yml)

Assuming you have an environment manager like [conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html#regular-installation) or [mamba](https://mamba.readthedocs.io/en/latest/installation/mamba-installation.html), or even [miniconda](https://www.anaconda.com/docs/getting-started/miniconda/install#quickstart-install-instructions) or [micromamba](https://mamba.readthedocs.io/en/latest/installation/micromamba-installation.html), here's a minimal set of commands to install a fresh argopy python environment for this training:
```bash
conda create -n argopy-training python=3.11
conda activate argopy-training
conda install -c conda-forge argopy gsw tqdm boto3 kerchunk numcodecs s3fs zarr dask distributed pyarrow ipython cartopy jupyterlab jupyterlab-git ipykernel ipywidgets matplotlib pyproj seaborn
```
This command will create and install a complete `argopy-training` environment with the last available version of all dependencies.

Don't forget to add this environment kernel to Jupyter:
```bash
python -m ipykernel install --name argopy-training --user
```
  
## 2. Download training material 

Once you have installed a fully functional Python environment, you need to download the training camp material from this repository. Again 2 methods are possible.

> Note that the Argopy team will probably upload and update training notebooks up to the very last minutes before the training session, so please perform this step as late as possible.

### Method 1 (recommended, repository cloning)

All cloning details are available on this [Github help page](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository#cloning-a-repository).

In a nutshell and from the command line, navigate to an appropriate folder and clone the repository with git:
```
git clone https://github.com/euroargodev/argopy-training.git
```
This will create an `argopy-training` folder where all the repository content will be cloned (and possibly synchronized on-demand).

> A simple `git pull` will easily update your local copy with last minute changes on the remote repository.

### Method 2 (repository archive download)

If you are not familiar with git, you can also simply download an archive of the repository by clicking to the link below:

https://github.com/euroargodev/argopy-training/archive/refs/heads/main.zip

Your browser should download to your computer a zip archive of the repository content.

Simply un-archive the zip file to an appropriate folder.

All [Github download details can be found on this help page](https://docs.github.com/en/repositories/working-with-files/using-files/downloading-source-code-archives#downloading-source-code-archives).

## 3. Test your installation

In order to test if your installation is correct, the following argopy set of commands should work and return True

```python
import argopy
[argopy.DataFetcher().float(1901393).data.argo.N_POINTS == 25527 and
 argopy.DataFetcher(src='gdac', mode='expert').profile(5903248, 34).data.argo.N_POINTS == 70 and
 argopy.DataFetcher(src='argovis').region([-20, -16., 0, 10, 0, 100., '20250801','20250901']).data.argo.N_LEVELS == 172
]
```

## 4. Execute training notebooks

Once you have your Python environment setup and the training material available, navigate from the command line to the `argopy-training/content` folder and execute Jupyterlab or Jupyter:
```bash
cd argopy-training/content
conda activate argopy-training
jupyter lab
```

You should now be ready to go !
