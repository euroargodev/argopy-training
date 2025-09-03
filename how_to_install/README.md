<img src="https://raw.githubusercontent.com/euroargodev/argopy/master/docs/_static/argopy_logo_long.png" alt="argopy logo" width="200"/>

# Training camp installation and setup instructions

> Note that training camps do not include an installation and setup session. 

List of requirements from participants:
- [ ] have a working argopy environment, running the latest version of argopy, i.e. **1.3.0**, as of September 2025
- [ ] have Jupyterlab or Jupyter installed, since training is with notebooks.
- [ ] download or clone this repository content in order to have training notebooks available to Jupyter for execution. 

<!-- TOC start -->

- [Training camp setup instructions](#training-camp-setup-instructions)
   * [Install a Python environment](#install-a-python-environment)
      + [Method 1](#method-1)
      + [Method 2 (recommended)](#method-2-recommended)
   * [Download training material ](#download-training-material)
      + [Method 1 (repository cloning)](#method-1-repository-cloning)
      + [Method 2 (repository archive download)](#method-2-repository-archive-download)
   * [Execute training notebooks](#execute-training-notebooks)

<!-- TOC end --> 

## Install a Python environment

Below are two succinct methods to install a Python environment with all the necessary libraries to execute argopy training notebooks.
  
### Method 1
Here's a minimal set of commands to install a fresh argopy python environment for this training.  
Assuming you have an environment manager like miniconda or conda.

```bash
conda create -n argopy-training python=3.11
conda activate argopy-training
mamba install -c conda-forge argopy gsw tqdm boto3 kerchunk numcodecs s3fs zarr dask distributed pyarrow ipython cartopy jupyterlab ipykernel ipywidgets matplotlib pyproj seaborn
```
then to add this environment to Jupyter:
```bash
python -m ipykernel install --name argopy-training --user
```

### Method 2 (recommended)
You can also use the **yml** file included in this repository to build a fully functional and complete environment with argopy, using library versions argopy has been tested with: 
```
conda env create -f https://raw.githubusercontent.com/euroargodev/argopy-training/refs/heads/main/how_to_install/argopy-training.yml
```
This command will create and install a complete `argopy-training` environment.

then to add this environment to Jupyter:
```bash
python -m ipykernel install --name argopy-training --user
```
  
## Download training material 

Once you have installed a fully functional Python environment, you need to download the training camp material from this repository. Again 2 methods are possible.

### Method 1 (repository cloning)

Navigate to an appropriate folder and clone the repository with git from the command line:
```
git clone https://github.com/euroargodev/argopy-training.git
```
This will create an `argopy-training` folder where all the repository content will be cloned.

### Method 2 (repository archive download)

By clicking to the link below:

https://github.com/euroargodev/argopy-training/archive/refs/heads/main.zip

your browser should download to your computer a zip archive of the repository content.

Simply un-archive the zip file to an appropriate folder.

## Execute training notebooks

Once you have your Python environment setup and the training material available, navigate from the command line to the `argopy-training/notebooks` folder and execute Jupyterlab or Jupyter:
```bash
cd argopy-training/notebooks
conda activate argopy-training
jupyter lab
```

You should now be ready to go !
