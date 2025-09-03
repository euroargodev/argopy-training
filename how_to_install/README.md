This training is not meant to be an installation tutorial. We expect from you to have a working argopy environment, running the latest version of **argopy : 1.3.0**
  
but
  
Here's a minimal set of commands to install a fresh argopy python environment for this training.  
Assuming you have an environment manager like miniconda or conda.  

```
conda create -n argopy-training python=3.11
conda activate argopy-training
conda install -c conda-forge argopy
conda install -c conda-forge cartopy
# if you want to add this env to jupyter-lab
conda install -c conda-forge ipykernel
python -m ipykernel install --name argopy-training --user
```
  
You can also use the **yml** file included to build your environment : 
```
conda env create -f argopy-training.yml
```
