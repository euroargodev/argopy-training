This training is not meant to be an installation tutorial. We expect from you to have a working argopy environment, running the latest version of **argopy : 1.3.0**
  
but
  
Here's a minimal set of commands to install a fresh argopy python environment for this training.  
Assuming you have an environment manager like miniconda or conda.  

```
conda create -n argopytraining python=3.11
conda activate argopytraining
pip install argopy
conda install cartopy
# if you want to add this env to jupyter-lab
pip install ipykernel
python -m ipykernel install --name argopytraining --user
```
  
You can also use the **yml** file included to build your environment.